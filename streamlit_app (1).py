import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime

# Disable certificate verification
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Main app structure
st.title("2089 STATE TRANSFER REGISTRATION")

# Google Sheets connection setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(credentials)

# Open the specific Google Sheet
sheet = gc.open_by_key(st.secrets["SHEET_ID"]).worksheet("Transfer")

# Registration Form
with st.form("registration_form"):
    # Player Information
    player_name = st.text_input("Enter your in-game name*", key="player_name")
    
    # Alliance Selection
    alliance = st.text_input("What is Your Current Alliance?*", key="alliance")
    
    # New fields
    reason_for_leaving = st.text_input("What is the Reason for leaving your original state?", key="reason_for_leaving")
    planned_alliance = st.text_input("Which alliance are you planning to join?", key="planned_alliance")
    
    # Power input with number validation
    power = st.number_input(
        "What is your power?*",
        min_value=0.0,
        format="%.2f",
        step=0.01,
        key="power"
    )
    
    # FC Level
    fc_level = st.selectbox(
        "What is Your FC level?*",
        ["F29","F30", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Troop Levels
    infantry_level = st.selectbox(
        "What is your Infantry Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    lancer_level = st.selectbox(
        "What is your Lancer Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    marksman_level = st.selectbox(
        "What is your Marksman Troops level?*",
        ["T10", "FC1", "FC2", "FC3", "FC4", "FC5"],
        index=0
    )
    
    # Submit Button
    submitted = st.form_submit_button("Submit Registration")
    
    if submitted:
        if not player_name:
            st.error("Please enter your in-game name")
        elif not alliance:
            st.error("Please enter your current alliance name")
        elif power <= 0:
            st.error("Please enter a valid power value (greater than 0)")
        else:
            # Prepare the data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [
                timestamp,
                player_name,
                alliance,
                reason_for_leaving,
                planned_alliance,
                f"{power:.2f}",  # Format power to 2 decimal places
                fc_level,
                infantry_level,
                lancer_level,
                marksman_level
            ]
            
            try:
                # Append the new row to the sheet
                sheet.append_row(new_row)
                st.success("Registration submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Failed to save data: {str(e)}")

# Add credit to STRIKE at the bottom of the page
st.markdown("---")  # Horizontal line for separation
st.markdown(
    """
    <div style="text-align: center; padding: 20px; background-color: #0E1117; border-radius: 10px;">
        <h3 style="color: #ffffff;">Developed by STRIKE</h3>
        <p style="color: #ffffff;">For alliance management and state transfer coordination</p>
    </div>
    """,
    unsafe_allow_html=True
)
