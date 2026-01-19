import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

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
        font-size: 18px;
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
    
    [data-testid="column"] {{
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        padding-right: 15px; padding-left: 15px;
    }}
    [data-testid="column"]:last-child {{ border-right: none; }}

    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 25px;
    }}

    .card-title {{ font-family: 'WuerthExtra'; font-size: 26px; text-transform: uppercase; color: #fff !important; margin-bottom: 5px; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 16px; color: #ddd !important; margin-bottom: 15px; }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; border-bottom: 3px solid #cc0000; margin-bottom: 20px;
    }}
    
    .stDataFrame {{ background-color: rgba(0,0,0,0.6) !important; }}
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES AUXILIARES ---

def format_score(val):
    if pd.isna(val) or val == "": return "-"
    if isinstance(val, float) and val.is_integer(): return int(val)
    return val

def draw_card(equipo, capitan, score_raw, label_score, border_class=""):
    score_display = format_score(score_raw)
    card_html = f"""
    <div class="fifa-card {border_class}">
        <div style="font-size: 50px; margin-bottom: 10px;">👤</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box" style="background-color: rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 10px; margin-top: 10px;">
            <span style="color: #eee; font-family: 'WuerthBook'; font-size: 14px;">{label_score}</span><br>
            <strong style="color: #fff; font-size: 24px; font-family: 'WuerthBold';">{score_display}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- 4. HEADER ---
c1, c2 = st.columns([1.5, 6])
with c1:
    if os.path.exists("logo_wurth.png"):
        st.image("logo_wurth.png", use_container_width=True)
    else:
        st.markdown("<div style='font-size: 80px; text-align: center;'>🏆</div>", unsafe_allow_html=True)
with c2:
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- 5. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except:
    st.error("No se encuentra el archivo Excel.")
    datos_cargados = False

if datos_cargados:
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    for grupo in grupos_labels:
        mask = df['Grupo'] == grupo
        df_g = df[mask]
        for kpi, pts in reglas.items():
            max_val = df_g[kpi].max()
            if max_val > 0:
                ganadores = df_g[df_g[kpi] == max_val].index
                df.loc[ganadores, 'Puntos_Fase2'] += pts

    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Destino'] = df.groupby('Grupo').cumcount().apply(lambda x: 'Mundial' if x == 0 else 'Confederaciones')

    tab1, tab2, tab_mundial, tab_conf, tab_galeria = st.tabs(["📢 SORTEO", "⚔️ GRUPOS", "🏆 MUNDIAL", "🥈 CONFEDERACIONES", "🖼️ VER EQUIPOS"])
    
    with tab1:
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].rename(columns={'F1_Venta_23_Ene_Porcentaje': 'Resultado Final'}), hide_index=True, use_container_width=True, height=(len(df)+1)*38)

    with tab2:
        cols = st.columns(4)
        for i, g_label in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {g_label}</div>", unsafe_allow_html=True)
                for _, row in df[df['Grupo'] == g_label].iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)

    with tab_galeria:
        st.markdown("## 🖼️ Galería de Equipos")
        
        # MAPEO INVERSO: Nombre Equipo en Excel -> Nombre exacto del archivo
        mapa_fotos = {
            "Equipo Cartera Propia": "Natalia García",
            "Equipo K3": "Andrés Viera",
            "Equipo Madera": "Álvaro Guerra"
        }
        
        g_tabs = st.tabs(["Grupo A", "Grupo B", "Grupo C", "Grupo D"])
        for i, g_label in enumerate(grupos_labels):
            with g_tabs[i]:
                df_g = df[df['Grupo'] == g_label].sort_values('Equipo')
                cols_gal = st.columns(3)
                
                for idx, row in df_g.reset_index().iterrows():
                    with cols_gal[idx % 3]:
                        nombre_equipo = str(row['Equipo']).strip()
                        nombre_cap_excel = str(row['Capitan']).strip()
                        
                        # 1. ¿Es una de nuestras excepciones?
                        nombre_archivo = mapa_fotos.get(nombre_equipo, nombre_cap_excel)
                        
                        # 2. Buscador multiformato (GIF, JPG, PNG)
                        img_path = None
                        for ext in [".gif", ".jpg", ".jpeg", ".png", ".GIF", ".JPG"]:
                            path_test = f"{nombre_archivo}{ext}"
                            if os.path.exists(path_test):
                                img_path = path_test
                                break
                        
                        st.markdown(f"""
                        <div class="fifa-card">
                            <div class="card-subtitle" style="color:#cc0000 !important;">{nombre_equipo}</div>
                            <div class="card-title" style="font-size:20px;">{nombre_cap_excel}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if img_path:
                            st.image(img_path, use_container_width=True)
                        else:
                            st.warning(f"Sin foto: {nombre_archivo}")

    # (Las pestañas de Mundial y Confederaciones siguen la lógica de las tablas anteriores)
