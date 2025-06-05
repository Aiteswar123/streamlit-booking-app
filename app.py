import streamlit as st
import json
import os
from datetime import datetime, timedelta

# Define constants
DAYS_ALLOWED = ['Saturday', 'Sunday']
SESSIONS = {
    "10:00–12:00": "10_12",
    "14:00–16:00": "14_16",
    "16:00–18:00": "16_18"
}
MAX_BOOKINGS = 3
BOOKING_FILE = 'bookings.json'

# Load or initialize booking data
def load_bookings():
    if os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_bookings(bookings):
    with open(BOOKING_FILE, 'w') as f:
        json.dump(bookings, f, indent=4)

# Check if a date is weekend
def is_weekend(date):
    return date.strftime('%A') in DAYS_ALLOWED

# Main app
def main():
    st.title("Weekend Group Appointment Booking")

    # Date picker
    booking_date = st.date_input("Choose a date", min_value=datetime.today().date())

    if not is_weekend(booking_date):
        st.warning("Bookings are only allowed on Saturdays and Sundays.")
        return

    bookings = load_bookings()
    date_str = booking_date.isoformat()

    if date_str not in bookings:
        bookings[date_str] = {sess_code: [] for sess_code in SESSIONS.values()}

    st.subheader("Select a Session")
    available_sessions = []
    for label, code in SESSIONS.items():
        count = len(bookings[date_str][code])
        status = f"({count}/3 booked)"
        if count >= MAX_BOOKINGS:
            st.button(f"{label} - FULL", disabled=True)
        else:
            available_sessions.append((label, code, status))

    if available_sessions:
        selected_label = st.selectbox("Available Sessions", [f"{label} {status}" for label, code, status in available_sessions])
        selected_code = next(code for label, code, status in available_sessions if f"{label} {status}" == selected_label)

        # Form
        st.subheader("Enter Group Details")
        email = st.text_input("Person In Charge Email")
        school_name = st.text_input("School Name")
        group_name = st.text_input("Group Name")

        if st.button("Book Session"):
            if not email or not school_name or not group_name:
                st.error("Please fill in all fields.")
            else:
                booking_info = {
                    "email": email,
                    "school_name": school_name,
                    "group_name": group_name
                }

                bookings[date_str][selected_code].append(booking_info)
                save_bookings(bookings)
                st.success(f"Booking confirmed for {selected_label.split()[0]} on {booking_date.strftime('%A, %d %B %Y')}")
    else:
        st.info("All sessions are fully booked for the selected date.")

if __name__ == '__main__':
    main()
