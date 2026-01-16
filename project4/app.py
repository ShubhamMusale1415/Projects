# import streamlit as st
# from evaluator import evaluate_text, get_domain_list
# from extractor import extract_text_from_pdf
# from utils import detect_title
#
# st.set_page_config(page_title="UPSC Essay Evaluator", layout="wide")
# st.title("📄 UPSC Essay Evaluator (ML Powered)")
#
# st.markdown("Upload your essay PDF and evaluate using Machine Learning + NLP.")
#
# domain = st.selectbox("Choose essay domain (optional)", options=get_domain_list())
# uploaded_file = st.file_uploader("Upload your essay PDF", type=["pdf"])
#
# if uploaded_file:
#     text = extract_text_from_pdf(uploaded_file)
#
#     if not text.strip():
#         st.error("No text extracted from PDF.")
#     else:
#         title = detect_title(text)
#         st.success(f"Detected Title: **{title}**")
#
#         with st.expander("Preview Extracted Text"):
#             st.text_area("", text, height=250)
#
#         if st.button("🚀 Evaluate"):
#             with st.spinner("Evaluating..."):
#                 results = evaluate_text(text, domain)
#
#             st.subheader("🎯 Final Score")
#             st.progress(int(results["aggregate_score"]))
#             st.write(f"### ⭐ {results['aggregate_score']:.1f} / 100")
#
#             st.write("🤖 **ML Predicted Domain:**", results["predicted_domain"])
#             st.write("📈 **ML Predicted Score:**", f"{results['ml_score']:.1f}")
#
#             st.divider()
#
#             st.subheader("📊 Rule Based Metrics")
#             col1, col2 = st.columns(2)
#
#             with col1:
#                 st.metric("Relevance", f"{results['relevance']*100:.1f}%")
#                 st.metric("Grammar", f"{results['grammar']*100:.1f}%")
#                 st.metric("Readability", f"{results['readability']*100:.1f}%")
#
#             with col2:
#                 st.metric("Coherence", f"{results['coherence']*100:.1f}%")
#                 st.metric("Length Score", f"{results['length_score']*100:.1f}%")
#                 st.metric("Keyword Coverage", f"{results['keyword_coverage']*100:.1f}%")
#
#             st.subheader("🛠 Suggestions")
#             for s in results["suggestions"]:
#                 st.write("•", s)



import streamlit as st
from evaluator import evaluate_text, get_domain_list
from extractor import extract_text
from utils import detect_title

st.set_page_config(page_title="UPSC Essay Evaluator", layout="wide")
st.title("📄 UPSC Essay Evaluator (PDF + Image + ML)")

st.markdown("Upload your essay as **PDF or Image (PNG/JPG/JPEG)**.")

domain = st.selectbox("Choose essay domain (optional)", options=get_domain_list())

uploaded_file = st.file_uploader(
    "Upload your file",
    type=["pdf", "png", "jpg", "jpeg", "webp"]
)

if uploaded_file:
    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("❌ No text detected. Try clearer image or text-based PDF.")
    else:
        title = detect_title(text)
        st.success(f"Detected Title: **{title}**")

        with st.expander("📄 Preview Extracted Text"):
            st.text_area("", text, height=250)

        if st.button("🚀 Evaluate"):
            with st.spinner("Evaluating..."):
                results = evaluate_text(text, domain)

            st.subheader("🎯 Final Score")
            st.progress(int(results["aggregate_score"]))
            st.write(f"### ⭐ {results['aggregate_score']:.1f} / 100")

            st.write("🤖 **ML Predicted Domain:**", results["predicted_domain"])
            st.write("📈 **ML Predicted Score:**", f"{results['ml_score']:.1f}")

            st.divider()

            st.subheader("📊 Rule Based Metrics")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Relevance", f"{results['relevance']*100:.1f}%")
                st.metric("Grammar", f"{results['grammar']*100:.1f}%")
                st.metric("Readability", f"{results['readability']*100:.1f}%")

            with col2:
                st.metric("Coherence", f"{results['coherence']*100:.1f}%")
                st.metric("Length Score", f"{results['length_score']*100:.1f}%")
                st.metric("Keyword Coverage", f"{results['keyword_coverage']*100:.1f}%")

            st.subheader("🛠 Suggestions")
            for s in results["suggestions"]:
                st.write("•", s)
