import streamlit as st

# PRIMA PAGINA, SCELTA TRA NEW GAME, GAME HISTORY E PLAYER STATS

new_game = st.button("NEW GAME")
game_history = st.button("GAME HISTORY")
player_stats = st.button("PLAYER STATS")

if new_game:
    st.switch_page("pages/data.py")

#if game_history:
#    st.switch_page("pages/?.py")

#if player_stats:
#    st.switch_page("pages/?.py")