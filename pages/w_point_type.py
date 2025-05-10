import streamlit as st
import pandas as pd

# SCELTA TIPO DI PUNTO IN CASO DI PUNTO VINTO

st.subheader("Due to?")

if st.button("Team point"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Team point"
    st.switch_page("pages/w_player.py")

if st.button("Opponent error"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Opponent error"
    st.session_state.current_row += 1
    st.switch_page("pages/score.py")

st.subheader("Go back to the intial page")
if st.button("Back"):
    st.switch_page("pages/score.py")