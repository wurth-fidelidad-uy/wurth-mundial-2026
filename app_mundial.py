import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS (DISEÑO INSTITUCIONAL + IMÁGENES DE SUPERVISORES)
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* Fuentes Personalizadas */
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

    /* Estilo de las Imágenes de Supervisor (Tamaño Icono Violeta) */
    .supervisor-img {{
        width: 85px;
        height: 85px;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid #cc0000;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}

    .default-avatar {{
        font-size: 50px;
        background: #6f42c1; /* Color Violeta */
        width: 85px;
        height: 85px;
        line-height: 85px;
        border-radius: 50%;
        display: inline-block;
        margin-bottom: 10px;
        text-align: center;
    }}

    .media-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }}

    /* Tarjetas */
    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 25px;
        transition: transform 0.2s;
    }}
    .fifa-card:hover {{ transform: scale(1.02); border-color: #cc0000; }}

    .card-title {{ font-family: 'WuerthExtra'; font-size: 22px; text-transform: uppercase; color: #fff !important; margin-top: 5px; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 15px; color: #bbb !important; }}
    .stat-box {{ background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px; margin-top: 15px; }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; color: white;
        border-bottom: 3px solid #cc0000; margin-bottom: 20px;
    }}

    .highlight-gold {{ border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important; }}
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES AUXILIARES ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def format_score(val):
    if pd.isna(val) or val == "": return "-"
    try:
        if float(val).is_integer(): return int(val)
        return val
    except: return val

def draw_card(equipo, capitan, score_raw, label_score, border_class=""):
    score_display = format_score(score_raw)
    
    # Búsqueda automática de imagen del equipo
    img_base64 = None
    for ext in [".png", ".jpeg", ".jpg"]:
        path = f"{equipo}{ext}"
        if os.path.exists(path):
            img_base64 = get_image_base64(path)
            break
    
    if img_base64:
        media_html = f'<img src="data:image/png;base64,{img_base64}" class="supervisor-img">'
    else:
        media_html = '<div class="default-avatar">👤</div>'

    card_html = f"""
    <div class="fifa-card {border_class}">
        <div class="media-container">{media_html}</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <span style="color: #eee; font-size: 13px;">{label_score}</span><br>
            <strong style="color: #fff; font-size: 24px; font-family: 'WuerthBold';">{score_display}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- 3. HEADER ---
c1, c2 = st.columns([1.5, 6])
with c1:
    if os.path.exists("logo_wurth.png"):
        st.image("logo_wurth.png", use_container_width=True)
    else:
        st.markdown("<div style='font-size: 80px;'>🏆</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- 4. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except:
    st.error(f"⚠️ No se encontró el archivo: {archivo_excel}")
    datos_cargados = False

if datos_cargados:
    # Orden inicial por ventas para el sorteo de grupos
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # Lógica de Puntos Fase 2: MÁXIMO 1 GANADOR POR KPI POR GRUPO
    df['Puntos_Fase2'] = 0
    reglas = {
        'F2_Workout_Week_Score': 3, 
        'F2_Sales_Battle_2_Score': 2, 
        'F2_Customer_Month_Score': 4, 
        'F2_Clientes_Compradores_Score': 5
    }

    for grupo in grupos_labels:
        mask = df['Grupo'] == grupo
        idx_grupo = df[mask].index
        
        for kpi, pts in reglas.items():
            max_val = df.loc[idx_grupo, kpi].max()
            if max_val > 0:
                # Se asignan los puntos solo al primer equipo que tenga el valor máximo (desempate por ranking inicial)
                ganador_idx = df.loc[idx_grupo][df.loc[idx_grupo, kpi] == max_val].index[0]
                df.at[ganador_idx, 'Puntos_Fase2'] += pts

    # Clasificación a fase final
    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- 5. PESTAÑAS ---
    tabs = st.tabs(["📊 CLASIFICACIÓN A GRUPOS", "⚔️ GRUPOS", "🏆 MUNDIAL", "🥈 CONFEDERACIONES", "📅 PARTIDOS Y PUNTOS", "🖼️ EQUIPOS"])
    
    with tabs[0]:
        st.markdown("### 📊 Ranking Clasificatorio")
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True, use_container_width=True)

    with tabs[1]:
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {grupo}</div>", unsafe_allow_html=True)
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)

    with tabs[2]:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        df_mundial = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        if not df_mundial.empty:
            best = df_mundial.iloc[0]
            val = best['F3_Pedidos_Por_Dia']
            hay_datos = pd.notna(val) and val > 0
            c1, c2 = st.columns([1, 2])
            with c1:
                if hay_datos: st.balloons()
                draw_card(best['Equipo'], best['Capitan'], val, "Pedidos/Día", "highlight-gold" if hay_datos else "")
            with c2:
                st.dataframe(df_mundial[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

    with tabs[3]:
        st.markdown("## 🥈 FINAL COPA CONFEDERACIONES")
        df_conf = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        st.dataframe(df_conf[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

    with tabs[4]:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("## 📅 PARTIDOS Y PUNTOS DEL CAMPEONATO")
        st.markdown(f"""
            <a href="#" target="_blank" style="text-decoration: none;">
                <div style='display: inline-block; padding: 20px 50px; background-color: #cc0000; border-radius: 50px; border: 2px solid white; margin-top:30px;'>
                    <span style='color: white !important; font-family: "WuerthExtra"; font-size: 24px;'>VER INFORMACIÓN 📊</span>
                </div>
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[5]:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("## ⚽ EQUIPOS Y FORMACIONES")
        st.markdown(f"""
            <a href="http://www.wurth.com.uy" target="_blank" style="text-decoration: none;">
                <div style='display: inline-block; padding: 20px 50px; background-color: #cc0000; border-radius: 50px; border: 2px solid white; margin-top:30px;'>
                    <span style='color: white !important; font-family: "WuerthExtra"; font-size: 24px;'>VER LA TARJETA DE CADA EQUIPO 🔗</span>
                </div>
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
