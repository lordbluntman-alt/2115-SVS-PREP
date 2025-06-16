import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("SvS Ministry Buffs Registration")

# Important Note and Caution
st.warning("""
**State buffs plan**  
16-June Monday: Construction  
19-June Thursday: Training  
20-June Friday: Research  
""")

st.error("""
**CAUTION:**  
- Resource Preparation: Ensure you have sufficient resources to fully maximize your score  
- Fair Participation: Scores will be actively monitored. If you are assigned the buff, please contribute fairly to maintain equity for all participants. Your cooperation is greatly appreciated  
- **Registration Deadline: Registration closes at 12:00 UTC on 18th June**  
""")


# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS Prep Ministry Buffs")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["TCW", "MRA", "RFA", "SHR" , "mra" , "FOX" , "ROK" , "ANT" , "TWN" , "DIU" ],
        index=0
    )
    
    # Ministry Buff Selection
    ministry_buff = st.multiselect(
        "Which ministry Buff do You want?",
        ["Ministry of Education"],
        default=["Ministry of Education"]
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?*",
        ["F26","F27","F28","F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
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
        ["T9","T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_level = st.selectbox(
        "What is your current Lancer Troops level?*",
        ["T9","T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_level = st.selectbox(
        "What is your current Marksman Troops level?*",
        ["T9","T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Training Goals During Prep
    st.subheader("Training Goals During Prep Phase")
    fc_goal = st.selectbox(
        "Which FC Level you are going for During SvS prep?*",
        ["F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    infantry_goal = st.selectbox(
        "Which FC Infantry Level will you be training During Prep Phase?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_goal = st.selectbox(
        "Which FC Marksman Level will you be training During Prep Phase?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_goal = st.selectbox(
        "Which FC Lancer Level will you be training During Prep Phase?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Preferred timing for ministry buff
    buff_timing = st.selectbox(
        "What is your Preferred time zone For ministry Buff?*",
        [
            "00:00 UTC to 02:00 UTC",
            "02:00 UTC to 04:00 UTC",
            "04:00 UTC to 06:00 UTC",
            "06:00 UTC to 08:00 UTC",
            "08:00 UTC to 10:00 UTC",
            "10:00 UTC to 12:00 UTC",
            "12:00 UTC to 14:00 UTC",
            "14:00 UTC to 16:00 UTC",
            "16:00 UTC to 18:00 UTC",
            "18:00 UTC to 20:00 UTC",
            "20:00 UTC to 22:00 UTC",
            "22:00 UTC to 23:59 UTC"
        ],
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
                ", ".join(ministry_buff),  # Convert list to comma-separated string
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
