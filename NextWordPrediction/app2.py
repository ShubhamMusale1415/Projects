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

    # Create reverse mapping (FAST lookup)
    index_word = {index: word for word, index in tokenizer.word_index.items()}

    return model, tokenizer, index_word


model, tokenizer, index_word = load_all()



# -------------------------
# Prediction Function
# -------------------------
def predict_next_words(seed_text, next_words, temperature=1.0):
    seed_text = seed_text.lower().strip()

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]

        # Padding
        token_list = pad_sequences([token_list], maxlen=11, padding='pre')

        # Get probabilities
        preds = model.predict(token_list, verbose=0)[0]

        # Temperature sampling (avoid repetition)
        preds = np.log(preds + 1e-8) / temperature
        preds = np.exp(preds) / np.sum(np.exp(preds))

        predicted_index = np.random.choice(len(preds), p=preds)

        # Get word
        output_word = index_word.get(predicted_index, "")

        # Stop if invalid
        if output_word == "":
            break

        seed_text += " " + output_word

        # Stop at punctuation
        if output_word in [".", "!", "?"]:
            break

    return seed_text


# -------------------------
# Streamlit UI
# -------------------------
st.title("Next Word Prediction (LSTM)")

input_text = st.text_input("Enter your sentence:")
num_words = st.number_input("How many words to predict?", min_value=1, max_value=15, value=3)
temperature = st.slider("Creativity (temperature)", 0.5, 1.5, 1.0)

if st.button("Predict"):
    if input_text.strip() == "":
        st.warning("Please enter some text!")
    else:
        result = predict_next_words(input_text, num_words, temperature)
        st.success(f"Predicted Sentence:\n\n{result}")