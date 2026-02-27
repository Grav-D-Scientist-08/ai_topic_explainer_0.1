import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Topic Explainer",
    page_icon="🧠",
    layout="wide"
)

# ------------------ GLASS UI CSS ------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    font-weight: 600;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD ENV ------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key missing")
    st.stop()

client = Groq(api_key=api_key)

# ------------------ HEADER ------------------
st.title("🧠 AI Topic Explainer")
st.caption("Explain any topic in seconds with examples")

st.markdown(
    """
    <div style='text-align:center; padding:10px;'>
        <h3>⚡ Explain Any Topic in Seconds</h3>
        <p style='color:gray;'>Perfect for students, developers & interview prep</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ EXAMPLE BUTTONS ------------------
st.markdown("### 🔥 Try Examples")

example_cols = st.columns(4)
examples = [
    "Machine Learning",
    "SQL Joins",
    "Python Decorators",
    "Normalization in DBMS"
]

for i, ex in enumerate(examples):
    if example_cols[i].button(ex):
        st.session_state["topic_example"] = ex

# ------------------ INPUT UI ------------------
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input(
        "📌 Enter Topic",
        value=st.session_state.get("topic_example", "")
    )

with col2:
    level = st.selectbox(
        "🎯 Select Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

tone = st.selectbox(
    "🗣️ Explanation Style",
    ["Simple Teacher", "Technical", "Interview Prep"]
)

# ================== GENERATE ==================
if st.button("🚀 Explain Topic"):

    if topic.strip() == "":
        st.warning("Please enter a topic")
        st.stop()

    st.markdown("---")
    st.markdown("## 📘 AI Explanation")

    # Glass card start
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    with st.status("🧠 AI is thinking...", expanded=False):

        prompt = f"""
You are an expert teacher.

Topic: {topic}
Level: {level}
Style: {tone}

Provide structured output:

### Explanation
(simple and clear)

### Real-Life Example

### Key Points (bullets)

### When to Use

Keep it concise and well formatted.
"""

        # -------- STREAMING RESPONSE --------
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.4,
            max_tokens=800,
            stream=True,
        )

        result = ""
        placeholder = st.empty()

        for chunk in stream:
            if chunk.choices[0].delta.content:
                result += chunk.choices[0].delta.content
                placeholder.markdown(result + "▌")

        placeholder.markdown(result)

    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ COPY BOX ------------------
    st.markdown("### 📋 Copy Explanation")
    st.text_area("", result, height=220)

    # ------------------ DOWNLOAD ------------------
    st.download_button(
        label="📥 Download Notes",
        data=result,
        file_name=f"{topic}_notes.txt",
        mime="text/plain"
    )

# ------------------ FOOTER ------------------
st.markdown(
    """
    ---
    ⭐ Loved by students & developers  
    🔥 Built by Gaurav Bisht
    """
)