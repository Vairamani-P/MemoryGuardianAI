import streamlit as st
import pandas as pd
import os
import pyttsx3
import datetime
import time
import datetime
import base64

def speak(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_sos_alarm():
    with open("alarm.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    audio_html = f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
def play_sos_alarm():
    file_path = os.path.join(os.getcwd(), "alarm.mp3")

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        b64 = base64.b64encode(data).decode()

        st.markdown(f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

    except Exception:
        st.error("⚠️ alarm.mp3 file not accessible")
from streamlit_autorefresh import st_autorefresh

from medicine_name import medicine_name

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

st.title("Memory Guardian AI")
if os.path.exists("patient_data.csv"):
    patient = pd.read_csv("patient_data.csv")

    st.subheader("Patient Summary")

    st.write("👤", patient.iloc[0]["Name"])
    st.write("🩸", patient.iloc[0]["Blood Group"])
    st.write("🏥", patient.iloc[0]["Condition"])

# ----------------------------
# FAMILY MEMBER REGISTRATION
# ----------------------------

st.header("Family Member Registration")

name = st.text_input("Enter Name")

relation = st.selectbox(
    "Select Relation",
    ["Daughter", "Son", "Wife", "Brother", "Sister", "Father", "Mother", "Granddaughter", "Grandson","Daughter-in-law"]
)

photo = st.file_uploader(
    "Upload Photo",
    type=["jpg", "jpeg", "png"]
)

if photo:
    st.image(photo, width=200)

if st.button("Save",key="save_btn"):

    if not name.strip():
        st.error("Please enter a name")

    else:

        photo_folder = os.path.join(os.getcwd(), "photos")
        os.makedirs(photo_folder, exist_ok=True)

        if photo:

            photo_path = os.path.join(
                photo_folder,
                f"{name}.jpg"
            )

            with open(photo_path, "wb") as f:
                f.write(photo.getbuffer())

        else:
            photo_path = ""

        new_data = pd.DataFrame({
            "Name": [name],
            "Relation": [relation],
            "Photo": [photo_path]
        })

        if os.path.exists("family_data.csv"):
            old_data = pd.read_csv("family_data.csv")
            data = pd.concat(
                [old_data, new_data],
                ignore_index=True
            )
        else:
            data = new_data

        data.to_csv(
            "family_data.csv",
            index=False
        )

        st.success(
            "Family Member Saved Successfully"
        )

# ----------------------------
# SHOW SAVED MEMBERS
# ----------------------------

if os.path.exists("family_data.csv"):

    st.subheader("Saved Family Members")

    data = pd.read_csv("family_data.csv")

    # Table Header
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### Name")

    with col2:
        st.markdown("### Relation")

    with col3:
        st.markdown("### Photo")

    st.divider()

    # Table Rows
    for index, row in data.iterrows():

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.write(row["Name"])

        with col2:
            st.write(row["Relation"])

        with col3:
            if pd.notna(row["Photo"]):

                if os.path.exists(str(row["Photo"])):

                    st.image(
                        str(row["Photo"]),
                        width=60
                    )

        st.divider()

# ----------------------------
# MEMORY RECALL
# ----------------------------

st.header("Memory Recall")

person_name = st.text_input("Enter Person Name")

if st.button("Who is this?"):

    if os.path.exists("family_data.csv"):

        data = pd.read_csv("family_data.csv")

        result = data[
            data["Name"].str.lower() == person_name.lower()
        ]

        if not result.empty:

            relation = result.iloc[0]["Relation"]

            message = f"{person_name} is your {relation}"

            st.success(message)

            speak(message)

        else:

            st.error("Person not found")
        st.header("Patient Information")

        patient_name = st.text_input("Patient Name")

        patient_age = st.number_input(
            "Age",
            min_value=1,
            max_value=120
)

        blood_group = st.selectbox(
          "Blood Group",
          ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
)

        medical_condition = st.text_input(
             "Medical Condition"
)

        emergency_contact = st.text_input(
            "Emergency Contact Number"
)           
        if st.button("Save Patient Details"):

           patient_data = pd.DataFrame({
               "Name":[patient_name],
                "Age":[patient_age],
                "Blood Group":[blood_group],
                "Condition":[medical_condition],
                "Contact":[emergency_contact]
    })

           patient_data.to_csv(
              "patient_data.csv",
               index=False
    )

           st.success(
              "Patient Details Saved Successfully"
    )
            
            ##MEDICINE REMINDER
         
        st.header("Medicine Reminder")

medicine_name = st.text_input(
    "Medicine Name",
    key="medicine_name"
)

medicine_time = st.time_input(
    "Medicine Time",
    key="medicine_time"
)
def speak(text):
    import pyttsx3
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
# -------------------------
# ADD REMINDER
# -------------------------
if st.button("Add Reminder", key="add_reminder"):

    new_reminder = pd.DataFrame({
        "Medicine": [medicine_name],
        "Time": [str(medicine_time)]
    })

    if os.path.exists("medicine_reminders.csv"):
        old = pd.read_csv("medicine_reminders.csv")
        reminders = pd.concat([old, new_reminder], ignore_index=True)
    else:
        reminders = new_reminder

    reminders.to_csv("medicine_reminders.csv", index=False)

    st.success("Medicine Reminder Added Successfully")


# -------------------------
# SESSION STATE
# -------------------------
if "spoken" not in st.session_state:
    st.session_state.spoken = {}


# -------------------------
# SHOW + CHECK
# -------------------------
st.subheader("Active Reminders")

if os.path.exists("medicine_reminders.csv"):

    reminder_data = pd.read_csv("medicine_reminders.csv")
    st.dataframe(reminder_data)

    current_time = datetime.datetime.now().strftime("%H:%M")

    for _, row in reminder_data.iterrows():

        reminder_time = str(row["Time"])[:5]

        if reminder_time == current_time:

            message = f"Time to take {row['Medicine']}"

            key = f"{row['Medicine']}_{reminder_time}"

            if not st.session_state.spoken.get(key, False):

                st.warning(message)
                
                speak(message)
                
                
                # ----------------------------
# PATIENT INFORMATION
# ----------------------------

st.header("Patient Information")

patient_name = st.text_input(
    "Patient Name",
    key="patient_name"
)

patient_age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    key="patient_age"
)

blood_group = st.selectbox(
    "Blood Group",
    ["A+","A-","B+","B-","AB+","AB-","O+","O-"],
    key="blood_group"
)

medical_condition = st.text_input(
    "Medical Condition",
    key="medical_condition"
)

emergency_contact = st.text_input(
    "Emergency Contact Number",
    key="emergency_contact"
)
patient_location = st.text_input(
    "Patient Location",
    key="patient_location"
)

if st.button("Save Patient Details", key="save_patient"):

    patient_data = pd.DataFrame({
    "Name":[patient_name],
    "Age":[patient_age],
    "Blood Group":[blood_group],
    "Condition":[medical_condition],
    "Contact":[emergency_contact],
    "Location":[patient_location]
})
    patient_data.to_csv(
        "patient_data.csv",
        index=False
    )

    st.success("Patient Details Saved Successfully")



if st.button("🔥 ACTIVATE SOS ALARM", key="sos_alarm"):

    st.error("🚨 EMERGENCY ALERT ACTIVATED!")
    st.warning("Sending emergency signal...")
    st.warning("🔊 SOS Alarm Activated")

    speak("Emergency alert activated. Help needed, Anyone Come fast")

    st.success("📧 Emergency Notification Sent")

    st.markdown(
        "<h1 style='color:red;text-align:center;'>HELP NEEDED !!!</h1>",
        unsafe_allow_html=True
    )
    if os.path.exists("patient_data.csv"):

       patient = pd.read_csv("patient_data.csv")

    st.subheader("Patient Emergency Information")

    st.write("👤 Name:", patient.iloc[0]["Name"])
    st.write("🎂 Age:", patient.iloc[0]["Age"])
    st.write("🩸 Blood Group:", patient.iloc[0]["Blood Group"])
    st.write("🏥 Condition:", patient.iloc[0]["Condition"])
    st.write("📞 Contact:", patient.iloc[0]["Contact"])
    st.success("📧 Email Alert Sent To Family")

    st.toast("🚨 SOS ALERT SENT!")