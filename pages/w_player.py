import streamlit as st
import pandas as pd

# SCELTA PLAYER IN CASO DI PUNTO GUADAGNATO
if "player_selected" not in st.session_state:
     st.session_state.player_selected = ""

st.subheader("Select the player involved")

for player in st.session_state.game_roster:
        if st.button(player):
            st.session_state.player_selected = player
            st.switch_page("pages/w_court.py")


# Tasto score page
st.subheader("Go to the initial page")

if st.button("Back"):

    st.session_state.point_scored = st.session_state.point_scored - 1

    st.switch_page("pages/score.py")