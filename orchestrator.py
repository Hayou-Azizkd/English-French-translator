from agents.translator_agent import translate
from agents.feedback_agent import generate_translation_feedback
from agents.reviewer_agent import review_translation_with_feedback

def run_translation_agent(text, source_lang, target_lang):
    draft = translate(text, source_lang, target_lang)
    feedback_json = generate_translation_feedback(text, draft, source_lang, target_lang)

    review_obj = review_translation_with_feedback(
        original=text,
        draft=draft,
        feedback_json=feedback_json,
        source_lang=source_lang,
        target_lang=target_lang
    )

    final_text = review_obj["final_translation"]
    status = "accepted" if review_obj["decision"] == "ACCEPT" else "revised"

    return {
        "final_translation": final_text,
        "initial_translation": draft,
        "review_verdict": review_obj["feedback"],
        "status": status,
        "external_feedback": feedback_json
    }
