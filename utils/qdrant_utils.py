from typing import List, Any
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from rank_bm25 import BM25Okapi
import logging

class QdrantRetriever:
    def __init__(self, client: QdrantClient, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    def retrieve(self, query_vector: List[float], top_k: int = 20) -> List[Any]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return results

def create_documents_from_qdrant_results(results) -> List[Document]:
    documents = []
    for result in results:
        text = result.payload.get('답변', 'N/A')
        metadata = {
            'id': result.id,
            '질병 카테고리': result.payload.get('질병_카테고리', 'N/A'),
            '질병': result.payload.get('질병', 'N/A'),
            '부서': result.payload.get('부서', 'N/A'),
            '의도': result.payload.get('의도', 'N/A'),
            'score': result.score
        }
        documents.append(Document(page_content=text, metadata=metadata))
    return documents

def ensemble_search(query: str, client: QdrantClient, collection_name: str, top_k: int = 1) -> List[Document]:
    encoder = SentenceTransformer("jhgan/ko-sroberta-multitask")
    qdrant_retriever = QdrantRetriever(client=client, collection_name=collection_name)

    query_vector = encoder.encode(query).tolist()
    qdrant_results = qdrant_retriever.retrieve(query_vector, top_k=20)

    if not qdrant_results:
        logging.warning("Qdrant에서 검색 결과가 없습니다.")
        return []

    documents = create_documents_from_qdrant_results(qdrant_results)
    bm25_retriever = BM25Okapi([doc.page_content for doc in documents])
    bm25_results = bm25_retriever.get_top_n(query.split(), documents, n=top_k)

    if not bm25_results:
        logging.warning("BM25에서 유사한 문서가 없습니다.")
        return []

    combined_results = []
    for bm25_result in bm25_results:
        matching_qdrant_result = next((doc for doc in documents if doc.page_content == bm25_result.page_content), None)
        if matching_qdrant_result:
            combined_score = 0.5 * matching_qdrant_result.metadata.get('score', 0) + 0.5 * bm25_result.metadata.get('score', 1)
            matching_qdrant_result.metadata['combined_score'] = combined_score
            combined_results.append(matching_qdrant_result)

    combined_results.sort(key=lambda x: x.metadata['combined_score'], reverse=True)
    return combined_results[:top_k] if combined_results else []
