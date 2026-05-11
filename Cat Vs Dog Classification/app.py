import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.title("Cat vs Dog Classifier 🐱🐶")

# Load trained model
model = tf.keras.models.load_model("model.h5")

uploaded_file = st.file_uploader("Upload an image", type=["jpg","png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = image.resize((256,256))
    st.image(img)
    img_array = np.expand_dims(np.array(img)/255.0, axis=0)

    prediction = model.predict(img_array)

    if prediction[0][0] > 0.5:
        st.write("🐶 Dog")
    else:
        st.write("🐱 Cat")