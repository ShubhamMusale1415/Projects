import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb

# 🔹 Load model
model = load_model("my_model.keras")

# 🔹 Load word index
word_index = imdb.get_word_index()

# 🔹 Function to preprocess input
def preprocess_text(text):
    words = text.lower().split()
    encoded = []

    for word in words:
        if word in word_index:
            encoded.append(word_index[word] + 3)  # offset like IMDB dataset
        else:
            encoded.append(2)  # unknown word

    padded = pad_sequences([encoded], maxlen=50, padding='post')
    return padded.reshape(1, 50, 1)


# 🔹 Streamlit UI
st.title("🎬 Movie Review Sentiment Analyzer")

user_input = st.text_input("Enter a review (max 50 words):")

if st.button("Predict"):
    if user_input:
        processed = preprocess_text(user_input)
        pred = model.predict(processed)

        if pred[0][0] > 0.5:
            st.success("😊 Positive Review")
        else:
            st.error("😞 Negative Review")
    else:
        st.warning("Please enter a review")