import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# --- ESTILOS CSS (FONDO DE ESTADIO + TARJETAS PREMIUM) ---
# Usamos una imagen de estadio de alta calidad (libre de derechos)
ESTADIO_URL = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* 1. Fondo de Estadio con capa oscura para leer bien el texto */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{ESTADIO_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    /* 2. Tarjetas con efecto 'Glassmorphism' (Vidrio ahumado) */
    .fifa-card {{
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(0, 0, 0, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }}
    
    .fifa-card:hover {{
        transform: translateY(-5px);
        border-color: #cc0000; /* Detalle rojo al pasar el mouse */
    }}

    /* 3. Tipografía y Detalles */
    .card-title {{ 
        font-size: 20px; 
        font-weight: 900; 
        text-transform: uppercase; 
        color: #fff; 
        letter-spacing: 1px;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}
    .card-subtitle {{ font-size: 14px; color: #ccc; margin-bottom: 15px; font-style: italic; }}
    
    /* Cajas de Estadísticas */
    .stat-box {{ 
        background-color: rgba(
