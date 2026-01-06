import streamlit as st
from evaluator import evaluate_text, get_domain_list
from extractor import extract_text_from_pdf
from utils import detect_title

from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

import requests
import matplotlib.pyplot as plt
# install below dependencies
# pip install streamlit-lottie streamlit-extras requests matplotlib
# ----------------- Helpers -----------------

def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None


hero_anim = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"
)
loading_anim = load_lottie(
    "https://assets2.lottiefiles.com/packages/lf20_ydo1amjm.json"
)
idea_anim = load_lottie(
    "https://assets6.lottiefiles.com/packages/lf20_puciaact.json"
)

# ----------------- PAGE CONFIG -----------------

st.set_page_config(
    page_title="UPSC Essay Evaluator",
    page_icon="📝",
    layout="wide",
)


# ----------------- HEADER -----------------

left, right = st.columns([1.6, 1])

with left:
    st.title("📄 UPSC Essay Evaluator")
    st.write(
        "Analyze your UPSC essay with structured feedback, scores, "
        "and smart improvement suggestions."
    )

with right:
    if hero_anim:
        st_lottie(hero_anim, height=220)


st.markdown("---")

# ----------------- Upload + Domain -----------------

st.subheader("✨ Start Evaluation")

domain = st.selectbox("Choose essay domain", options=get_domain_list())
uploaded_file = st.file_uploader("Upload your essay PDF", type=["pdf"])


# ----------------- Processing -----------------

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    if not text.strip():
        st.error("⚠ No text extracted. Try another PDF.")
    else:
        title = detect_title(text)
        st.success(f"📌 Detected title: **{title}**")

        with st.expander("👁 Preview extracted text"):
            st.text_area("", text, height=260)

        if st.button("🚀 Evaluate my essay", use_container_width=True):

            with st.spinner("Analyzing…"):
                if loading_anim:
                    st_lottie(loading_anim, height=120)

                results = evaluate_text(text, domain)

            st.success("🎯 Evaluation complete!")
            st.balloons()

            # ---------- TABS ----------
            tab_overall, tab_metrics, tab_diagnostics, tab_suggestions = st.tabs(
                ["📊 Overview", "📈 Metrics", "🛠 Diagnostics", "💡 Suggestions"]
            )

            # ---------- OVERVIEW ----------
            with tab_overall:
                st.subheader("Overall Score")

                st.progress(int(results["aggregate_score"]))
                st.markdown(
                    f"""
                    <h1 style="text-align:center;">
                        ⭐ {results['aggregate_score']:.1f} / 100
                    </h1>
                    """,
                    unsafe_allow_html=True,
                )

                add_vertical_space(1)

                if idea_anim:
                    st_lottie(idea_anim, height=160)

            # ---------- METRICS ----------
            with tab_metrics:
                st.subheader("Detailed Metrics")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Relevance", f"{results['relevance']*100:.1f}%")
                    st.metric("Grammar & Spelling", f"{results['grammar']*100:.1f}%")
                    st.metric("Readability", f"{results['readability']*100:.1f}%")

                with col2:
                    st.metric("Coherence", f"{results['coherence']*100:.1f}%")
                    st.metric("Length Score", f"{results['length_score']*100:.1f}%")
                    st.metric("Keyword Coverage", f"{results['keyword_coverage']*100:.1f}%")

                style_metric_cards()

                st.write("---")
                st.write("### Score breakdown chart")

                labels = [
                    "Relevance",
                    "Grammar",
                    "Readability",
                    "Coherence",
                    "Length",
                    "Keywords",
                ]

                values = [
                    results["relevance"],
                    results["grammar"],
                    results["readability"],
                    results["coherence"],
                    results["length_score"],
                    results["keyword_coverage"],
                ]

                fig, ax = plt.subplots()
                ax.bar(labels, values)
                ax.set_ylim(0, 1)
                ax.set_ylabel("Score (0–1)")
                ax.set_title("Performance Overview")

                st.pyplot(fig)

            # ---------- DIAGNOSTICS ----------
            with tab_diagnostics:
                st.subheader("Top Misspelled Words")

                if results["misspelled"]:
                    for w, s in results["misspelled"][:15]:
                        st.write(f"- **{w}** → {s}")
                else:
                    st.write("✅ No obvious spelling problems.")

                st.write("### Domain keywords detected")
                st.write(", ".join(results["matched_keywords"][:30]))

            # ---------- SUGGESTIONS ----------
            with tab_suggestions:
                st.subheader("Actionable Suggestions")

                for sug in results["suggestions"]:
                    st.info(f"💡 {sug}")

                st.toast("Evaluation finished ✔", icon="🚀")
