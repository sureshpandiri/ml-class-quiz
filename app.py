import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --------------------------------------------------------------------------
# 🏢 STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------------------------------
st.set_page_config(page_title="Data Science Quiz Portal", page_icon="🎓", layout="centered")

st.title("🎯 Data Science & Machine Learning Quiz Portal")
st.write("Enter your profile details below, complete the mini-quiz, and submit your scores directly to the cloud.")

# --------------------------------------------------------------------------
# 🔐 GOOGLE SHEETS CLOUD CONNECTION SETUP
# --------------------------------------------------------------------------
@st.cache_resource
def get_sheets_client():
    # Streamlit securely stores your Google credentials in its dashboard secrets
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    secret_creds = dict(st.secrets["gcp_service_account"])
    credentials = Credentials.from_service_account_info(secret_creds, scopes=scopes)
    return gspread.authorize(credentials)

try:
    gc = get_sheets_client()
    # Replace with your actual Google Sheet name or exact sheet URL
    sheet = gc.open("Classroom_ML_Quiz_Grades").get_worksheet(0)
except Exception as e:
    st.error("🚨 Cloud connection database setup incomplete. Please configure Streamlit Secrets.")
    sheet = None

# --------------------------------------------------------------------------
# 👤 PHASE 1: STUDENT PROFILE FORM
# --------------------------------------------------------------------------
st.subheader("👤 Student Profile")
col1, col2 = st.columns(2)

with col1:
    roll_no = st.text_input("Roll Number", placeholder="e.g., 26CSE01").strip().upper()
    name = st.text_input("Full Name", placeholder="e.g., Alex Rivera").strip()

with col2:
    year = st.selectbox("Academic Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
    college = st.text_input("College Name", placeholder="e.g., IIT, VIT, NIT").strip()

# --------------------------------------------------------------------------
# 📝 PHASE 2: THE LIVE MINI-QUIZ
# --------------------------------------------------------------------------
st.markdown("---")
st.subheader("📝 Machine Learning Quick Check")

# Question 1
q1_input = st.radio(
    "1. Which step explicitly handles filtering data static, structural anomalies, and missing values?",
    ["Data Collection", "Data Cleaning", "Feature Extraction", "Model Testing"],
    index=None
)

# Question 2
q2_input = st.radio(
    "2. Is a standard, raw digital image pixel grid matrix considered structured or unstructured data?",
    ["Structured Data", "Unstructured Data"],
    index=None
)

# --------------------------------------------------------------------------
# 🚀 PHASE 3: SUBMISSION ENGINE
# --------------------------------------------------------------------------
st.markdown("---")

if st.button("🚀 Submit Quiz Answers", type="primary"):
    # Validation check
    if not roll_no or not name or not college:
        st.warning("⚠️ Submission blocked: Please completely fill out your Student Profile information.")
    elif q1_input is None or q2_input is None:
        st.warning("⚠️ Submission blocked: Please answer all the quiz questions before submitting.")
    else:
        # Calculate evaluation score
        score = 0
        if q1_input == "Data Cleaning": score += 50
        if q2_input == "Unstructured Data": score += 50
        
        # Display feedback to student
        st.success(f"🏁 Quiz Completed, {name}! You scored: **{score}/100**")
        
        # Append row to Google Sheets
        if sheet:
            with st.spinner("💾 Syncing your marks securely to the teacher dashboard..."):
                try:
                    row_data = [roll_no, name, year, college, score]
                    sheet.append_row(row_data)
                    st.balloons()
                    st.info("✅ Your score has been written to the master class spreadsheet successfully!")
                except Exception as e:
                    st.error(f"❌ Cloud database write failed. Error details: {e}")