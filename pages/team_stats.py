import streamlit as st
import pandas as pd


import streamlit as st
import pandas as pd
import glob
import plotly.graph_objects as go

# Titolo dell'app
st.title("Game stats")

# Trova tutti i file Excel (.xlsx) nella directory corrente
excel_files = glob.glob("*.xlsx")

if excel_files:
    st.sidebar.header("File Excel trovati")
    st.sidebar.write(excel_files)

    # Opzione per scegliere tra statistiche cumulative o per singola partita
    mode = st.sidebar.radio("Seleziona la modalità:", ["Cumulative stats", "Single match stats"])

    if mode == "Single match stats":
        # Seleziona un file specifico
        selected_file = st.sidebar.selectbox("Seleziona un file Excel:", excel_files)
        excel_files = [selected_file]  # Considera solo il file selezionato

    total_our_score = 0
    total_opp_score = 0
    fault_count = 0
    team_point_count = 0
    team_error_count = 0
    opp_error_count = 0
    opp_point_count = 0
    card_count = 0
    unknown_count = 0
    total_defense_lost = 0
    total_receive_errors = 0

    # Dizionario per memorizzare i dati per ogni giocatore
    player_stats = {}

    for file_name in excel_files:
        # Legge tutti i fogli del file Excel
        excel_data = pd.ExcelFile(file_name)
        sheet_names = excel_data.sheet_names

        for sheet_name in sheet_names:
            # Legge il foglio corrente
            df = pd.read_excel(file_name, sheet_name=sheet_name)

            # Conta punti persi e guadagnati
            if 'our_score' in df.columns and 'opp_score' in df.columns:
                if not df.empty and not df['our_score'].isna().all() and not df['opp_score'].isna().all():
                    total_our_score += df['our_score'].iloc[-1]
                    total_opp_score += df['opp_score'].iloc[-1]

            # Conta i parametri della colonna point_type
            if 'point_type' in df.columns:
                fault_count += df['point_type'].str.count("foul").sum()
                team_point_count += df['point_type'].str.count("team point").sum()
                team_error_count += df['point_type'].str.count("team error").sum()
                opp_error_count += df['point_type'].str.count("opp error").sum()
                opp_point_count += df['point_type'].str.count("opp point").sum()
                card_count += df['point_type'].str.count("card").sum()
                unknown_count += df['point_type'].str.count("unknown").sum()

            # Analizza i dati per ogni giocatore
            if 'player' in df.columns and 'score' in df.columns:
                for _, row in df.iterrows():
                    player = row['player']
                    score = row['score']
                    serve_zone = row['serve_zone'] if 'serve_zone' in df.columns else None
                    attack_zone = row['attack_zone'] if 'attack_zone' in df.columns else None
                    block_zone = row['block_zone'] if 'block_zone' in df.columns else None
                    defense_zone = row['defense_zone'] if 'defense_zone' in df.columns else None

                    # Ignora i valori NaN nella colonna player
                    if pd.isna(player):
                        continue

                    if player not in player_stats:
                        player_stats[player] = {
                            'S': 0,
                            'L': 0,
                            'Ace': 0,
                            'Attack point': 0,
                            'Block': 0,
                            'Defense lost': 0,
                            'Receive errors': 0,
                            'Attack errors': 0,
                            'Serve errors': 0,
                            'Block lost': 0,
                            'Att%': 0,
                            'Serve%': 0,
                            'Def%': 0,
                            'Rec%': 0,
                            'Block%': 0
                        }

                    if score == "S":
                        player_stats[player]['S'] += 1
                        # Controlla se è un ace
                        if serve_zone and not pd.isna(serve_zone):
                            player_stats[player]['Ace'] += 1
                        # Controlla se è un punto attacco
                        if attack_zone and not pd.isna(attack_zone):
                            player_stats[player]['Attack point'] += 1
                        # Controlla se è un muro
                        if block_zone and not pd.isna(block_zone):
                            player_stats[player]['Block'] += 1
                    elif score == "L":
                        player_stats[player]['L'] += 1
                        # Controlla se è una difesa persa
                        if defense_zone and not pd.isna(defense_zone):
                            player_stats[player]['Defense lost'] += 1
                            total_defense_lost += 1
                        # Controlla se è un errore in ricezione
                        if serve_zone and not pd.isna(serve_zone):
                            player_stats[player]['Receive errors'] += 1
                            total_receive_errors += 1
                        # Count attack errors
                        if attack_zone and not pd.isna(attack_zone):
                            player_stats[player]['Attack errors'] += 1
                        # Count serve errors
                        if serve_zone and not pd.isna(serve_zone):
                            player_stats[player]['Serve errors'] += 1
                        # Controlla se è un "Block lost"
                        if 'point_type' in row and row['point_type'] == "opp point" and block_zone and not pd.isna(block_zone):
                            if 'Block lost' not in player_stats[player]:
                                player_stats[player]['Block lost'] = 0
                            player_stats[player]['Block lost'] += 1

    # Assicurati che il calcolo di Att% e Serve% venga eseguito solo per giocatori validi
    for player, stats in player_stats.items():
        if stats['Attack point'] + stats['Attack errors'] > 0:
            player_stats[player]['Att%'] = (stats['Attack point'] / (stats['Attack point'] + stats['Attack errors'])) * 100
        else:
            player_stats[player]['Att%'] = 0

        # Calcolo sicuro di Serve%
        if stats['Ace'] + stats['Serve errors'] > 0:
            player_stats[player]['Serve%'] = (stats['Ace'] / (stats['Ace'] + stats['Serve errors'])) * 100
        else:
            player_stats[player]['Serve%'] = 0

        # Calcolo Def%
        player_stats[player]['Def%'] = player_stats[player]['Defense lost'] / total_defense_lost * 100
    
        # Calcolo Rec%
        player_stats[player]['Rec%'] = player_stats[player]['Receive errors'] / total_receive_errors * 100

        # Calcolo Block%
        if player_stats[player]['Block'] + player_stats[player]['Block lost'] > 0:
            player_stats[player]['Block%'] = player_stats[player]['Block'] / (player_stats[player]['Block'] + player_stats[player]['Block lost']) * 100
        else:
            player_stats[player]['Block%'] = 0

    # Funzione per creare radar plot
    def make_player_radar_chart(player_name, stats):
        metrics = ['Att%', 'Serve%', 'Def%', 'Rec%', 'Block%']
        values = [stats[metric] for metric in metrics]
        values.append(values[0])  # Chiudi il radar plot
        angles = metrics + [metrics[0]]  # Chiudi il radar plot

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=angles,
            fill='toself',
            name=player_name
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]  # Percentuali da 0 a 100
                )
            ),
            showlegend=True
        )
        return fig
    
    # Mostra i risultati generali
    st.write(f"Total scored points: {int(total_our_score)}")
    st.write(f"Total lost points: {int(total_opp_score)}")
    st.write(f"Fault number: {int(fault_count)}")
    st.write(f"Total team points: {int(team_point_count)}")
    st.write(f"Total team errors: {int(team_error_count)}")
    st.write(f"Total opponent errors: {int(opp_error_count)}")
    st.write(f"Total opponent points: {int(opp_point_count)}")
    st.write(f"Total card: {int(card_count)}")
    st.write(f"Total unknown: {int(unknown_count)}")
    st.write(f"Total defense lost: {int(total_defense_lost)}")
    st.write(f"Total receive errors: {int(total_receive_errors)}")

    # Mostra i risultati per giocatore
    st.subheader("Stats per player")
    for player, stats in player_stats.items():
        st.markdown(f"""
        **Player:** {player}  
        - **Points scored:** +{int(stats['S'])}  
        - **Points lost:** -{int(stats['L'])}  
        - **Aces:** {int(stats['Ace'])}  
        - **Attack points:** {int(stats['Attack point'])}  
        - **Blocks:** {int(stats['Block'])}  
        - **Defense lost:** {int(stats['Defense lost'])}  
        - **Receive errors:** {int(stats['Receive errors'])}
        - **Attack errors:** {int(stats['Attack errors'])}
        - **Serve errors:** {int(stats['Serve errors'])}
        - **Block lost:** {int(stats['Block lost'])}
        - **Att%:** {stats['Att%']:.2f}%
        - **Serve%:** {stats['Serve%']:.2f}%
        - **Def%:** {stats['Def%']:.2f}%
        - **Rec%:** {stats['Rec%']:.2f}%
        - **Block%:** {stats['Block%']:.2f}%
        """)

        # Genera e mostra il radar plot
        radar_chart = make_player_radar_chart(player, stats)
        st.plotly_chart(radar_chart)

else:
    st.error("No Excel file (.xlsx) found in the current directory")