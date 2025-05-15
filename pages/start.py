import streamlit as st
import pandas as pd

# PRIMA PAGINA, SCELTA TRA NEW GAME, GAME HISTORY E PLAYER STATS

new_game = st.button("NEW GAME")
game_history = st.button("GAME HISTORY")
player_stats = st.button("PLAYER STATS")

if new_game:
    
    st.session_state.info_df = pd.DataFrame()

    st.session_state.df = pd.DataFrame({
        "score": [None],
        "point_type": [None],
        "player": [None],
        "attack_zone": [None],
        "serve_zone": [None],
        "defense_zone": [None],
        "block_zone": [None],
        "out_zone": [None],
        "our_score": [None],  
        "opp_score": [None],  
    })

    st.session_state.current_row = 0
    st.session_state.n_set = 1

    st.session_state.set1 = pd.DataFrame()
    st.session_state.set2 = pd.DataFrame()
    st.session_state.set3 = pd.DataFrame()
    st.session_state.set4 = pd.DataFrame()
    st.session_state.set5 = pd.DataFrame()

    st.switch_page("pages/data.py")

if game_history:
    st.switch_page("pages/team_stats.py")

if player_stats:
   st.switch_page("pages/player_stats.py")