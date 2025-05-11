import streamlit as st
import pandas as pd

# SCELTA TIPO DI PUNTO IN CASO DI PUNTO VINTO

st.subheader("Due to?")



if st.button("Team point"):

    st.switch_page("pages/w_player.py")



if st.button("Opponent error"):
    
    st.session_state.df.loc[st.session_state.current_row,"score"]="S"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="opp error"
    st.session_state.df.loc[st.session_state.current_row,"player"]= None
    st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
    st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
    
    st.session_state.current_row += 1
    
    st.switch_page("pages/score.py")

if st.button("Unknown"):

    st.session_state.df.loc[st.session_state.current_row,"score"]="S"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="unknown"
    st.session_state.df.loc[st.session_state.current_row,"player"]= None
    st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
    st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
    st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
    
    st.session_state.current_row += 1
    
    st.switch_page("pages/score.py")



st.subheader("Go back to the intial page")

if st.button("Back"):

    st.session_state.point_scored = st.session_state.point_scored - 1
    
    st.switch_page("pages/score.py")