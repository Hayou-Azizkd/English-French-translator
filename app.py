import streamlit as st
from translator import translate

# Page configuration
st.set_page_config(
    page_title="English ⟷ French Translator",
    page_icon="🌍",
    layout="centered"
)

# Initialize session state for language swap
if 'swap_languages' not in st.session_state:
    st.session_state.swap_languages = False

# Title and description
st.title("🌍 English ⟷ French Translator")
st.markdown("*Powered by OpenAI GPT-4o-mini*")

# Language selection
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    # Determine source language based on swap state
    default_source = 1 if st.session_state.swap_languages else 0
    source_lang = st.selectbox(
        "From:",
        ["English", "French"],
        index=default_source
    )

with col2:
    # Swap button in the middle
    st.write("")  # Add spacing
    if st.button("🔄"):
        st.session_state.swap_languages = not st.session_state.swap_languages
        st.rerun()

with col3:
    # Automatically set opposite language
    target_lang = "French" if source_lang == "English" else "English"
    st.selectbox(
        "To:",
        [target_lang],
        disabled=True
    )

# Divider
st.markdown("---")

# Text input
input_text = st.text_area(
    f"Enter {source_lang} text:",
    height=150,
    placeholder=f"Type or paste your {source_lang} text here..."
)

# Character count
if input_text:
    st.caption(f"📝 {len(input_text)} characters | {len(input_text.split())} words")

# Translate button
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if input_text.strip():
        with st.spinner("Translating..."):
            try:
                # Call the translate function
                translation = translate(input_text, source_lang, target_lang)
                
                # Display result
                st.markdown("---")
                st.success(f"**Translation ({target_lang}):**")
                st.write(translation)
                
                # Code block for easy copying
                st.code(translation, language=None)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is set correctly in the .env file")
    else:
        st.warning("⚠️ Please enter some text to translate")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and OpenAI API")