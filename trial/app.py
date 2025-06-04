import streamlit as st
from datetime import date, datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# ---------------- Google Sheets Setup ----------------
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(
    r"F:\College\Placements\maintenance-log-report\trial\credentials.json",
    scopes=scopes
)
client = gspread.authorize(creds)

sheet_id = "1PJeDjik5m6m9twgUP9n9SCgMrLiH4Se3UvyFzFvLd7A"
sheet = client.open_by_key(sheet_id).sheet1

# ---------------- Department - Machine Mapping ----------------
department_machines = {
    "Production": ["Lathe", "Drill", "CNC-1", "CNC-2"],
    "Maintenance": ["Compressor", "Pump-1", "Pump-2", "Welding Machine"],
    "Quality": ["Spectrometer", "Measuring Station"],
    "R&D": ["Prototype Bench", "Microcontroller Lab Setup"],
    "Logistics": ["Conveyor A", "Conveyor B", "Pallet Jack"]
}

# ---------------- Streamlit UI ----------------
st.header("__Maintenance Log Reporting App__")

d = date.today()
shift = st.selectbox("Enter the shift Number:", ["Shift 1", "Shift 2", "Shift 3", "General Shift"])
request = st.text_input("Maintenance requested by:")

# Select department
dept = st.selectbox("Enter the department name:", list(department_machines.keys()))

# Machine name dropdown depends on department
machine_options = department_machines.get(dept, [])
machine_name = st.selectbox("Select the Machine name:", machine_options)

maintenance_type = st.selectbox("Select the maintenance type:", ['Breakdown', 'Preventive', 'Routine'])
nature_of_complaint = st.text_input("Enter the nature of complaint:")
start_time = st.time_input("Start Time:")
end_time = st.time_input("End time:", step=600)

# Calculate duration
start_dt = datetime.combine(date.min, start_time)
end_dt = datetime.combine(date.min, end_time)
if end_dt < start_dt:
    end_dt += timedelta(days=1)
duration = end_dt - start_dt
work_minutes = round(duration.total_seconds() / 60, 2)

st.write(f"Duration: {duration}")
st.write(f"Work minutes: {work_minutes}")

# Submit and append to Google Sheets
if st.button("Submit"):
    row = [
        d.strftime("%Y-%m-%d"), shift, request, dept, machine_name,
        maintenance_type, nature_of_complaint,
        start_time.strftime("%H:%M"), end_time.strftime("%H:%M"),
        work_minutes
    ]
    sheet.append_row(row)
    st.success("Data successfully appended to Google Sheets!")
