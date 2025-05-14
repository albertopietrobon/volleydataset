import streamlit as st
import pandas as pd
import io   # per scaricare il file excel

if "point_scored" not in st.session_state:
    st.session_state.point_scored = 0

if "point_lost" not in st.session_state:
    st.session_state.point_lost = 0

if "n_set" not in st.session_state:
    st.session_state.n_set = 1


# SCELTA PUNTO GUADAGNATO O PERSO E SALVATAGGIO FILE EXCEL
st.write(f"SET {st.session_state.n_set}")
st.write(f"{st.session_state.point_scored} - {st.session_state.point_lost}")



#punto fatto
if st.button("Point scored"):

    st.session_state.point_scored = st.session_state.point_scored + 1

    st.switch_page("pages/w_point_type.py")

#punto subito
if st.button("Point lost"):

    st.session_state.point_lost = st.session_state.point_lost + 1

    st.switch_page("pages/l_player.py")

#elimina ultimo punto salvato
if st.button("Delete last point"):

    if st.session_state.current_row != 0 :

        if st.session_state.df.loc[st.session_state.current_row-1,"score"] == "S":
            st.session_state.point_scored = st.session_state.point_scored - 1
        elif st.session_state.df.loc[st.session_state.current_row-1,"score"] == "L":
            st.session_state.point_lost = st.session_state.point_lost - 1

        st.session_state.df.loc[st.session_state.current_row-1,"score"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"point_type"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"player"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"attack_zone"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"serve_zone"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"defense_zone"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"block_zone"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"out_zone"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"our_score"]= None
        st.session_state.df.loc[st.session_state.current_row-1,"opp_score"]= None

        st.session_state.current_row = st.session_state.current_row -1
        st.rerun()
        
#show df
st.dataframe(st.session_state.df)
st.write(st.session_state.n_set)
# Aggiungi un pulsante "Next Set"
st.subheader("Start the next set")

#passa al prossimo set
if st.button("Next Set"):
    
    if st.session_state.n_set <=4:

        if st.session_state.n_set == 1 :

            st.session_state.set1 = st.session_state.df

            st.session_state.df = pd.DataFrame({
                "score": [None],
                "point_type": [None],
                "player": [None],
                "attack_zone": [None],
                "serve_zone": [None],
                "defense_zone": [None],
                "block_zone": [None],
                "out_zone": [None],
                "our_score": [None],  # Inizializza con 0
                "opp_score": [None],  # Inizializza con 0
            })

            st.session_state.point_scored = 0
            st.session_state.point_lost = 0
            st.session_state.current_row = 0
        
        if st.session_state.n_set == 2 :

            st.session_state.set2 = st.session_state.df

            st.session_state.df = pd.DataFrame({
                "score": [None],
                "point_type": [None],
                "player": [None],
                "attack_zone": [None],
                "serve_zone": [None],
                "defense_zone": [None],
                "block_zone": [None],
                "out_zone": [None],
                "our_score": [None],  # Inizializza con 0
                "opp_score": [None],  # Inizializza con 0
            })

            st.session_state.point_scored = 0
            st.session_state.point_lost = 0
            st.session_state.current_row = 0

        if st.session_state.n_set == 3 :

            st.session_state.set3 = st.session_state.df

            st.session_state.df = pd.DataFrame({
                "score": [None],
                "point_type": [None],
                "player": [None],
                "attack_zone": [None],
                "serve_zone": [None],
                "defense_zone": [None],
                "block_zone": [None],
                "out_zone": [None],
                "our_score": [None],  # Inizializza con 0
                "opp_score": [None],  # Inizializza con 0
            })

            st.session_state.point_scored = 0
            st.session_state.point_lost = 0
            st.session_state.current_row = 0

        if st.session_state.n_set == 4 :

            st.session_state.set4 = st.session_state.df

            st.session_state.df = pd.DataFrame({
                "score": [None],
                "point_type": [None],
                "player": [None],
                "attack_zone": [None],
                "serve_zone": [None],
                "defense_zone": [None],
                "block_zone": [None],
                "out_zone": [None],
                "our_score": [None],  # Inizializza con 0
                "opp_score": [None],  # Inizializza con 0
            })

            st.session_state.point_scored = 0
            st.session_state.point_lost = 0
            st.session_state.current_row = 0
        
        st.session_state.n_set += 1
        st.rerun()
    else:
        st.error("Reached maximum number of sets!")
        
    


if st.button("Save Game Report"):
    
    if st.session_state.n_set == 5:
        st.session_state.set5 = st.session_state.df
    
    if st.session_state.n_set == 4:
        st.session_state.set4 = st.session_state.df

    if st.session_state.n_set == 3:
        st.session_state.set3 = st.session_state.df
    

    file_name = f"Match_{st.session_state.date_str}.xlsx"
    
    #salva tutti i set sul file excel
    try:
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='w') as writer:
            
            st.session_state.info_df.to_excel(writer, index=False, sheet_name="Info")
            st.session_state.set1.to_excel(writer, index=False, sheet_name="Set 1")
            st.session_state.set2.to_excel(writer, index=False, sheet_name="Set 2")
            st.session_state.set3.to_excel(writer, index=False, sheet_name="Set 3")
            st.session_state.set4.to_excel(writer, index=False, sheet_name="Set 4")
            st.session_state.set5.to_excel(writer, index=False, sheet_name="Set 5")
            
    
        st.success(f"Game salvato nel file Excel: {file_name}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file Excel: {e}")
    

    try:
        with open(file_name, "rb") as f:
            buffer = io.BytesIO(f.read())  # Legge il contenuto del file salvato in memoria
    except FileNotFoundError:
        st.error(f"Il file {file_name} non esiste. Assicurati di salvarlo prima di scaricarlo.")
    else:
        # Button per il download del file excel
        st.download_button(
            label="Download the Excel file",
            data=buffer,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


#bottone ritorno 
if st.button(":house:"):
    st.session_state.point_scored = 0
    st.session_state.point_lost = 0
    st.session_state.n_set = 1
    st.switch_page('pages/start.py')
