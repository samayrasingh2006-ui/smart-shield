import streamlit as st
import joblib
from pathlib import Path 

st.set_page_config(
    page_title="FAKE SHIELD",
    page_icon="🛡️",
    layout="centered"
)
@st.cache_resource
def load_news_model():
    model_path = Path(__file__).parent / "news_model.joblib"
    return joblib.load(model_path)

try:
    news_model = load_news_model()
except Exception as e:
    news_model = None
    st.error(f"Could not load the news model: {e}"
 )


st.title("🛡️ FAKE SHIELD")
st.subheader("AI-Based Fake News & Scam Detection")

st.write(
    "Check suspicious messages and identify "
    "potential warning signs."
)

user_text = st.text_area(
    "Enter news or a suspicious message:",
    placeholder="Paste your text here..."
)

# Demonstration warning signs and their weights
warning_signs = {
    "Urgent or pressuring language": {
        "words": [
            "urgent", "act now", "immediately",
            "limited time", "within 24 hours"
        ],
        "weight": 20
    },
    "Prize or lottery scam": {
        "words": [
            "you won", "have won", "winner",
            "prize", "lottery", "claim your reward"
        ],
        "weight": 25
    },
    "Request for sensitive information": {
        "words": [
            "password", "otp", "pin",
            "bank details", "verify your account"
        ],
        "weight": 30
    },
    "Threatening or pressuring claim": {
        "words": [
            "account blocked", "account suspended",
            "final warning", "legal action"
        ],
        "weight": 20
    }
}

if st.button("Analyze Text"):
    if not user_text.strip():
        st.warning("Please enter some text first.")

    else:
        text = user_text.lower()
        found_signs = []
        score = 0

        # Find warning signs in the entered text
        for name, details in warning_signs.items():
            if any(word in text for word in details["words"]):
                found_signs.append(name)
                score += details["weight"]

        # Keep score within 0–100
        score = min(score, 100)

        # Determine risk category
        if score > 87:
            risk = "HIGH RISK"
            color = "🔴"
        elif score >= 60:
            risk = "MEDIUM RISK"
            color = "🟠"
        else:
            risk = "LOW RISK"
            color = "🟢"

        # Display results
        st.divider()
        st.subheader("Analysis Results")

        st.metric("Risk Score", f"{score}%")
        st.progress(score / 100)

        st.markdown(f"## {color} {risk}")

        if found_signs:
            st.write("Warning signs detected:")
            for sign in found_signs:
                st.write(f"- ⚠️ {sign}")
        else:
            st.info(
                "No configured warning signs were detected. "
                "This does not guarantee the text is safe."
            )

        st.caption(
            "Prototype result based on keyword rules, "
            "not a trained AI model or verified probability."
        )
       # Fake News Model Prediction
if news_model is not None:
    st.subheader("Fake News Detection")

    try:
        prediction = news_model.predict([user_text])[0]

        if prediction == 1:
            st.error("⚠️ FAKE NEWS detected by the model")
        else:
            st.success("REAL NEWS predicted by the model")

        st.caption(
            "This is an automated model prediction, "
            "not a verified fact-check."
        )

    except Exception as e:
        st.warning(f"Could not analyze news: {e}")