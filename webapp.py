import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt
from io import BytesIO

# --- Config ---
key = "AIzaSyDKCSwh-y55gWT4aTSw4aZY-xzmAORJaQM"
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.set_page_config(
    page_title="Structural Defect Identifier 🏗",
    page_icon="🛠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("📂 Upload Section")
uploaded_image = st.sidebar.file_uploader("Upload a structure image", type=["jpeg", "jpg", "png"])
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

# --- Main Header ---
st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h1 style="color:#FF4B4B;">🏗 AI-Assisted Structural Defect Identifier</h1>
        <p style="font-size:18px; color:gray;">
            Upload an image of a structure and generate a detailed defect report instantly.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Instructions ---
with st.expander("📘 How to use this app"):
    st.markdown(
        """
        1. *Upload an image* of the structure from the sidebar  
        2. Fill in the *report details* (title, prepared by, prepared for)  
        3. Click *Generate Report*  
        4. Review your report and *download it* if needed  
        """
    )

# --- Report Inputs ---
rep_title = st.text_input("📑 Report Title", "")
prep_by = st.text_input("👷 Report Prepared by", "")
prep_for = st.text_input("🏢 Report Prepared for", "")

# --- Prompt Builder ---
prompt = f"""
Assume you are a structural engineer. The user has provided an image of a structure. 
You need to identify the structural defects in the image and generate a report.

The report must contain:
- Title: {rep_title}
- Prepared by: {prep_by}
- Prepared for: {prep_for}
- Date: {dt.datetime.now().date()}

Instructions:
* Identify and classify each defect (crack, spalling, corrosion, honeycombing, etc.)
* Provide a description and potential impact of each defect
* Rate severity (Low / Medium / High)
* Estimate time before permanent damage
* Suggest short-term and long-term solutions with estimated *costs (₹)* and time
* Provide preventive measures
* Use bullet points and tables where possible
* Keep report ≤ 3 pages
"""

# --- Report Generation ---
if st.button("🚀 Generate Report"):
    if uploaded_image is None:
        st.error("⚠ Please upload an image first.")
    else:
        with st.spinner("⏳ Analyzing image and preparing report..."):
            response = model.generate_content([prompt, Image.open(uploaded_image)])
            report_text = response.text

        st.success("✅ Report generated successfully!")
        st.balloons()

        # Show report nicely
        st.markdown("### 📄 Generated Report")
        st.write(report_text)

        # --- Download Option ---
        buffer = BytesIO()
        buffer.write(report_text.encode("utf-8"))
        buffer.seek(0)

        st.download_button(
            label="💾 Download Report",
            data=buffer,
            file_name=f"Structural_Report_{dt.datetime.now().date()}.txt",
            mime="text/plain",
            )