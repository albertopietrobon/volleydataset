import streamlit as st
import pandas as pd

# SCELTA TIPO DI PUNTO IN CASO DI PUNTO PERSO

st.subheader("Due to?")

if st.button("Opponent point"):

    st.switch_page("pages/l_court_opp_point.py")

if st.button("Team error"):

    st.switch_page("pages/l_court_team_error.py")
    
if st.button("Foul"):
    
    st.session_state.df.loc[st.session_state.current_row,"score"]="L"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="foul"
    st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
    st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
    st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
    
    st.session_state.current_row += 1

    st.switch_page("pages/score.py")
    
if st.button("Card"):

    st.session_state.df.loc[st.session_state.current_row,"score"]="L"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="card"
    st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
    st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
    st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
    
    st.session_state.current_row += 1
    
    st.switch_page("pages/score.py")

# Tasto score page
st.subheader("Go back to the intial page")

if st.button("Back"):

    st.session_state.point_lost = st.session_state.point_lost - 1

    st.switch_page("pages/score.py")