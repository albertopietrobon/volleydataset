import streamlit as st
import pandas as pd
from openpyxl import Workbook

#ATTENZIONE: CAMBIARE NUMERO DI GIOCATORI DEL ROSTER
# PAGINA INIZIALE, SCELTA DI DATA, OPPONENT E ROSTER

if 'step' not in st.session_state:
    st.session_state.step = 0

if "game_opp" not in st.session_state:
    st.session_state.game_opp = None

if "game_roster" not in st.session_state:
    st.session_state.game_roster = None

def click_step(i):
    st.session_state.step = i

def return_home():
    st.session_state.step = 0
    st.switch_page("pages/start.py")

def start_game():
    st.session_state.step = 0
    st.switch_page("pages/score.py")

if st.session_state.step == 0:
    tab1,tab2,tab3 = st.tabs(['Game Date', 'Opponent Team', 'Game Roster'])

    with tab1:
        st.session_state.match_date = st.date_input("Select the game's date from the calendar:", st.session_state.match_date)
    with tab2:
        st.session_state.game_opp = st.radio("Select the opponent team:", st.session_state.opp_teams)
    with tab3:
        st.write("Details of available players:") 
        st.dataframe(st.session_state.roster)
        st.session_state.game_roster = st.multiselect("Select all the players for the match:", st.session_state.roster['Name'], placeholder="Choose a player...")

    col1,col2 = st.columns(2)

    with col1:
        home = st.button(":house:", on_click=click_step, args=[2])
    with col2:
        report = st.button("Report", on_click=click_step, args=[1])

if st.session_state.step == 1:
    if len(st.session_state.game_roster) != 14 : #ATTENZIONE: CAMBIARE NUMERO DI GIOCATORI DEL ROSTER
        st.warning("You are missing required information. Please finish to fill all the fields.")
        back = st.button("Back", on_click=click_step, args=[0])
    else:
        st.write(f">Game date: {st.session_state.match_date}")
        st.write(f">Opponent team: {st.session_state.game_opp}")
        st.write(f">Game roster: {st.session_state.game_roster}")
        col1,col2 = st.columns(2)

        with col1:
            back = st.button("Back", on_click=click_step, args=[0])
        with col2:
            save = st.button("Save", on_click=click_step, args=[3])

if st.session_state.step == 2:
    return_home()

if st.session_state.step == 3:
    # Formatta la data come stringa (es. "13-04-2025") e salvala in session_state
    if st.session_state.match_date:
        st.session_state.date_str = st.session_state.match_date.strftime("%Y-%m-%d")
    
    st.session_state.info_df = pd.DataFrame({
        "Players": st.session_state.game_roster,
        "Data": [st.session_state.match_date] * len(st.session_state.game_roster),
        "Opponent": [st.session_state.game_opp] * len(st.session_state.game_roster)
    })
    
    start_game()