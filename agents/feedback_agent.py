from openai import OpenAI
from config import MODEL_NAME

client = OpenAI()

def generate_translation_feedback(original: str, translation: str, source_lang: str, target_lang: str) -> str:
    """
    Creates external feedback in a structured way (JSON).
    """
    prompt = f"""
You are a strict evaluator for translation quality.

Original ({source_lang}):
{original}

Translation ({target_lang}):
{translation}

Check these:
1) Is the translation fully in {target_lang}?
2) Is meaning preserved (no missing/added information)?
3) Are numbers/dates/proper nouns preserved?
4) Is it natural and idiomatic?

Return STRICT JSON:
{{
  "checks": {{
    "target_language_ok": true/false,
    "meaning_ok": true/false,
    "numbers_preserved": true/false,
    "naturalness_ok": true/false
  }},
  "feedback": "1-3 sentences",
  "decision": "ACCEPT" or "REVISE"
}}
"""
    r = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return r.choices[0].message.content.strip()
