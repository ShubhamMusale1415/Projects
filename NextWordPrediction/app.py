import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# -------------------------
# Load Model & Tokenizer
# -------------------------
@st.cache_resource
def load_all():
    model = load_model("new_model.keras")

    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    return model, tokenizer


model, tokenizer = load_all()



# -------------------------
# Prediction Function
# -------------------------
def predict_next_words(seed_text, next_words):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=11, padding='pre')

        predicted = np.argmax(model.predict(token_list, verbose=0), axis=-1)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break

        seed_text += " " + output_word

    return seed_text


# -------------------------
# Streamlit UI
# -------------------------
st.title("Next Word Prediction (LSTM)")

input_text = st.text_input("Enter your sentence:")
num_words = st.number_input("How many words to predict?", min_value=1, max_value=20, value=3)

if st.button("Predict"):
    if input_text.strip() == "":
        st.warning("Please enter some text!")
    else:
        result = predict_next_words(input_text, num_words)
        st.success(f"Predicted Sentence:\n\n{result}")

