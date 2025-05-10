import streamlit as st
import pandas as pd

# SCELTA PLAYER IN CASO DI PUNTO GUADAGNATO

st.subheader("Select the player involved")

# Controlla se il game_roster è stato definito
if "game_roster" in st.session_state and st.session_state.game_roster:
    for player in st.session_state.game_roster:
        if st.button(player):
            st.session_state.df.loc[st.session_state.current_row, "player"] = player
            st.switch_page("pages/w_court.py")
else:
    st.warning("No players selected in the roster. Please go back and select players.")

# Tasto score page
st.subheader("Go to the initial page")
if st.button("Back"):
    st.switch_page("pages/score.py")