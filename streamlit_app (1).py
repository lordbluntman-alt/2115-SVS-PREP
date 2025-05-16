import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("SFC Battle Registration")

# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS Battle Registration")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?",
        ["TCW", "MRA", "RFA", "SHR" , "mra" , "FOX"],
        index=0
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?",
        ["F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Speedups Information
    st.subheader("Speedups Inventory")
    general_speedups = st.number_input(
        "How many General Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    
    building_speedups = st.number_input(
        "How many Building Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    
    training_speedups = st.number_input(
        "How many Training Speedups do you have (In Days)?*",
        min_value=0,
        step=1,
        value=0
    )
    
    # Troop Levels (Current)
    st.subheader("Current Troop Levels")
    infantry_level = st.selectbox(
        "What is your current Infantry Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_level = st.selectbox(
        "What is your current Lancer Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_level = st.selectbox(
        "What is your current Marksman Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Training Goals During Prep
    st.subheader("Training Goals During Prep Phase")
    fc_goal = st.selectbox(
        "Which FC Level you are going for During SvS prep?",
        ["FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    infantry_goal = st.selectbox(
        "Which FC Infantry Level will you be training During Prep Phase?",
        ["FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_goal = st.selectbox(
        "Which FC Marksman Level will you be training During Prep Phase?",
        ["FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_goal = st.selectbox(
        "Which FC Lancer Level will you be training During Prep Phase?",
        ["FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Preferred timing for ministry buff
    buff_timing = st.selectbox(
        "What is your Preferred timing For ministry Buff?",
        ["12:00 UTC", "13:00 UTC", "14:00 UTC", "15:00 UTC", "16:00 UTC", "17:00 UTC", "18:00 UTC"],
        index=0
    )
    
    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        if not player_name:
            st.error("Please enter your in-game name")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [
                timestamp,
                player_name,
                alliance,
                fc_level,
                general_speedups,
                building_speedups,
                training_speedups,
                infantry_level,
                lancer_level,
                marksman_level,
                fc_goal,
                infantry_goal,
                marksman_goal,
                lancer_goal,
                buff_timing
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")
