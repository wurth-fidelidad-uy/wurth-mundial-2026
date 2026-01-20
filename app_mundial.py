import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
# El page_icon es lo que define el favicon (icono de pestaña y previsualización)
st.set_page_config(
    page_title="Würth World Cup 2026", 
    page_icon="logo_copa.png", 
    layout="wide"
)

# --- 2. FUNCIONES AUXILIARES ---
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except: return None

def format_score(val):
    if pd.isna(val) or val == "" or val == 0: return "-"
    try:
        if float(val).is_integer(): return int(val)
        return val
    except: return val

def draw_card(equipo, capitan, score_raw, label_score, border_class=""):
    score_display = format_score(score_raw)
    img_base64 = None
    for ext in [".png", ".jpeg", ".jpg"]:
        path = f"{equipo}{ext}"
        if os.path.exists(path):
            img_base64 = get_image_base64(path)
            break
    
    media_html = f'<img src="data:image/png;base64,{img_base64}" class="supervisor-img">' if img_base64 else '<div class="default-avatar">👤</div>'

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

    .supervisor-img {{
        width: 85px; height: 85px; object-fit: cover; border-radius: 50%;
        border: 3px solid #cc0000; margin-bottom: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}

    .default-avatar {{
        font-size: 50px; background: #6f42c1; width: 85px; height: 85px; 
        line-height: 85px; border-radius: 50%; display: inline-block; text-align: center;
    }}

    .media-container {{ display: flex; justify-content: center; align-items: center; margin-bottom: 10px; }}

    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 25px;
    }}

    .card-title {{ font-family: 'WuerthExtra'; font-size: 22px; text-transform: uppercase; color: #fff !important; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 15px; color: #bbb !important; }}
    .stat-box {{ background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px; margin-top: 15px; }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; color: white;
        border-bottom: 3px solid #cc0000; margin-bottom: 20px;
    }}

    .highlight-gold {{ border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important; }}
    .highlight-silver {{ border-color: #C0C0C0 !important; box-shadow: 0 0 15px rgba(192, 192, 192, 0.3) !important; }}
    .highlight-bronze {{ border-color: #CD7F32 !important; box-shadow: 0 0 15px rgba(205, 127, 50, 0.3) !important; }}

    .wait-message {{
        background: rgba(204, 0, 0, 0.2); border: 1px solid #cc0000;
        padding: 40px; border-radius: 20px; text-align: center; margin-top: 50px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    if os.path.exists("logo_copa.png"):
        st.image("logo_copa.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>WÜRTH WORLD CUP 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #ccc;'>⚽ Tablero Oficial de Competencia</p>", unsafe_allow_html=True)

# --- 4. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except:
    st.error(f"⚠️ ERROR: No se pudo leer el archivo '{archivo_excel}'.")
    datos_cargados = False

if datos_cargados:
    # A. Clasificación inicial
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # B. Puntos acumulados
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    
    for grupo in grupos_labels:
        idx_g = df[df['Grupo'] == grupo].index
        for kpi, pts in reglas.items():
            max_val = df.loc[idx_g, kpi].max()
            if max_val > 0:
                ganador_idx = df.loc[idx_g][df.loc[idx_g, kpi] == max_val].index[0]
                df.at[ganador_idx, 'Puntos_Fase2'] += pts

    # C. Desempate Final para asignar Mundial/Confederaciones
    df = df.sort_values(
        by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes', 'F1_Venta_23_Ene_Porcentaje'], 
        ascending=[True, False, False, False]
    ).reset_index(drop=True)
    
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- 5. PESTAÑAS ---
    tab1, tab2, tab_m, tab_c, tab_p, tab_ext = st.tabs([
        "📊 CLASIFICACIÓN", "⚔️ GRUPOS", "🏆 MUNDIAL", "🥈 CONFEDERACIONES", "📅 REGLAMENTO", "🖼️ EQUIPOS"
    ])
    
    with tab1:
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True, use_container_width=True)

    with tab2:
        cols = st.columns(4)
        for i, g in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {g}</div>", unsafe_allow_html=True)
                df_g = df[df['Grupo'] == g]
                for _, row in df_g.iterrows():
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales")

    with tab_m:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        df_m = df[df['Destino'] == 'Mundial'].sort_values(['F3_Pedidos_Por_Dia', 'F2_TieBreak_Nuevos_Clientes'], ascending=[False, False])
        
        if not df_m.empty and (df_m['F3_Pedidos_Por_Dia'] > 0).any():
            best = df_m.iloc[0]
            st.balloons()
            c1, c2 = st.columns([1, 2])
            with c1: draw_card(best['Equipo'], best['Capitan'], best['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-gold")
            with c2: st.dataframe(df_m[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia', 'F2_TieBreak_Nuevos_Clientes']], hide_index=True, use_container_width=True)
        else:
            st.markdown("<div class='wait-message'><h3>⏳ COMPETENCIA EN CURSO</h3><p>El campeón mundial aparecerá aquí al cargar datos de Pedidos/Día.</p></div>", unsafe_allow_html=True)

    with tab_c:
        st.markdown("## 🥈 FINAL COPA CONFEDERACIONES")
        df_c = df[df['Destino'] == 'Confederaciones'].sort_values(['F3_Pedidos_Por_Dia', 'F2_TieBreak_Nuevos_Clientes'], ascending=[False, False])
        
        if not df_c.empty and (df_c['F3_Pedidos_Por_Dia'] > 0).any():
            c1, c2, c3 = st.columns(3); meds = ["🥇 Oro", "🥈 Plata", "🥉 Bronce"]; clss = ["highlight-gold", "highlight-silver", "highlight-bronze"]
            for i in range(min(3, len(df_c))):
                row = df_c.iloc[i]
                with [c1, c2, c3][i]:
                    st.markdown(f"<h4 style='text-align:center'>{meds[i]}</h4>", unsafe_allow_html=True)
                    draw_card(row['Equipo'], row['Capitan'], row['F3_Pedidos_Por_Dia'], "Pedidos/Día", clss[i])
            st.divider()
            st.dataframe(df_c[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia', 'F2_TieBreak_Nuevos_Clientes']], hide_index=True, use_container_width=True)
        else:
            st.markdown("<div class='wait-message'><h3>⏳ COMPETENCIA EN CURSO</h3><p>Las medallas se asignarán al cargar datos de Pedidos/Día.</p></div>", unsafe_allow_html=True)

    with tab_p:
        st.markdown("<div style='text-align: center; margin-top: 50px;'><h2>📅 REGLAMENTO</h2><a href='https://viewer.ipaper.io/wurth-uruguay/world-cup/wurth-world-cup-2026/' target='_blank' style='text-decoration:none;'><div style='display:inline-block; padding:20px 50px; background-color:#cc0000; border-radius:50px; border:2px solid white; color:white; font-family:WuerthExtra; font-size:24px; margin-top:20px;'>VER INFORMACIÓN 📊</div></a></div>", unsafe_allow_html=True)

    with tab_ext:
        st.markdown("<div style='text-align: center; margin-top: 50px;'><h2>⚽ EQUIPOS</h2><a href='http://www.wurth.com.uy' target='_blank' style='text-decoration:none;'><div style='display:inline-block; padding:20px 50px; background-color:#cc0000; border-radius:50px; border:2px solid white; color:white; font-family:WuerthExtra; font-size:24px; margin-top:20px;'>VER LA TARJETA DE CADA EQUIPO 🔗</div></a></div>", unsafe_allow_html=True)
