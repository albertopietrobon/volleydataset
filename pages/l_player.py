import streamlit as st
import pandas as pd

# SCELTA PLAYER IN CASO DI PUNTO PERSO
if "player_selected" not in st.session_state:
     st.session_state.player_selected = ""


if st.button("Unknown"):

    st.session_state.df.loc[st.session_state.current_row,"score"]="L"
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


st.subheader("Select the player involved")

for player in st.session_state.game_roster:
    if st.button(player):
        st.session_state.player_selected = player
        st.switch_page("pages/l_point_type.py")


# Tasto score page
st.subheader("Go to the initial page")

if st.button("Back"):

    st.session_state.point_lost = st.session_state.point_lost - 1

    st.switch_page("pages/score.py")