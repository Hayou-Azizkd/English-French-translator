import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def translate(text, source_lang, target_lang):
    """
    Translate text between languages using OpenAI.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language (e.g., "English", "French")
        target_lang (str): Target language (e.g., "English", "French")
    
    Returns:
        str: Translated text
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate from {source_lang} to {target_lang}. Provide only the translation without explanations."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3  # Low temperature for consistent translations
    )
    
    return response.choices[0].message.content

# Test the translator when running directly
if __name__ == "__main__":
    # Test translation
    test_text = "Hello, how are you today?"
    result = translate(test_text, "English", "French")
    print(f"Original: {test_text}")
    print(f"Translation: {result}")