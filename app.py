import streamlit as st
from rag_engine import search, generate_answer
import base64
import os


st.title("HIPAA Compliance Assistant")

# --- Styling ---
st.markdown(
    """
    <style>
    /* Text colors */
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #ffffff !important;
    }
    .stTextInput > label {
        color: #ffffff !important;
    }
    .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    .stButton > button:hover {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }
    /* Input fields */
    .stTextInput > div > div > input {
    color: #000000 !important;
    }
    
    
    /* Info, warning, error boxes */
    .stAlert {
        background-color: rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #ffffff !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def set_bg(image_file):
    """Set background image if it exists."""
    if not os.path.exists(image_file):
        st.warning(f"Background image '{image_file}' not found. Using default background.")
        return
    
    try:
        with open(image_file, "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

        bg_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load background image: {str(e)}")

set_bg("background.png")


def run_hipaa_query(prompt: str):
    """Execute HIPAA query with RAG system."""
    if not prompt or prompt.strip() == "":
        st.warning("Please enter a question.")
        return
    
    try:
        with st.spinner(" Searching ..."):
            retrieved = search(prompt, k=3)

        with st.spinner("Generating answer..."):
            answer = generate_answer(prompt, retrieved)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("📚View Retrieved Context"):
            for i, chunk in enumerate(retrieved):
                st.markdown(f"**Chunk {i+1}:**")
                st.write(chunk["text"])
                if i < len(retrieved) - 1:
                    st.markdown("---")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try rephrasing your question or contact support if the issue persists.")


# Initialize session state for FAQ selection
if 'selected_faq' not in st.session_state:
    st.session_state.selected_faq = None

# User input
user_prompt = st.text_input("Ask a HIPAA-related question:", key="user_input")

# Common questions section
st.markdown("### Or try some common questions:")

col1, col2, col3,  = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    if st.button("Minimum Necessary Rule", use_container_width=True):
        st.session_state.selected_faq = "What is the HIPAA Minimum Necessary standard and when does it NOT apply?"

with col2:
    if st.button("Privacy vs Security Rule", use_container_width=True):
        st.session_state.selected_faq = "What is the difference between the HIPAA Privacy Rule and Security Rule?"

with col3:
    if st.button("Breach Notification", use_container_width=True):
        st.session_state.selected_faq = "When does HIPAA require breach notification and what must be included?"
with col4:
    if st.button("Patient Rights", use_container_width=True):
        st.session_state.selected_faq ="What are the key patient rights under HIPAA?"

with col5:
    if st.button("Daily Awareness", use_container_width=True):
        st.session_state.selected_faq = "What are the important daily practices for HIPAA compliance in healthcare?"

with col6:
    if st.button("Consequences", use_container_width=True):
        st.session_state.selected_faq ="What are the penalties and consequences for HIPAA violations?"


# Determine which prompt to use
final_prompt = None

if st.session_state.selected_faq:
    final_prompt = st.session_state.selected_faq
    st.info(f": {final_prompt}")
    # Clear the FAQ selection after displaying
    st.session_state.selected_faq = None
elif user_prompt:
    final_prompt = user_prompt

# Execute query if there's a prompt
if final_prompt:
    run_hipaa_query(final_prompt)

# Footer
st.markdown("---")
st.caption(" This assistant provides information about HIPAA regulations. For legal advice, please consult a qualified attorney.")