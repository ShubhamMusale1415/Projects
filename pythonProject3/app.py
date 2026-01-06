import streamlit as st
from evaluator import evaluate_text, get_domain_list
from extractor import extract_text_from_pdf
from utils import detect_title

st.title("📄 UPSC Essay Evaluator")

st.markdown("Select the domain your essay belongs to, upload the PDF, then press Evaluate.")

domain = st.selectbox("Choose essay domain", options=get_domain_list())

uploaded_file = st.file_uploader("Upload your essay PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    if not text.strip():
        st.error("No text extracted from PDF. Try another PDF or use a text-based PDF.")
    else:
        title = detect_title(text)
        st.info(f"Detected title (first non-empty line): **{title}**")

        with st.expander("Preview extracted text"):
            st.text_area("Extracted text", text, height=300)

        if st.button("Evaluate"):
            with st.spinner("Evaluating..."):
                results = evaluate_text(text, domain)

            # Summary
            st.subheader("Overall Score")
            st.progress(int(results['aggregate_score']))
            st.write(f"**Aggregate score:** {results['aggregate_score']:.1f} / 100")

            # Detailed metrics
            st.subheader("Detailed Metrics")
            cols = st.columns(2)
            with cols[0]:
                st.metric("Relevance", f"{results['relevance']*100:.1f}%")
                st.metric("Grammar/Spelling", f"{results['grammar']*100:.1f}%")
                st.metric("Readability", f"{results['readability']*100:.1f}%")
            with cols[1]:
                st.metric("Coherence", f"{results['coherence']*100:.1f}%")
                st.metric("Length score", f"{results['length_score']*100:.1f}%")
                st.metric("Keyword coverage", f"{results['keyword_coverage']*100:.1f}%")

            st.subheader("Diagnostics & Suggestions")
            st.write("**Top misspelled words (with suggestions):**")
            if results['misspelled']:
                for w, s in results['misspelled'][:15]:
                    st.write(f"- {w} → {s}")
            else:
                st.write("No obvious misspellings found.")

            st.write("**Top domain keywords found:**")
            st.write(", ".join(results['matched_keywords'][:30]))

            st.write("**Short suggestions:**")
            for sug in results['suggestions']:
                st.write(f"- {sug}")