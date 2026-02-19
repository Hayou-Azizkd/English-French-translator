# agents/translator_agent.py

from clients import client
from config import MODEL_NAME, TRANSLATION_TEMPERATURE

def translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text between languages using OpenAI.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a professional translator. Translate from {source_lang} to {target_lang}. "
                    "Provide only the translation without explanations."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=TRANSLATION_TEMPERATURE,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from translation model")
    return content.strip()
