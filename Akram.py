import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page Configurations (Monogram aur responsive design)
st.set_page_config(
    page_title="Akram Hospital Attendance", 
    page_icon="AKRAM LOG.png",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Files Names for Data Storage
STAFF_FILE = "hospital_staff_info.csv"
ATTENDANCE_FILE = "hospital_attendance.csv"

# Helper Functions for Data Handling
def load_staff_data():
    if os.path.exists(STAFF_FILE):
        return pd.read_csv(STAFF_FILE)
    return pd.DataFrame(columns=["EmployeeID", "Name", "JoiningDate", "Department", "DefaultShift"])

def save_staff_data(df):
    df.to_csv(STAFF_FILE, index=False)

def generate_unique_id(df):
    if len(df) == 0:
        return "AH-1001"
    last_id = df.iloc[-1]["EmployeeID"]
    try:
        last_num = int(last_id.split("-")[1])
    except:
        last_num = 1000
    return f"AH-{last_num + 1}"

# Hospital Header Layout
st.markdown("<h2 style='text-align: center; color: #007bff; margin-bottom: 0;'>Akram Hospital</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Zargoon Road, Quetta</p>", unsafe_allow_html=True)

# Logo Display
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("AKRAM LOG.png", use_container_width=True)

st.markdown("<h4 style='text-align: center; margin-top: 10px;'>Online Attendance Portal</h4>", unsafe_allow_html=True)

# Live Time Display Section
now = datetime.now()
current_date_str = now.strftime("%A, %d %B %Y")
current_time_str = now.strftime("%I:%M:%S %p")
st.markdown(f"""
<div style='background-color: #f8f9fa; border-left: 5px solid #007bff; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
    <p style='margin: 0; font-size: 14px; color: #555;'>📅 <b>Date:</b> {current_date_str}</p>
    <p style='margin: 0; font-size: 18px; color: #333;'>🕒 <b>Current Live Time:</b> <span style='color: #28a745; font-weight: bold;'>{current_time_str}</span></p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# Main Portal Tabs (Attendance vs Registration)
tab1, tab2 = st.tabs(["📝 Mark Attendance", "👤 Register New Staff"])
df_staff = load_staff_data()

# ----------------- TAB 2: REGISTER NEW STAFF -----------------
with tab2:
    st.subheader("Add New Hospital Employee")
    reg_name = st.text_input("Full Name:", key="reg_name").strip()
    reg_date = st.date_input("Joining Date:", datetime.today(), key="reg_date")
    
    departments_list = ["Emergency", "OPD", "ICU", "Pharmacy", "Laboratory", "Administration", "Nursing", "Other"]
    reg_dept = st.selectbox("Assign Department:", departments_list, key="reg_dept")
    
    shifts_list = [
        "Morning Shift (9:00 AM - 3:00 PM)",
        "Evening Shift (3:00 PM - 9:00 PM)",
        "Night Shift (9:00 PM - 9:00 AM)"
    ]
    reg_shift = st.selectbox("Select Regular Duty Timing:", shifts_list, key="reg_shift")
    
    if st.button("Generate ID & Register Employee", type="primary"):
        if reg_name:
            if len(df_staff) > 0 and reg_name.lower() in df_staff["Name"].str.lower().values:
                st.warning(f"Employee named '{reg_name}' is already registered.")
            else:
                new_id = generate_unique_id(df_staff)
                new_employee = {
                    "EmployeeID": [new_id],
                    "Name": [reg_name],
                    "JoiningDate": [reg_date.strftime("%Y-%m-%d")],
                    "Department": [reg_dept],
                    "DefaultShift": [reg_shift]
                }
                df_new_emp = pd.DataFrame(new_employee)
                df_staff = pd.concat([df_staff, df_new_emp], ignore_index=True)
                save_staff_data(df_staff)
                
                st.success(f"🎉 Success! {reg_name} registered successfully.")
                st.code(f"Assigned Employee ID: {new_id}", language="text")
                st.rerun()
        else:
            st.error("Please enter the staff member's full name.")

# ----------------- TAB 1: MARK ATTENDANCE -----------------
with tab1:
    st.subheader("Daily Attendance Check-In")
    
    if len(df_staff) == 0:
        st.info("No registered staff found. Please go to 'Register New Staff' tab first.")
    else:
        staff_names = sorted(df_staff["Name"].tolist())
        selected_name = st.selectbox("Select Your Name:", ["-- Choose Your Name --"] + staff_names)
        
        if selected_name != "-- Choose Your Name --":
            staff_row = df_staff[df_staff["Name"] == selected_name].iloc[0]
            auto_id = staff_row["EmployeeID"]
            auto_dept = staff_row["Department"]
            auto_shift = staff_row["DefaultShift"]
            
            st.info(f"🆔 **Employee ID:** {auto_id}   |   🏥 **Department:** {auto_dept}")
            
            final_shift = st.selectbox("Confirm Today's Shift/Timing:", shifts_list, index=shifts_list.index(auto_shift))
            
            if st.button("Submit My Attendance ✅"):
                current_d = now.strftime("%Y-%m-%d")
                current_t = now.strftime("%I:%M:%S %p")
                
                attendance_record = {
                    "Hospital": ["Akram Hospital"],
                    "EmployeeID": [auto_id],
                    "Name": [selected_name],
                    "Department": [auto_dept],
                    "DutyTiming": [final_shift],
                    "Date": [current_d],
                    "Time": [current_t]
                }
                df_att_new = pd.DataFrame(attendance_record)
                
                if os.path.exists(ATTENDANCE_FILE):
                    df_att_old = pd.read_csv(ATTENDANCE_FILE)
                    df_att_total = pd.concat([df_att_old, df_att_new], ignore_index=True)
                else:
                    df_att_total = df_att_new
                    
                df_att_total.to_csv(ATTENDANCE_FILE, index=False)
                st.success(f"Thank you {selected_name}! Attendance marked at {current_t}.")

# ----------------- DATA SHEET DISPLAY SECTION -----------------
st.write("---")
show_sheets = st.checkbox("Show Records Dashboard")
if show_sheets:
    sheet_opt = st.radio("Select View:", ["Today's Attendance Sheet", "Registered Staff Directory"], horizontal=True)
    
    if sheet_opt == "Today's Attendance Sheet":
        if os.path.exists(ATTENDANCE_FILE):
            df_att = pd.read_csv(ATTENDANCE_FILE)
            st.dataframe(df_att)
        else:
            st.info("No attendance records found for today yet.")
            
    elif sheet_opt == "Registered Staff Directory":
        if len(df_staff) > 0:
            st.dataframe(df_staff)
        else:
            st.info("No employees registered in the system yet.")
