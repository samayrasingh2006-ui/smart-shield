import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(
    page_title="FAKE SHIELD",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_resource
def load_news_model():
    model_path = Path(__file__).parent / "news_model.joblib"
    return joblib.load(model_path)


try:
    news_model = load_news_model()
except Exception as e:
    news_model = None
    st.error(f"Could not load the news model: {e}")


# Navigation
st.sidebar.title("🛡️ FAKE SHIELD")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Scam Detector",
        "Fake News Detector",
        "How It Works",
        "About"
    ]
)


# HOME PAGE
if page == "Home":
    st.title("🛡️ FAKE SHIELD")
    st.subheader("Your Digital Safety Companion")

    st.write(
        "Identify suspicious messages and analyze news "
        "with our fake news and scam detection prototype."
    )

    st.divider()
    st.markdown("### Protect Yourself Online")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Scam Detection")
        st.write(
            "Check suspicious messages for common scam "
            "warning signs and review their risk score."
        )

    with col2:
        st.markdown("### 📰 Fake News Detection")
        st.write(
            "Use a trained machine-learning model to "
            "classify news text as fake or real."
        )

    st.info(
        "Choose a detector from the sidebar to get started."
    )

    st.caption(
        "Student prototype: results are not a guarantee "
        "of safety or factual accuracy."
    )


# SCAM DETECTOR PAGE
elif page == "Scam Detector":
    st.title("🔍 Scam Detector")
    st.write(
        "Enter a suspicious message to check for common "
        "scam warning signs."
    )

    user_text = st.text_area(
        "Enter suspicious message:",
        placeholder="Paste the message here...",
        key="scam_text"
    )

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

    if st.button("Analyze Scam Risk"):
        if not user_text.strip():
            st.warning("Please enter a message first.")
        else:
            text = user_text.lower()
            found_signs = []
            score = 0

            for name, details in warning_signs.items():
                if any(
                    word in text
                    for word in details["words"]
                ):
                    found_signs.append(name)
                    score += details["weight"]

            score = min(score, 100)

            if score > 87:
                risk = "HIGH RISK"
                color = "🔴"
            elif score >= 60:
                risk = "MEDIUM RISK"
                color = "🟠"
            else:
                risk = "LOW RISK"
                color = "🟢"

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
                    "This does not guarantee the message is safe."
                )

            st.caption(
                "This score is based on keyword rules. "
                "It is not a trained AI prediction or a "
                "verified probability."
            )


# FAKE NEWS DETECTOR PAGE
elif page == "Fake News Detector":
    st.title("📰 Fake News Detector")
    st.write(
        "Enter a news article or news text for "
        "classification by the trained model."
    )

    news_text = st.text_area(
        "Enter news text:",
        placeholder="Paste the news article here...",
        key="news_text"
    )

    if st.button("Analyze News"):
        if not news_text.strip():
            st.warning("Please enter news text first.")

        elif news_model is None:
            st.error(
                "The news model could not be loaded. "
                "Check that news_model.joblib exists."
            )

        else:
            try:
                prediction = news_model.predict([news_text])[0]

                st.divider()
                st.subheader("Prediction Result")

                if prediction == 1:
                    st.error("⚠️ FAKE NEWS predicted by the model")
                else:
                    st.success("✅ REAL NEWS predicted by the model")

                st.caption(
                    "This is a model prediction, not a verified "
                    "fact-check. Always check reliable sources."
                )

            except Exception as e:
                st.warning(f"Could not analyze news: {e}")


# HOW IT WORKS PAGE
elif page == "How It Works":
    st.title("⚙️ How FAKE SHIELD Works")

    st.markdown("### 1. Scam Detection")
    st.write(
        "The application checks the entered message for "
        "configured warning keywords. Each matching warning "
        "category contributes to a risk score."
    )

    st.markdown("### 2. Risk Classification")
    st.write(
        "- Below 60%: Low Risk\n"
        "- 60% to 87%: Medium Risk\n"
        "- Above 87%: High Risk"
    )

    st.markdown("### 3. Fake News Detection")
    st.write(
        "A trained machine-learning model analyzes the "
        "submitted text and predicts whether it belongs "
        "to the fake or real class."
    )

    st.markdown("### 4. Review the Results")
    st.write(
        "Users should treat the results as an initial screening "
        "and independently verify suspicious messages and news."
    )

    st.warning(
        "The scam score is rule-based. It is not a verified "
        "probability that a message is fraudulent."
    )


# ABOUT PAGE
elif page == "About":
    st.title("🛡️ About FAKE SHIELD")

    st.write(
        "FAKE SHIELD is a college mini-project that demonstrates "
        "scam warning detection and fake news classification."
    )

    st.markdown("### Technologies Used")
    st.write(
        "- Python\n"
        "- Streamlit\n"
        "- Joblib\n"
        "- Machine learning for news classification\n"
        "- Rule-based scam risk scoring"
    )

    st.markdown("### Project Objectives")
    st.write(
        "- Identify common warning signs in suspicious messages.\n"
        "- Display a risk score and risk category.\n"
        "- Classify news text using a trained model.\n"
        "- Encourage users to verify information before trusting it."
    )

    st.caption(
        "FAKE SHIELD is an educational prototype and may "
        "produce incorrect results."
    )
