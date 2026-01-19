import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# --- ESTILOS CSS (FONDO DE ESTADIO + TARJETAS) ---
# URL de una imagen de estadio de uso libre
ESTADIO_BG_URL = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

st.markdown(f"""
<style>
    /* FONDO DE ESTADIO */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{ESTADIO_BG_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    /* TARJETAS NEGRAS ESTILO FIFA */
    .fifa-card {{
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border: 2px solid #333;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.8); /* Sombra más intensa */
        margin-bottom: 20px;
        color: white;
        backdrop-filter: blur(5px); /* Efecto de cristal sobre el fondo */
    }}
    .card-title {{ font-size: 18px; font-weight: bold; text-transform: uppercase; color: #fff; text-shadow: 2px 2px 4px #000; }}
    .card-subtitle {{ font-size: 14px; color: #ccc; margin-bottom: 10px; }}
    .stat-box {{ 
        background-color: rgba(34, 34, 34, 0.8); 
        border-radius: 5px; padding: 5px; 
        font-size: 13px; margin-top: 5
