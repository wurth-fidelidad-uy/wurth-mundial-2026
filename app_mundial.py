import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS (DISEÑO INSTITUCIONAL + MEDALLAS + IMÁGENES CIRCULARES)
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
        background: #6f42c1; /* Violeta Institucional */
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

    /* Tarjetas de Resultados */
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

    /* Clases de Resaltado para Medallas */
    .highlight-gold {{ border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important; }}
    .highlight-silver {{ border-color: #C0C0C0 !important; box-shadow: 0 0 15px rgba(192, 192, 192, 0.3) !important; }}
    .highlight-bronze {{ border-color: #CD7F32 !important; box-shadow: 0 0 15px rgba(205, 127, 50, 0.3) !important; }}
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
    
    # Búsqueda automática de imagen
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

    st.markdown(f"""
    <div class="fifa-card {border_class}">
        <div class="media-container">{media_html}</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <span style="color: #eee; font-size: 13px;">{label_score}</span><br>
            <strong style="color: #fff; font-size: 24px; font-family: 'WuerthBold';">{score_display}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.error(f"⚠️ ERROR: No se pudo leer el archivo '{archivo_excel}'.")
    datos_cargados = False

if datos_cargados:
    # 1. Ranking inicial por ventas
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # 2. Lógica de puntos (Máximo 14 puntos por grupo)
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    for grupo in grupos_labels:
        idx_g = df[df['Grupo'] == grupo].index
        for kpi, pts in reglas.items():
            max_val = df.loc[idx_g, kpi].max()
            if max_val > 0:
                # Solo un ganador por KPI por grupo (desempate por ranking inicial)
                ganador_idx = df.loc[idx_g][df.loc[idx_g, kpi] == max_val].index[0]
                df.at[ganador_idx, 'Puntos_Fase2'] += pts

    # 3. Clasificación Final
    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- 5. VISUALIZACIÓN EN PESTAÑAS ---
    tab1, tab2, tab_mundial, tab_conf, tab_partidos, tab_externo = st.tabs([
        "📊 CLASIFICACIÓN A GRUPOS", 
        "⚔️ GRUPOS", 
        "🏆 MUNDIAL", 
        "🥈 CONFEDERACIONES", 
        "📅 PARTIDOS Y PUNTOS",
        "🖼️ EQUIPOS"
    ])
    
    with tab1:
        st.markdown("### 📊 Clasificación Inicial")
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True, use_container_width=True)

    with tab2:
        cols = st.columns(4)
        for i, g in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {g}</div>", unsafe_allow_html=True)
                df_g = df[df['Grupo'] == g]
                for _, row in df_g.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)

    with tab_mundial:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        df_m = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        if not df_m.empty:
            best = df_m.iloc[0]
            val = best['F3_Pedidos_Por_Dia']
            hay_v = pd.notna(val) and val > 0
            c1, c2 = st.columns([1, 2])
            with c1:
                if hay_v: st.balloons()
                draw_card(best['Equipo'], best['Capitan'], val, "Pedidos/Día", "highlight-gold" if hay_v else "")
            with c2: st.dataframe(df_m[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

    with tab_conf:
        st.markdown("## 🥈 FINAL COPA CONFEDERACIONES")
        df_c = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        if not df_c.empty:
            c1, c2, c3 = st.columns(3)
            meds = ["🥇 Oro", "🥈 Plata", "🥉 Bronce"]
            clss = ["highlight-gold", "highlight-silver", "highlight-bronze"]
            for i in range(min(3, len(df_c))):
                row = df_c.iloc[i]
                val = row['F3_Pedidos_Por_Dia']
                with [c1, c2, c3][i]:
                    st.markdown(f"<h4 style='text-align:center'>{meds[i]}</h4>", unsafe_allow_html=True)
                    draw_card(row['Equipo'], row['Capitan'], val, "Pedidos/Día", clss[i] if (pd.notna(val) and val > 0) else "")
            st.divider()
            st.dataframe(df_c[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

    with tab_partidos:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("## 📅 PARTIDOS Y PUNTOS DEL CAMPEONATO")
        st.markdown(f"""
            <a href="https://viewer.ipaper.io/wurth-uruguay/world-cup/wurth-world-cup-2026/" target="_blank" style="text-decoration: none;">
                <div style='display: inline-block; padding: 20px 50px; background-color: #cc0000; border-radius: 50px; border: 2px solid white; margin-top:30px;'>
                    <span style='color: white !important; font-family: "WuerthExtra"; font-size: 24px;'>VER INFORMACIÓN 📊</span>
                </div>
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_externo:
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
