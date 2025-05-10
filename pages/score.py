import streamlit as st
import pandas as pd
import io   # per scaricare il file excel

# SCELTA PUNTO GUADAGNATO O PERSO E SALVATAGGIO FILE EXCEL
st.subheader("What happened?")

if st.button("Point scored"):
    st.session_state.df.loc[st.session_state.current_row, "score"] = "Point scored"
    
    # Verifica che la riga precedente esista e aggiorna i punteggi
    if st.session_state.current_row > 0 and st.session_state.current_row - 1 in st.session_state.df.index:
        st.session_state.df.loc[st.session_state.current_row, "our_score"] = (
            st.session_state.df.loc[st.session_state.current_row - 1, "our_score"] + 1
        )
        st.session_state.df.loc[st.session_state.current_row, "opp_score"] = (
            st.session_state.df.loc[st.session_state.current_row - 1, "opp_score"]
        )
    else:
        # Usa i valori esistenti se disponibili, altrimenti inizializza
        st.session_state.df.loc[st.session_state.current_row, "our_score"] = (
            st.session_state.df["our_score"].max() + 1 if "our_score" in st.session_state.df.columns else 1
        )
        st.session_state.df.loc[st.session_state.current_row, "opp_score"] = (
            st.session_state.df["opp_score"].max() if "opp_score" in st.session_state.df.columns else 0
        )
    st.switch_page("pages/w_point_type.py")

if st.button("Point lost"):
    st.session_state.df.loc[st.session_state.current_row, "score"] = "Point lost"
    
    # Verifica che la riga precedente esista e aggiorna i punteggi
    if st.session_state.current_row > 0 and st.session_state.current_row - 1 in st.session_state.df.index:
        st.session_state.df.loc[st.session_state.current_row, "opp_score"] = (
            st.session_state.df.loc[st.session_state.current_row - 1, "opp_score"] + 1
        )
        st.session_state.df.loc[st.session_state.current_row, "our_score"] = (
            st.session_state.df.loc[st.session_state.current_row - 1, "our_score"]
        )
    else:
        # Usa i valori esistenti se disponibili, altrimenti inizializza
        st.session_state.df.loc[st.session_state.current_row, "opp_score"] = (
            st.session_state.df["opp_score"].max() + 1 if "opp_score" in st.session_state.df.columns else 1
        )
        st.session_state.df.loc[st.session_state.current_row, "our_score"] = (
            st.session_state.df["our_score"].max() if "our_score" in st.session_state.df.columns else 0
        )
    st.switch_page("pages/l_player.py")

# Aggiungi un pulsante "Next Set"
st.subheader("Start the next set")

if st.button("Next Set"):
    # Incrementa il numero del set corrente
    #if "current_set" not in st.session_state:
        #st.session_state.current_set = 1  # Inizializza il primo set
    #else:
    st.session_state.current_set += 1

    # Salva il foglio corrente nel file Excel
    file_name = f"Match_{st.session_state.date_str}.xlsx"
    try:
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Salva tutte le colonne del DataFrame nel foglio corrente
            st.session_state.df.to_excel(writer, index=False, sheet_name=f"Set {st.session_state.current_set-1}") 
        st.success(f"Set {st.session_state.current_set-1} salvato nel file Excel: {file_name}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file Excel: {e}")

    # Azzera il DataFrame per il nuovo set, con punteggi iniziali a zero
    st.session_state.df = pd.DataFrame(columns=["score", "point_type", "player", "attack_zone", "serve_zone", "defense_zone", "block_zone", "out_zone", "our_score", "opp_score"])
    st.session_state.df.loc[0] = ["", "", "", "", "", "", "", "", 0, 0]

    st.info(f"Pronto per il Set {st.session_state.current_set}!")

# Salva il foglio "Set 1" (ex "Game Report")
st.subheader("The game is concluded? Save and download the report, after adding optional comments")

text_input = st.text_input(
    "Post-match hot takes",
    key="placeholder",
)

if st.button("Save Game Report"):
    # Inizializza current_set se non esiste
    if "current_set" not in st.session_state:
        st.session_state.current_set = 1  # Inizializza il primo set

    file_name = f"Match_{st.session_state.date_str}.xlsx"
    
    # Verifica se il file esiste
    try:
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Salva tutte le colonne del DataFrame nel foglio corrente
            st.session_state.df.to_excel(writer, index=False, sheet_name=f"Set {st.session_state.current_set}")
            
            # Aggiungi un nuovo foglio "comments" con il contenuto del text_input
            comments_df = pd.DataFrame({"Comments": [st.session_state.placeholder]})
            comments_df.to_excel(writer, index=False, sheet_name="Comments")
        
        st.success(f"Set {st.session_state.current_set} e commenti salvati nel file Excel: {file_name}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file Excel: {e}")

# Verifica se il file Excel esiste e lo carica nel buffer per il download
file_name = f"Match_{st.session_state.date_str}.xlsx"

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