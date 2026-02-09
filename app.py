import streamlit as st
import pandas as pd
import altair as alt

from ocr.ocr_engine import extract_text
from parser.lab_parser import parse_lab_values
from analysis.abnormal_detector import detect_abnormal
from explanation.term_explainer import explain_term
from utils.pdf_generator import generate_pdf
from utils.file_handler import save_uploaded_file
from analysis.confidence_score import get_confidence_message

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Medical Report Analyzer",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

/* Card base */
.card {
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 16px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
}

/* Text colors (force visibility) */
.card .test-name {
    font-size: 18px;
    font-weight: 600;
    color: #111827;
}

.card .value {
    font-size: 22px;
    font-weight: bold;
    color: #111827;
}

.card .range {
    font-size: 14px;
    color: #374151;
}

.card .status {
    font-size: 14px;
    color: #374151;
}

.card .status b {
    color: #111827;
}

/* Status backgrounds */
.normal {
    background-color: #e6f4ea;
    border-left: 6px solid #22c55e;
}

.low {
    background-color: #fff4e5;
    border-left: 6px solid #f59e0b;
}

.high {
    background-color: #fdecea;
    border-left: 6px solid #ef4444;
}

/* Explanation box */
details summary {
    cursor: pointer;
    color: #2563eb;
    font-weight: 500;
}

details p {
    margin-top: 8px;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🩺 AI-Powered Medical Report Analyzer")
st.caption(
    "Understand your lab reports in simple language. "
    "This tool provides explanations only and does **not** replace medical advice."
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Patient Details")

gender = st.sidebar.selectbox("Gender", ["male", "female"])
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)

uploaded_file = st.sidebar.file_uploader(
    "Upload Medical Report",
    type=["png", "jpg", "jpeg"]
)

# ---------------- MAIN CONTENT ----------------
if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)

    with st.spinner("Analyzing medical report..."):
        text, confidence = extract_text(file_path)
        labs = parse_lab_values(text)
        results = detect_abnormal(labs, gender=gender)

    # ---------------- CHART DATA ----------------
    chart_data = pd.DataFrame([
        {
            "Test": r["test"],
            "Value": r["value"],
            "Status": r["status"]
        }
        for r in results
    ])


    st.success(f"OCR confidence: {round(confidence * 100, 1)}%")
    confidence_msg = get_confidence_message(confidence)
    if confidence_msg:
        st.warning(confidence_msg)


    # ---------------- KEY FINDINGS ----------------
    st.subheader("🔍 Key Findings")

    abnormal_found = False

    for r in results:
        status = r["status"].lower()

        if status in ["low", "high"]:
            abnormal_found = True
            st.markdown(f"""
            <div class="card {status}">
                <div class="test-name">{r["test"]}</div>
                <div class="value">{r["value"]}</div>
                <div class="range">Normal Range: {r["normal_range"]}</div>
                <div class="status">Status: <b>{r["status"]}</b></div>
                <details>
                  <summary>What does this mean?</summary>
                  <p>{explain_term(r["test"])}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)

    if not abnormal_found:
        st.info("✅ No abnormal values detected in this report.")


    st.subheader("📊 Visual Summary")

    chart = (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Test:N", sort=None,title="Test"),
            y=alt.Y("Value:Q",title="Value"),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(
                    domain=["Normal", "Low", "High"],
                    range=["#22c55e", "#f59e0b", "#ef4444"]
                )
            ),
            tooltip=["Test", "Value", "Status"]
        )
        .properties(height=300)
    )

    st.altair_chart(chart, use_container_width=True)

    # ---------------- COMPLETE REPORT ----------------
    st.subheader("📋 Complete Report")

    cols = st.columns(2)

    for i, r in enumerate(results):
        status = r["status"].lower()
        col = cols[i % 2]

        with col:
            st.markdown(f"""
            <div class="card {status}">
                <div class="test-name">{r["test"]}</div>
                <div class="value">{r["value"]}</div>
                <div class="range">Normal Range: {r["normal_range"]}</div>
                <div class="status">Status: <b>{r["status"]}</b></div>
                <details>
                  <summary>What does this mean?</summary>
                  <p>{explain_term(r["test"])}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- DOCTOR QUESTIONS ----------------
    st.subheader("🧠 Questions You May Ask Your Doctor")

    st.markdown("""
    - Are these abnormal values temporary or something to monitor?
    - Do I need a repeat test?
    - Could recent illness, stress, or lifestyle affect these results?
    - Should any value be monitored regularly?
    """)

    # ---------------- DISCLAIMER ----------------
    st.divider()
    st.warning(
        "⚠️ This application provides general explanations only. "
        "It does NOT diagnose conditions or suggest treatments. "
        "Always consult a qualified medical professional."
    )
    # ---------------- DOWNLOAD PDF ----------------
    st.subheader("⬇️ Download Report Summary")

    pdf_buffer = generate_pdf(results, confidence)

    st.download_button(
        label="Download PDF Summary",
        data=pdf_buffer,
        file_name="medical_report_summary.pdf",
        mime="application/pdf"
    )

else:
    st.info("⬅️ Upload a medical report from the sidebar to begin.")
