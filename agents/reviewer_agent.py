import json
from openai import OpenAI
from config import MODEL_NAME

client = OpenAI()

def review_translation_with_feedback(original, draft, feedback_json, source_lang, target_lang):
    prompt = f"""
You are a translation reviewer and refiner.

User asked for translation {source_lang} -> {target_lang}.

Original:
{original}

Draft translation:
{draft}

External feedback (JSON):
{feedback_json}

Step 1: Briefly explain what is wrong (or confirm it's excellent).
Step 2: If decision is REVISE, output an improved translation.

Return STRICT JSON:
{{
  "feedback": "...",
  "final_translation": "...",
  "decision": "ACCEPT" or "REVISE"
}}
"""
    r = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = r.choices[0].message.content.strip()
    return json.loads(content)
