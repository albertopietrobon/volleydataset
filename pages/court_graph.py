import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

if "info_type" not in st.session_state:
    st.session_state.info_type = "errors"

if "fundamental_type" not in st.session_state:
    st.session_state.fundamental_type = "attack"

if "player" not in st.session_state:
    st.session_state.player = "Paola Egonu"









def plot_volleyball_attack_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze, player_name="Giocatore",soglia_freq=0.01):
    
    if st.session_state.info_type == "points":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'{player_name} attack distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0, court_length], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0, court_length], 'k--', linewidth=1) #6m verticale
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [5*court_length/6,5*court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
        1: (2*court_width/3,0), 
        2: (2*court_width/3,court_length/3),
        3: (court_width/3,court_length/3),
        4: (0,court_length/3), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            if 2 <= zone <= 4:
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            else:
                circle = plt.Rectangle((x, y),height=6,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+3, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Attack zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
        1: (0,court_length), 
        2: (0,2*court_length/3),
        3: (court_width/3,2*court_length/3),
        4: (2*court_width/3,2*court_length/3), 
        5: (2*court_width/3,court_length), 
        6: (court_width/3,court_length),
        8: (0,5*court_length/6),
        9: (2*court_width/3,5*court_length/6),
        10:(court_width/3,5*court_length/6)
        }

        cmap2 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,3), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (1.5,court_length/3+1.5), 
            5: (1.5,3), 
            6: (court_width/3+1.5,3)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (0+1.5,court_length-1.5), 
            2: (0+1.5,2*court_length/3-1.5),
            3: (court_width/3+1.5,2*court_length/3-1.5),
            4: (2*court_width/3+1.5,2*court_length/3-1.5), 
            5: (2*court_width/3+1.5,court_length-1.5), 
            6: (court_width/3+1.5,court_length-1.5),
            8: (0+1.5,5*court_length/6-1.5),
            9: (2*court_width/3+1.5,5*court_length/6-1.5),
            10:(court_width/3+1.5,5*court_length/6-1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='green', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
    
    elif st.session_state.info_type == "errors":

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'{player_name} attack distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0, court_length/2+1], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0, court_length/2+1], 'k--', linewidth=1) #6m verticale
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/2+1,court_length/2+1], 'k--', linewidth=1) 
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)
        plt.plot([-1,court_width+1], [court_length/2,court_length/2], 'k--', linewidth=1)
        plt.plot([-1,-1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width+1,court_width+1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([-1,court_width+1], [court_length+1,court_length+1], 'k--', linewidth=1)
        plt.plot([0,0], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width,court_width], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width/3,court_width/3], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([2*court_width/3,2*court_width/3], [court_length, court_length+1], 'k--', linewidth=1)

        # Coordinate delle zone di attack
        zone_coords_att = {
        1: (2*court_width/3,0), 
        2: (2*court_width/3,court_length/3),
        3: (court_width/3,court_length/3),
        4: (0,court_length/3), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            if 2 <= zone <= 4:
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            else:
                circle = plt.Rectangle((x, y),height=6,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+3, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Attack zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (0,court_length+1), 
            2: (0,court_length/2+1),
            3: (court_width/3,court_length/2+1),
            4: (2*court_width/3,court_length/2+1), 
            5: (2*court_width/3,court_length+1), 
            6: (court_width/3,court_length+1),
            7: (-1,court_length+1),
            8: (court_width,court_length+1)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 7<= zone <= 8:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-10,width=1, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+0.5, y-5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,3), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (1.5,court_length/3+1.5), 
            5: (1.5,3), 
            6: (court_width/3+1.5,3)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (1.5,court_length+0.5), 
            2: (1.5,court_length/2+0.5),
            3: (court_width/3+1+1.5,court_length/2+0.5),
            4: (2*court_width/3+1.5,court_length/2+0.5), 
            5: (2*court_width/3+1.5,court_length+0.5), 
            6: (court_width/3+1.5,court_length+0.5),
            7: (-0.5,court_length-4),
            8: (court_width+0.5,court_length-4)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 

    
    



def plot_volleyball_serve_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze, player_name="Giocatore",soglia_freq=0.01):
    
    if st.session_state.info_type == "points":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'{player_name} serve distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [court_length/2, court_length], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [court_length/2, court_length], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width/3,court_width/3], [-1,0], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [-1,0], 'k--', linewidth=1) #6m verticale
        plt.plot([0,0], [-1,0], 'k--', linewidth=1) #3m verticale
        plt.plot([0,court_width], [-1,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width ,court_width], [-1,0], 'k--', linewidth=1)
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [5*court_length/6,5*court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
        1: (2*court_width/3,0), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():

            if 5<= zone <= 6:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if zone == 1:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Serving zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
        1: (0,court_length), 
        2: (0,2*court_length/3),
        3: (court_width/3,2*court_length/3),
        4: (2*court_width/3,2*court_length/3), 
        5: (2*court_width/3,court_length), 
        6: (court_width/3,court_length),
        8: (0,5*court_length/6),
        9: (2*court_width/3,5*court_length/6),
        10:(court_width/3,5*court_length/6)
        }

        cmap2 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ace zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,-0.5), 
            5: (1.5,-0.5), 
            6: (court_width/3+1.5,-0.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (0+1.5,court_length-1.5), 
            2: (0+1.5,2*court_length/3-1.5),
            3: (court_width/3+1.5,2*court_length/3-1.5),
            4: (2*court_width/3+1.5,2*court_length/3-1.5), 
            5: (2*court_width/3+1.5,court_length-1.5), 
            6: (court_width/3+1.5,court_length-1.5),
            8: (0+1.5,5*court_length/6-1.5),
            9: (2*court_width/3+1.5,5*court_length/6-1.5),
            10:(court_width/3+1.5,5*court_length/6-1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='green', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
    
    elif st.session_state.info_type == "errors":

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'{player_name} serve distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0,-1], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([0,0], [0,-1], 'k--', linewidth=1) #3m verticale
        plt.plot([court_width, court_width], [0,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([0, court_width], [-1,-1], 'k--', linewidth=1)
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/2+1,court_length/2+1], 'k--', linewidth=1) 
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)
        plt.plot([-1,court_width+1], [court_length/2,court_length/2], 'k--', linewidth=1)
        plt.plot([-1,-1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width+1,court_width+1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([-1,court_width+1], [court_length+1,court_length+1], 'k--', linewidth=1)
        plt.plot([0,0], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width,court_width], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width/3,court_width/3], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([2*court_width/3,2*court_width/3], [court_length, court_length+1], 'k--', linewidth=1)

        # Coordinate delle zone di attack
        zone_coords_att = {
        1: (2*court_width/3,0), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():

            if 5<= zone <= 6:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if zone == 1:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Serve zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (0,court_length+1), 
            2: (0,court_length/2+1),
            3: (court_width/3,court_length/2+1),
            4: (2*court_width/3,court_length/2+1), 
            5: (2*court_width/3,court_length+1), 
            6: (court_width/3,court_length+1),
            7: (-1,court_length+1),
            8: (court_width,court_length+1)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 7<= zone <= 8:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-10,width=1, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+0.5, y-5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,-0.5), 
            5: (1.5,-0.5), 
            6: (court_width/3+1.5,-0.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (1.5,court_length+0.5), 
            2: (1.5,court_length/2+0.5),
            3: (court_width/3+1+1.5,court_length/2+0.5),
            4: (2*court_width/3+1.5,court_length/2+0.5), 
            5: (2*court_width/3+1.5,court_length+0.5), 
            6: (court_width/3+1.5,court_length+0.5),
            7: (-0.5,court_length-4),
            8: (court_width+0.5,court_length-4)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 

    
    








































#DATA

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

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":
        focus_att = focus_att[(focus_att['score'] == 'S') & (focus_att['point_type'] == 'team point')]
        
        att = pd.DataFrame({
            'start_att' : focus_att['attack_zone'].str.extract(r'att_(\d+)')[0].dropna().astype(int),
            'end_att' : focus_att['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        att = att.reset_index(drop=True)

        #crea vettore con frequenza zone di attacco
        frequenza_attacchi = att['start_att'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_difese = att['end_att'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(att['start_att'], att['end_att'], normalize=True)


        min_frequenza_threshold = st.slider(
            "Soglia minima frequenza transizione:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_attack_frequency(frequenza_attacchi,frequenza_difese,frequenza_transizioni, st.session_state.player, soglia_freq=min_frequenza_threshold)


    elif st.session_state.info_type == "errors":
        focus_att = focus_att[(focus_att['score'] == 'L') & (focus_att['point_type'] == 'team error')]
        
        block_zone_extracted = focus_att['block_zone'].str.extract(r'block_net_(\d+)')[0].dropna().astype(int)

        out_zone_mapping = {
            'out_1': 1,
            'out_5': 5,
            'out_6': 6,
            'out_left': 7, 
            'out_right': 8 
        }

        out_zone_extracted_raw = focus_att['out_zone'].map(out_zone_mapping).dropna().astype(int, errors='ignore')

        start_att = focus_att['attack_zone'].str.extract(r'att_(\d+)')[0].dropna().astype(int)

        end_att_block = block_zone_extracted.reindex(start_att.index)
        end_att_out = out_zone_extracted_raw.reindex(start_att.index)

        end_att = pd.concat([end_att_block, end_att_out]).dropna().astype(int)
        att = pd.DataFrame({'start_att': start_att, 'end_att': end_att})

        att = att.dropna(subset=['end_att']).astype(int)
        att = att.reset_index(drop=True)
        st.dataframe(att)
        #crea vettore con frequenza zone di attacco
        frequenza_attacchi = att['start_att'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_difese = att['end_att'].value_counts(normalize=True).sort_index().reindex(range(1, 9), fill_value=0)
        frequenza_transizioni = pd.crosstab(att['start_att'], att['end_att'], normalize=True)
    

        min_frequenza_threshold = st.slider(
            "Soglia minima frequenza transizione:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_attack_frequency(frequenza_attacchi,frequenza_difese,frequenza_transizioni, st.session_state.player, soglia_freq=min_frequenza_threshold)

   
if st.session_state.fundamental_type == "serve":

    focus_serve = focus[focus['serve_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":
        focus_serve = focus_serve[(focus_serve['score'] == 'S') & (focus_serve['point_type'] == 'team point')]
        
        serve = pd.DataFrame({
            'start_serve' : focus_serve['serve_zone'].str.extract(r'serve_(\d+)')[0].dropna().astype(int),
            'end_serve' : focus_serve['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        serve = serve.reset_index(drop=True)
        
        #crea vettore con frequenza zone di servizio
        frequenza_servizi = serve['start_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_ace = serve['end_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(serve['start_serve'], serve['end_serve'], normalize=True)


        min_frequenza_threshold = st.slider(
            "Soglia minima frequenza transizione:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_serve_frequency(frequenza_servizi,frequenza_ace,frequenza_transizioni, st.session_state.player, soglia_freq=min_frequenza_threshold)





    elif st.session_state.info_type == "errors":
        focus_serve = focus_serve[(focus_serve['score'] == 'L') & (focus_serve['point_type'] == 'team error')]
        
        block_zone_extracted = focus_serve['block_zone'].str.extract(r'block_net_(\d+)')[0].dropna().astype(int)

        out_zone_mapping = {
            'out_1': 1,
            'out_5': 5,
            'out_6': 6,
            'out_left': 7, 
            'out_right': 8 
        }

        out_zone_extracted_raw = focus_serve['out_zone'].map(out_zone_mapping).dropna().astype(int, errors='ignore')

        start_serve = focus_serve['serve_zone'].str.extract(r'serve_(\d+)')[0].dropna().astype(int)

        end_serve_block = block_zone_extracted.reindex(start_serve.index)
        end_serve_out = out_zone_extracted_raw.reindex(start_serve.index)

        end_serve = pd.concat([end_serve_block, end_serve_out]).dropna().astype(int)
        serve = pd.DataFrame({'start_serve': start_serve, 'end_serve': end_serve})

        serve = serve.dropna(subset=['end_serve']).astype(int)
        serve = serve.reset_index(drop=True)
        st.dataframe(focus_serve)
        st.dataframe(serve)
        #crea vettore con frequenza zone di attacco
        frequenza_servizi = serve['start_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_ace = serve['end_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 9), fill_value=0)
        frequenza_transizioni = pd.crosstab(serve['start_serve'], serve['end_serve'], normalize=True)
    

        min_frequenza_threshold = st.slider(
            "Soglia minima frequenza transizione:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_serve_frequency(frequenza_servizi,frequenza_ace,frequenza_transizioni, st.session_state.player, soglia_freq=min_frequenza_threshold)

    
######################################################################################
if st.session_state.fundamental_type == "block":

    focus_block = focus[focus['block_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":
        focus_block = focus_block[(focus_block['score'] == 'S') & (focus_block['point_type'] == 'team point')]
        st.dataframe(focus_block)
    elif st.session_state.info_type == "errors":
        focus_block = focus_block[(focus_block['score'] == 'L') & (focus_block['point_type'] == 'opp point')]
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



