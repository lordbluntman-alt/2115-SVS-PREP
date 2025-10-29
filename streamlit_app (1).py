import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("2115 Ministry Position Registration Request (All Days)")

# Important Note and Caution
st.warning("""
**State buffs plan**  
03-Nov Monday : Construction                 
04-Nov Tuesday : Research   
06-Nov Thursday: Training   
07-Nov Friday: Final Day  
  
""")

st.error("""
**CAUTION:**  
- Resource Preparation: Ensure you have sufficient resources to fully maximize your score. Always gather!   
- Fair Participation: If you are assigned the buff, please contribute fairly to maintain equity for all participants. Your contribution is greatly appreciated.  
- We will do our best to align you with your preferred time. But we cannot guarantee the slot will be available. If you have concerns, please reach out through your R5/R4s.  
- **Registration Deadline: Registration closes at 12:00 UTC on 2nd Nov** 
""")


# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
#sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SVS Prep Spreadsheet")
sheet = gc.open_by_key("1PfVQM8ckHdSQGYQTRVT_XghNO9VXGMc9xBsfxlip8Nw").worksheet("SVS Prep Spreadsheet")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    game_id = st.text_input("Enter Your Game ID*", key="game_id")
    
# Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["FBR", "LAT", "CON", "WLX" ,"NWN", "Bluntman is Sexy" ],
        index=0
    )
    
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?*",
        ["FC8","FC7","FC6", "FC5", "FC4", "FC3", "FC2", "FC1", "F30","Less than F30"],
        index=0
    )
  st.warning("""
   If you don’t know how many speed ups you have, it’s OKAY. Please enter “0”, and submit your request anyway.
""")

    # Speedups Information
    st.subheader("Inventory")
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
    

    
    fc_count = st.number_input(
        "How many FCs do you have?*",
        min_value=0,
        step=1,
        value=0
    )
    
    refined_fc_count = st.number_input(
        "How many Refined FCs do you have?*",
        min_value=0,
        step=1,
        value=0
    )
   # Construction Day
    day_1 = st.selectbox(
        "Do you want VP for construction on day 1?*",
        ["No","Yes"],
        index=0
    ) 
     # Research Day
    day_2 = st.selectbox(
        "Do you want VP on day 2 for research?*",
        ["No","Yes"],
        index=0
    ) 
     # Troops for the meat grinder Day
    day_4 = st.selectbox(
        "Do you want Minister of Education on day 4 to make more troops for the meat grinder?*",
        ["No","Yes"],
        index=0
    ) 
     # Final Day Day
    day_5 = st.selectbox(
        "Do you want VP on day 5 to finish construction and research?*",
        ["No","Yes"],
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
        if not player_name or not game_id:
            st.error("Please enter your in-game name and Game ID")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [
                timestamp,
                player_name,
                game_id,
                alliance,
                fc_level,
                general_speedups,
                building_speedups,
                fc_count,
                refined_fc_count,
                day_1,
                day_2,
                day_4,
                day_5,
                buff_timing
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")












