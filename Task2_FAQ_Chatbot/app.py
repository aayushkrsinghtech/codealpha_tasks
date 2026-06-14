import streamlit as st
import pandas as pd
import nltk
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources
nltk.download('punkt', quiet=True)

# Page Config
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

h1 {
    text-align:center;
    color:#38bdf8;
}

.chat-box {
    padding:15px;
    border-radius:12px;
    background:#1e293b;
    color:white;
    margin-top:10px;
}

.answer-box {
    padding:15px;
    border-radius:12px;
    background:#0f766e;
    color:white;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI FAQ Chatbot")

st.write("Ask a question from the FAQ dataset and get the best matching answer.")

# Load FAQ data
faq_df = pd.read_csv("faq.csv")

# Preprocessing
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text

faq_df["processed"] = faq_df["question"].apply(preprocess)

# TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(faq_df["processed"])

# User Input
user_question = st.text_input("Enter your question")

if st.button("Get Answer"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:

        processed_query = preprocess(user_question)

        query_vector = vectorizer.transform([processed_query])

        similarity_scores = cosine_similarity(
            query_vector,
            tfidf_matrix
        )

        best_match_index = similarity_scores.argmax()

        confidence = similarity_scores[0][best_match_index]

        if confidence > 0.20:

            answer = faq_df.iloc[best_match_index]["answer"]

            st.markdown(
                f"""
                <div class="chat-box">
                <b>You:</b><br>{user_question}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="answer-box">
                <b>Bot:</b><br>{answer}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success(
                f"Confidence Score: {confidence:.2f}"
            )

        else:
            st.error(
                "No suitable answer found in FAQ database."
            )

# Dataset Preview
with st.expander("View FAQ Dataset"):
    st.dataframe(
        faq_df[["question", "answer"]],
        use_container_width=True
    )