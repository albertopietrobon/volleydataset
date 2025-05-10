import streamlit as st
import pandas as pd

# SCELTA TIPO DI PUNTO IN CASO DI PUNTO PERSO

st.subheader("Due to?")

if st.button("Opponent point"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Opponent point"
    st.switch_page("pages/l_court_opp_point.py")

if st.button("Team error"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Team error"
    st.switch_page("pages/l_court_team_error.py")
    
if st.button("Fault"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Fault"
    st.session_state.current_row += 1
    st.switch_page("pages/score.py")
    
if st.button("Card"):
    st.session_state.df.loc[st.session_state.current_row, "point_type"] = "Card"
    st.session_state.current_row += 1
    st.switch_page("pages/score.py")

# Tasto score page
st.subheader("Go back to the intial page")
if st.button("Back"):
    st.switch_page("pages/score.py")