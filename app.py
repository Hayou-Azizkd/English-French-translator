import streamlit as st
from orchestrator import run_translation_agent
from config import MAX_INPUT_CHARS

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="English ⟷ French Translator",
    page_icon="🌍",
    layout="centered"
)

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "swap_languages" not in st.session_state:
    st.session_state.swap_languages = False

if "show_debug" not in st.session_state:
    st.session_state.show_debug = False

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🌍 English ⟷ French Translator")
st.markdown(
    "*Powered by OpenAI GPT-4o-mini — agentic workflow with reflection & external feedback*"
)

# -------------------------------------------------
# Language selection
# -------------------------------------------------
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    default_source = 1 if st.session_state.swap_languages else 0
    source_lang = st.selectbox(
        "From:",
        ["English", "French"],
        index=default_source
    )

with col2:
    st.write("")
    if st.button("🔄"):
        st.session_state.swap_languages = not st.session_state.swap_languages
        st.rerun()

with col3:
    target_lang = "French" if source_lang == "English" else "English"
    st.selectbox(
        "To:",
        [target_lang],
        disabled=True
    )

# -------------------------------------------------
# Input
# -------------------------------------------------
st.markdown("---")

input_text = st.text_area(
    f"Enter {source_lang} text:",
    height=150,
    placeholder=f"Type or paste your {source_lang} text here..."
)

if input_text:
    st.caption(
        f"📝 {len(input_text)} characters | {len(input_text.split())} words"
    )

# Debug toggle
st.session_state.show_debug = st.toggle(
    "Show agent trace (draft, feedback, review)",
    value=st.session_state.show_debug
)

# -------------------------------------------------
# Translate
# -------------------------------------------------
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to translate")
        st.stop()

    if MAX_INPUT_CHARS and len(input_text) > MAX_INPUT_CHARS:
        st.warning(f"⚠️ Please keep input under {MAX_INPUT_CHARS} characters")
        st.stop()

    with st.spinner("Running agentic translation workflow..."):
        try:
            result = run_translation_agent(
                input_text,
                source_lang,
                target_lang
            )

            final_translation = result["final_translation"]
            status = result["status"]  # accepted | revised

            st.markdown("---")

            if status == "accepted":
                st.success(
                    f"✅ **Translation ({target_lang}) — accepted by reviewer**"
                )
            else:
                st.warning(
                    f"🛠️ **Translation ({target_lang}) — revised after reflection**"
                )

            st.write(final_translation)
            st.code(final_translation, language=None)

            # -------------------------------------------------
            # Agent trace (debug)
            # -------------------------------------------------
            if st.session_state.show_debug:
                with st.expander("🔍 Agent trace"):
                    st.markdown("**V1 — Initial draft**")
                    st.write(result["initial_translation"])

                    st.markdown("**Reviewer verdict**")
                    st.code(result["review_verdict"])

                    if "external_feedback" in result:
                        st.markdown("**External feedback (checks)**")
                        st.code(result["external_feedback"])

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info(
                "💡 Ensure OPENAI_API_KEY is set correctly in your .env file"
            )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "Built with Streamlit + OpenAI API • "
    "Agentic pipeline: draft → external feedback → reflection → decision"
)
