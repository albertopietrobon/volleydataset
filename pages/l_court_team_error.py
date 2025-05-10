import streamlit as st
import pandas as pd
import numpy as np
import pathlib

# PAGINA CAMPO IN CASO DI PUNTO PERSO, TEAM ERROR

#recall the court.css file to create the court
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/l_court_team_error.css")
load_css(css_path)

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'point_att' not in st.session_state:
    st.session_state.point_att = 0

if 'point_def' not in st.session_state:
    st.session_state.point_def = 0


def click_step(i):
    st.session_state.step = i

def click_att(i):
    st.session_state.point_att = i

def click_def(i):
    st.session_state.point_def = i


def return_set_page():
    st.session_state.current_row += 1  # Passa alla riga successiva
    st.success(f"Moved to the next row: {st.session_state.current_row + 1}")
    st.session_state.step = 0
    st.switch_page("pages/score.py")
    


if st.session_state.step == 0:

    #creation of the court
    col1,col2,col3,col4,col5=st.columns(5,gap="small")

    with col1:
        eb1 = st.button("out", key="ebutt1", on_click=click_def,args=['out-left'], use_container_width=True)

    with col2:
        eb2 = st.button("out", key="ebutt2", on_click=click_def,args=['out-1'], use_container_width=True)
        eb3 = st.button("1", key="ebutt3", use_container_width=True)
        eb4 = st.button("2", key="ebutt4", use_container_width=True)
        eb5 = st.button("block/net", key="ebutt5", on_click=click_def,args=['block/net-2'], use_container_width=True)
        eb6 = st.button("4", key="ebutt6", on_click=click_att,args=['att-4'], use_container_width=True)
        eb7 = st.button("5", key="ebutt7", on_click=click_att,args=['att-5'], use_container_width=True)
        eb8 = st.button("serve", key="ebutt8", on_click=click_att,args=['serve-5'], use_container_width=True)

    with col3:
        eb9 = st.button("out", key="ebutt9", on_click=click_def,args=['out-6'], use_container_width=True)
        eb10 = st.button("1", key="ebutt10", use_container_width=True)
        eb11 = st.button("2", key="ebutt11", use_container_width=True)
        eb12 = st.button("block/net", key="ebutt12", on_click=click_def,args=['block/net-3'], use_container_width=True)
        eb13 = st.button("4", key="ebutt13", on_click=click_att,args=['att-3'], use_container_width=True)
        eb14 = st.button("5", key="ebutt14", on_click=click_att,args=['att-6'], use_container_width=True)
        eb15 = st.button("serve", key="ebutt15", on_click=click_att,args=['serve-6'], use_container_width=True)

    with col4:
        eb16 = st.button("out", key="ebutt16", on_click=click_def,args=['out-5'], use_container_width=True)
        eb17 = st.button("1", key="ebutt17", use_container_width=True)
        eb18 = st.button("2", key="ebutt18", use_container_width=True)
        eb19 = st.button("block/net", key="ebutt19", on_click=click_def,args=['block/net-4'], use_container_width=True)
        eb20 = st.button("4", key="ebutt20", on_click=click_att,args=['att-2'], use_container_width=True)
        eb21 = st.button("5", key="ebutt21", on_click=click_att,args=['att-1'], use_container_width=True)
        eb22 = st.button("serve", key="ebutt22", on_click=click_att,args=['serve-1'], use_container_width=True)
    
    with col5:
        eb23 = st.button("out", key="ebutt23", on_click=click_def,args=['out-right'], use_container_width=True)

    confirm = st.button("Confirm point", key="econfirm", on_click=click_step, args=[1])

    st.subheader("Go to the initial page")
    if st.button("Back"):
        st.switch_page("pages/score.py")

if st.session_state.step == 1:

    if st.session_state.point_att != 0 and st.session_state.point_def !=0:
        st.info(f"You selected: error in {st.session_state.point_def} from {st.session_state.point_att} .\n\nDo you want to save the action?")
        back = st.button("Back", key="eback", on_click=click_step, args=[0])
        save = st.button("Save", key="esave", on_click=click_step, args = [2])

    
    elif (st.session_state.point_att==0) or (st.session_state.point_def==0):
        st.warning("Please go back. You are missing the point selection!")
        back = st.button("Back", key="eback", on_click=click_step, args=[0])
        
        
if st.session_state.step == 2:
    # Salva i valori in base al tipo di azione
    if 'att' in st.session_state.point_att:
        st.session_state.df.loc[st.session_state.current_row, "attack_zone"] = st.session_state.point_att
    elif 'serve' in st.session_state.point_att:
        st.session_state.df.loc[st.session_state.current_row, "serve_zone"] = st.session_state.point_att

    if 'block/net' in st.session_state.point_def:
        st.session_state.df.loc[st.session_state.current_row, "block_zone"] = st.session_state.point_def
    elif 'out' in st.session_state.point_def:
        st.session_state.df.loc[st.session_state.current_row, "out_zone"] = st.session_state.point_def

    # Reset delle variabili
    st.session_state.point_att = 0
    st.session_state.point_def = 0

    # Passa alla riga successiva
    st.session_state.current_row += 1

    return_set_page()
