import streamlit as st
import pandas as pd
import os
import pyttsx3
import datetime
import time

from medicine_name import medicine_name

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

st.title("Memory Guardian AI")

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

if st.button("Save"):

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
            
            ##MEDICINE REMINDER
            
        st.header("Medicine Reminder")

        medicine_time = st.time_input("Medicine Time")

        if st.button("Add Reminder"):

              st.success(
                f"Reminder Added: {medicine_name} at {medicine_time}"
             )

              current_time = datetime.datetime.now().strftime("%H:%M")

              reminder_time = medicine_time.strftime("%H:%M")

              if current_time == reminder_time:

                 message = f"Time to take {medicine_name}"

                 st.warning(message)

                 speak(message)
       