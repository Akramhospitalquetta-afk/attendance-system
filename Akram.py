import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Mobile screen optimization ke liye setup
st.set_page_config(
    page_title="Akram Hospital Attendance",
    page_icon="AKRAM LOG.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)


FILE_NAME = "hospital_attendance.csv"

# Hospital Header (Mobile ke mutabik chota aur wazeh)
st.markdown("<h2 style='text-align: center; color: #007bff; margin-bottom: 0;'>Akram Hospital</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Zargoon Road, Quetta</p>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-top: 10px;'>Online Attendance Portal</h4>", unsafe_allow_html=True)
st.write("---")

# Logo ko center mein lane ke liye
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("AKRAM LOG.png",
, use_container_width=True)


# Mobile Friendly Input Fields (Single Column layout)
name = st.text_input("👤 Apna Poora Naam Likhein:")
emp_id = st.text_input("🆔 Employee ID / Roll No:")
department = st.selectbox("🏥 Department Select Karein:", [
    "Emergency", "OPD", "ICU", "Pharmacy", "Laboratory", "Administration", "Other"
])

# Attendance Button (Mobile screen par poora fit aane ke liye styling)
st.markdown("""
<style>
div.stButton > button:first-child {
    width: 100%;
    background-color: #28a745;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

if st.button("Submit Attendance 📝"):
    if name and emp_id:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        
        new_data = {
            "Hospital": ["Akram Hospital"],
            "Location": ["Zargoon Road, Quetta"],
            "Name": [name],
            "ID/RollNo": [emp_id],
            "Department": [department],
            "Date": [current_date],
            "Time": [current_time]
        }
        df_new = pd.DataFrame(new_data)
        
        if os.path.exists(FILE_NAME):
            df_old = pd.read_csv(FILE_NAME)
            df_total = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_total = df_new
            
        df_total.to_csv(FILE_NAME, index=False)
        st.success(f"Shukriya {name}! Akram Hospital ke record mein aap ki attendance lag gayi hai.")
    else:
        st.error("Meharbani karke Naam aur ID dono lazmi likhein.")

# Attendance Sheet check karne ka section
st.write("---")
if st.checkbox("Show Today's Attendance Sheet"):
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        # Mobile screen par scrollable table dikhane ke liye
        st.dataframe(df)
    else:
        st.info("Abhi tak koi attendance record nahi hai.")
