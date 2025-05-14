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

    focus_att = focus[focus['attack_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors','both'])
    
    if st.session_state.info_type == "points":
        focus_att = focus_att[(focus_att['score'] == 'S') & (focus_att['point_type'] == 'team point')]
        st.dataframe(focus_att)
    elif st.session_state.info_type == "errors":
        focus_att = focus_att[(focus_att['score'] == 'L') & (focus_att['point_type'] == 'team error')]
        st.dataframe(focus_att)
    else:
        focus_att = focus_att[(focus_att['point_type'] == 'team error') | (focus_att['point_type'] == 'team point') ]
        st.dataframe(focus_att)
   
if st.session_state.fundamental_type == "serve":

    focus_serve = focus[focus['serve_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors','both'])
    
    if st.session_state.info_type == "points":
        focus_serve = focus_serve[(focus_serve['score'] == 'S') & (focus_serve['point_type'] == 'team point')]
        st.dataframe(focus_serve)
    elif st.session_state.info_type == "errors":
        focus_serve = focus_serve[(focus_serve['score'] == 'L') & (focus_serve['point_type'] == 'team error')]
        st.dataframe(focus_serve)
    else:
        focus_serve = focus_serve[(focus_serve['point_type'] == 'team error') | (focus_serve['point_type'] == 'team point') ]
        st.dataframe(focus_serve)

if st.session_state.fundamental_type == "block":

    focus_block = focus[focus['block_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors','both'])
    
    if st.session_state.info_type == "points":
        focus_block = focus_block[(focus_block['score'] == 'S') & (focus_block['point_type'] == 'team point')]
        st.dataframe(focus_block)
    elif st.session_state.info_type == "errors":
        focus_block = focus_block[(focus_block['score'] == 'L') & (focus_block['point_type'] == 'opp point')]
        st.dataframe(focus_block)
    else:
        focus_block = focus_block[(focus_block['point_type'] == 'opp point') | (focus_block['point_type'] == 'team point') ]
        st.dataframe(focus_block)

if st.session_state.fundamental_type == "defense":

    focus_defense = focus[focus['defense_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", 'errors')
    
    if st.session_state.info_type == "errors":
        focus_defense = focus_defense[(focus_defense['score'] == 'L') & (focus_defense['point_type'] == 'opp point') & (focus_defense['attack_zone'].notna())]
        st.dataframe(focus_defense)
    
if st.session_state.fundamental_type == "receive":

    focus_receive = focus[focus['defense_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", 'errors')
    
    if st.session_state.info_type == "errors":
        focus_receive = focus_receive[(focus_receive['score'] == 'L') & (focus_receive['point_type'] == 'opp point') & (focus_receive['serve_zone'].notna())]
        st.dataframe(focus_receive)
    

