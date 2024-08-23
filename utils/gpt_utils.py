from typing import Optional, Dict
import logging

def generate_gpt4_response(openai_client, query: str, context: Optional[str] = None, metadata: Optional[Dict[str, str]] = None) -> str:
    try:
        system_message = (
            "You are a helpful and compassionate assistant designed to support seniors during medical emergencies "
            "while traveling. Your primary role is to provide accurate and clear medical advice based on the user's "
            "symptoms or questions about diseases. When the user asks about a disease or symptom, "
            "show the related metadata, such as the disease and intent, and then provide the best advice based on "
            "the retrieved information."
        )

        user_message = (
            f"User Query: {query}\n\n"
            f"Context: {context}\n\n"
            f"Metadata:\n"
            f"- Category: {metadata.get('질병 카테고리', 'N/A') if metadata else 'N/A'}\n"
            f"- Disease: {metadata.get('질병', 'N/A') if metadata else 'N/A'}\n"
            f"- Department: {metadata.get('부서', 'N/A') if metadata else 'N/A'}\n"
            f"- Intent: {metadata.get('의도', 'N/A') if metadata else 'N/A'}\n"
            f"- Score: {metadata.get('score', 'N/A') if metadata else 'N/A'}\n"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.3,
            n=1,
            stop=None,
        )

        generated_response = response.choices[0].message.content.strip()
        logging.info(f"GPT-4 응답 생성 완료: 길이={len(generated_response)}")

        return generated_response

    except Exception as e:
        logging.error(f"GPT-4 응답 생성 중 오류 발생: {str(e)}", exc_info=True)
        return "죄송합니다. GPT-4 응답을 생성하는 중에 오류가 발생했습니다."
