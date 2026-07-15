import json
from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

USERS = {
    "tech": {"password": "tech123", "role": "Technician"},
    "manager": {"password": "manager123", "role": "Manager"},
}

COMMANDS = {
    "Power On": "power_on",
    "Power Off": "power_off",
    "Restart": "restart",
}


def authenticate(username: str, password: str):
    """Return the user's role when the demo credentials are valid."""
    user = USERS.get(username.strip().lower())
    if user and user["password"] == password:
        return user["role"]
    return None


def build_control_payload(command: str, device: str) -> dict[str, str]:
    """Build the JSON-serializable payload sent by a manager."""
    return {"command": command, "device": device}


def load_mock_sheets() -> tuple[pd.DataFrame, pd.DataFrame]:
    inventory = pd.read_csv(DATA_DIR / "equipment.csv")
    schedules = pd.read_csv(DATA_DIR / "shifts.csv")
    return inventory, schedules


def show_login() -> None:
    st.title("AV Operations")
    st.caption("Sign in with one of the demo accounts listed in the README.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if submitted:
        role = authenticate(username, password)
        if role:
            st.session_state.username = username.strip().lower()
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid username or password.")


def show_app() -> None:
    inventory, schedules = load_mock_sheets()

    title_col, logout_col = st.columns([5, 1])
    with title_col:
        st.title("AV Operations")
        st.caption(
            f"Signed in as {st.session_state.username} · {st.session_state.role}"
        )
    with logout_col:
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()

    st.subheader("Equipment Inventory")
    st.dataframe(inventory, hide_index=True, use_container_width=True)

    st.subheader("Staff Shift Schedule")
    st.dataframe(schedules, hide_index=True, use_container_width=True)

    if st.session_state.role == "Manager":
        st.divider()
        st.subheader("Device Control")
        device_ids = inventory["device_id"].tolist()
        device = st.selectbox("Device", device_ids)
        command_label = st.selectbox("Command", list(COMMANDS))

        if st.button("Trigger Device Command", type="primary"):
            payload = build_control_payload(COMMANDS[command_label], device)
            st.session_state.last_payload = payload
            st.success("Device command simulated successfully.")

        if "last_payload" in st.session_state:
            st.caption("Generated JSON payload")
            st.code(json.dumps(st.session_state.last_payload), language="json")
    else:
        st.info("Technicians have view-only access. Device controls are unavailable.")


def main() -> None:
    st.set_page_config(page_title="AV Operations", page_icon="🎛️", layout="wide")
    if "role" not in st.session_state:
        show_login()
    else:
        show_app()


if __name__ == "__main__":
    main()
