import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime
import os

# Main app structure
st.set_page_config(page_title="VP Registration", page_icon="🏗️")
st.title("VP Registration (Construction)")

# Important Note and Caution
st.warning("""
**State buffs plan**  
10-Oct Monday : Construction                 
11-Oct Tuesday : Research  
13-Oct Thursday: Training  
""")

st.error("""
**CAUTION:**  
- Resource Preparation: Ensure you have sufficient resources to fully maximize your score  
- Fair Participation: Scores will be actively monitored. If you are assigned the buff, please contribute fairly to maintain equity for all participants. Your cooperation is greatly appreciated  
- **Registration Deadline: Registration closes at 12:00 UTC on 9th Oct**  
""")

# Google Sheets connection setup with error handling
@st.cache_resource
def get_google_sheet():
    try:
        # Check if secrets are available
        if "gcp_service_account" not in st.secrets:
            st.error("Google Cloud Service Account credentials not found in secrets")
            return None
        if "SHEET_ID" not in st.secrets:
            st.error("SHEET_ID not found in secrets")
            return None
            
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("SvS Prep Ministry Buffs")
        return sheet
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {str(e)}")
        return None

# Initialize sheet connection
sheet = get_google_sheet()

# Input validation functions
def validate_game_id(game_id):
    """Validate game ID format"""
    if not game_id:
        return False, "Game ID cannot be empty"
    # Basic validation - game IDs are typically numeric
    if not game_id.strip().isdigit():
        return False, "Game ID should contain only numbers"
    if len(game_id.strip()) < 6:
        return False, "Game ID seems too short"
    return True, ""

def validate_player_name(name):
    """Validate player name"""
    if not name or not name.strip():
        return False, "Player name cannot be empty"
    if len(name.strip()) < 2:
        return False, "Player name seems too short"
    return True, ""

# Registration Form
with st.form("registration_form", clear_on_submit=True):
    st.subheader("Player Information")
    
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name", 
                               placeholder="Your in-game name")
    game_id = st.text_input("Enter Your Game ID*", key="game_id", 
                           placeholder="Numeric game ID")
    
    # Alliance Selection
    alliance = st.selectbox(
        "What is Your Alliance?*",
        ["TCW", "EFE", "MRA", "FOX", "SHR", "MMD"],
        index=0
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your Current FC level?*",
        ["F28", "F29", "F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Speedups Information
    st.subheader("Inventory")
    
    col1, col2 = st.columns(2)
    
    with col1:
        general_speedups = st.number_input(
            "General Speedups (Days)*",
            min_value=0,
            step=1,
            value=0,
            help="Total general speedups in days"
        )
        
        building_speedups = st.number_input(
            "Building Speedups (Days)*",
            min_value=0,
            step=1,
            value=0,
            help="Total building speedups in days"
        )
    
    with col2:
        fc_count = st.number_input(
            "FCs Count*",
            min_value=0,
            step=1,
            value=0,
            help="Number of FCs available"
        )

        refined_fc_count = st.number_input(
            "Refined FCs Count*",
            min_value=0,
            step=1,
            value=0,
            help="Number of refined FCs available"
        )
  
    # Preferred timing for ministry buff
    buff_timing = st.selectbox(
        "Preferred time zone For ministry Buff*",
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
        # Validate inputs
        validation_passed = True
        error_messages = []
        
        # Validate player name
        is_valid_name, name_error = validate_player_name(player_name)
        if not is_valid_name:
            validation_passed = False
            error_messages.append(name_error)
        
        # Validate game ID
        is_valid_id, id_error = validate_game_id(game_id)
        if not is_valid_id:
            validation_passed = False
            error_messages.append(id_error)
        
        if not validation_passed:
            for error in error_messages:
                st.error(error)
        else:
            if sheet is None:
                st.error("Cannot connect to database. Please try again later.")
            else:
                try:
                    # Prepare the data row
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_row = [
                        timestamp,
                        player_name.strip(),
                        game_id.strip(),
                        alliance,
                        fc_level,
                        general_speedups,
                        building_speedups,
                        fc_count,
                        refined_fc_count,
                        buff_timing
                    ]
                    
                    # Append the new row to the sheet
                    sheet.append_row(new_row)
                    
                    st.success("Registration submitted successfully! 🎉")
                    st.balloons()
                    
                    # Show confirmation
                    st.info(f"""
                    **Registration Details:**
                    - Player: {player_name.strip()}
                    - Game ID: {game_id.strip()}
                    - Alliance: {alliance}
                    - FC Level: {fc_level}
                    - Preferred Time: {buff_timing}
                    """)
                    
                except Exception as e:
                    st.error(f"Failed to save data: {str(e)}")
                    st.info("Please try again or contact administrator if the problem persists.")

# Add some helpful information at the bottom
st.markdown("---")
st.caption("Need help? Contact your alliance leadership for assistance with registration.")
