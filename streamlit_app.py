import streamlit as st
import pandas as pd

data_page = st.Page('pages/data.py', title='data')
score_page = st.Page('pages/score.py', title='score')
w_point_type_page = st.Page('pages/w_point_type.py', title='w_point_type')
l_point_type_page = st.Page('pages/l_point_type.py', title='l_point_type')
w_player_page = st.Page('pages/w_player.py', title='w_player')
l_player_page = st.Page('pages/l_player.py', title='l_player')
w_court_page = st.Page('pages/w_court.py', title='w_court')
l_court_opp_point_page = st.Page('pages/l_court_opp_point.py', title='l_court_opp_point')
l_court_team_error_page = st.Page('pages/l_court_team_error.py', title='l_court_team_error')
start_page = st.Page('pages/start.py', title='start')

pg = st.navigation([start_page, data_page, score_page, w_point_type_page, l_point_type_page, w_player_page, l_player_page, w_court_page, l_court_opp_point_page, l_court_team_error_page], position='sidebar')
st.set_page_config(page_title='Volleyball report app DV4S', initial_sidebar_state='collapsed')

# Inizializza tutti i "session state"
    
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "score": [None],
        "point_type": [None],
        "player": [None],
        "attack_zone": [None],
        "defense_zone": [None],
        "block_zone": [None],
        "serve_zone": [None],
        "out_zone": [None],
        "our_score": [0],  # Inizializza con 0
        "opp_score": [0],  # Inizializza con 0
    })

if "current_row" not in st.session_state:
    st.session_state.current_row = 0  # Indice della riga corrente

if "match_date" not in st.session_state:
    st.session_state.match_date = None  # Puoi impostare un valore predefinito, ad esempio `None`

if "date_str" not in st.session_state:
    st.session_state.date_str = None

if "team name" not in st.session_state:
    st.session_state.team_name = 'Numia Vero Volley Milano'

if "opp_teams" not in st.session_state:
    st.session_state.opp_teams = [
        'Prosecco Doc Imoco Conegliano',
        'Savino Del Bene Scandicci',
        'Igor Gorgonzola Novara',
        'Reale Mutua Fenera Chieri 76',
        'Eurotek Uyba Busto Arsizio',
        'Megabox Ond. Savio Vallefoglia',
        'Bergamo',
        'Wash4green Pinerolo',
        'Bartoccini-Mc Restauri Perugia',
        'Honda Olivero Cuneo',
        'Il Bisonte Firenze',
        'Smi Roma Volley',
        'Cda Volley Talmassons Fvg'
    ]

team = {
     "Name": ['Helena Cazaute', 'Juliette Gelin','Ludovica Guidi', 'Laura Heyrman', 'Elena Pietrini', 'Alessia Orro', 'Anna Danesi', 'Lamprini Konstantinidou', 'Satomi Fukudome', 'Hena Kurtagic', 'Anna Smrek', 'Myriam Sylla', 'Paola Egonu', 'Nika Daalderop'],
     "Number":[1,2,3,5,7,8,11,12,13,14,15,17,18,19],
     "Role":['ATT','LIB','CEN','CEN','ATT','SET','CEN','SET','LIB','CEN','OPP','ATT','OPP','ATT'],
     "Age":[1997,2001,1992,1993,2000,1998,1996,1996,1997,2004,2003,1995,1998,1998],
     "Height":[184,162,186,188,186,180,196,184,162,195,207,181,193,190],
     "Nationality":['FRA','FRA','ITA','BEL','ITA','ITA','ITA','GRE','JPN','SRB','CAN','ITA','ITA','NED']
    }

if "roster" not in st.session_state:
    st.session_state.roster = team

pg.run()