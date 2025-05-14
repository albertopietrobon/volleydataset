import streamlit as st
import pandas as pd
import numpy as np

if "info_type" not in st.session_state:
    st.session_state.info_type = "errors"

if "fundamental_type" not in st.session_state:
    st.session_state.fundamental_type = "attack"

if "player" not in st.session_state:
    st.session_state.player = "Paola Egonu"

name1 = "datasets/Match_2025-04-16.xlsx"

match1 = pd.read_excel(name1, sheet_name=None)

match1_info = match1['Info']
match1_set1 = match1['Set 1']
match1_set2 = match1['Set 2']
match1_set3 = match1['Set 3']
match1_set4 = match1['Set 4']
match1_set5 = match1['Set 5']


all_match1 = pd.concat([match1_set1,match1_set2,match1_set3,match1_set4,match1_set5])


st.session_state.player = st.selectbox("Select a player:",st.session_state.roster['Name'])
st.session_state.fundamental_type = st.segmented_control("Choose the type of fundamental:", ["attack","serve","block","defense","receive"])


#filtering of the data presented based on player, points/errors/both, and fundamental

#player
focus = all_match1[all_match1['player'] == st.session_state.player]

#points/errors/both and fundamental
if st.session_state.fundamental_type == "attack":
    focus = focus[focus['attack_zone'].notna()]
    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors','both'])
    if st.session_state.info_type == "points":
        focus = focus[focus['score'] == 'S']
    elif st.session_state.info_type == "errors":
        focus = focus[focus['score'] == 'L']
        focus = focus[focus['point_type'] == 'team error']
    else:
        focus = focus
elif st.session_state.fundamental_type == "serve":
    focus = focus[focus['serve_zone'].notna()]
elif st.session_state.fundamental_type == "block":
    focus = focus[focus['block_zone'].notna()]
    
elif st.session_state.info_type == "errors":
     focus = focus[focus['score'] == 'L']
     if st.session_state.fundamental_type == "attack":
        focus = focus[focus['attack_zone'].notna()]
     elif st.session_state.fundamental_type == "serve":
        focus = focus[focus['serve_zone'].notna()]
     elif st.session_state.fundamental_type == "block":
        focus = focus[focus['block_zone'].notna()]
     elif st.session_state.fundamental_type == "defense":
        focus = focus[focus['defense_zone'].notna()]

else:
    focus = focus


if st.session_state.fundamental_type == "attack":
    focus = focus[focus['attack_zone'].notna()]
elif st.session_state.fundamental_type == "serve":
    focus = focus[focus['serve_zone'].notna()]
elif st.session_state.fundamental_type == "block":
    focus = focus[focus['block_zone'].notna()]
elif st.session_state.fundamental_type == "defense":
    focus = focus[focus['defense_zone'].notna()]



st.dataframe(focus)