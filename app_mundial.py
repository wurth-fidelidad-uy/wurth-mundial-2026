import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Würth World Cup 2026", 
    layout="wide", 
    page_icon="🏆"
)

# --- 2. FUNCIONES PARA CARGAR IMÁGENES LOCALES ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Preparamos el logo de la campaña para el encabezado
# Asegúrate de tener un archivo llamado 'logo_copa.png' en la misma carpeta
logo_campana_base64 = get_image_base64("logo_copa.png")

# ==============================================================================
# 🎨 ESTILOS CSS
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    @font-face {{ font-family: 'WuerthExtra'; src: url('WuerthExtraBoldCond.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBold'; src: url('WuerthBold.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBook'; src: url('WuerthBook.ttf') format('truetype'); }}

    html, body, [class*="css"], .stDataFrame, .stText, p, span, div {{
        font-family: 'WuerthBook', sans-serif;
        color: #ffffff !important;
    }}
    
    h1, h2, h3, h4 {{
        font-family: 'WuerthExtra', sans-serif !important;
        color: white !important;
        text-shadow: 0 3px 6px rgba(0,0,0,0.9);
    }}

    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('{ESTADIO_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .logo-container {{
        text-align: center;
        margin-bottom: 20px;
    }}

    .main-logo {{
        max-width: 250px;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.5));
    }}

    /* ... (resto de tus estilos de tarjetas y supervisor) ... */
    .supervisor-img {{
        width: 85px; height: 85px;
        object-fit: cover; border-radius: 50%;
        border: 3px solid #cc0000; margin-bottom: 10px;
    }}
    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px; padding: 20px; text-align: center;
    }}
    .wait-message {{
        background: rgba(204, 0, 0, 0.2);
        border: 1px solid #cc0000;
        padding: 40px; border-radius: 20px; text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER CON LOGO DIRECTO ---
if logo_campana_base64:
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_campana_base64}" class="main-logo">
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>WÜRTH WORLD CUP 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>⚽ Tablero Oficial de Competencia</p>", unsafe_allow_html=True)

# --- 4. LÓGICA DE DATOS (Se mantiene igual que la versión anterior) ---
# ... (Aquí va toda tu lógica de Excel, desempate y pestañas)
