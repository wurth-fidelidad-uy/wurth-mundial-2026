import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS (DISEÑO VISUAL + FOTOS CIRCULARES)
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* Fuentes Locales */
    @font-face {{ font-family: 'WuerthExtra'; src: url('WuerthExtraBoldCond.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBold'; src: url('WuerthBold.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBook'; src: url('WuerthBook.ttf') format('truetype'); }}

    html, body, [class*="css"], .stDataFrame, .stText, p, span, div {{
        font-family: 'WuerthBook', sans-serif;
        color: #ffffff !important;
        font-size: 18px;
    }}
    
    h1, h2, h3, h4 {{ font-family: 'WuerthExtra', sans-serif !important; color: white !important; }}

    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('{ESTADIO_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="column"] {{ border-right: 1px solid rgba(255, 255, 255, 0.2); padding: 0 15px; }}
    [data-testid="column"]:last-child {{ border-right: none; }}

    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 25px;
    }}

    /* Estilo de la Foto del Capitán */
    .captain-photo {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #cc0000;
        margin: 0 auto 15px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        display: block;
    }}

    .card-title {{ font-family: 'WuerthExtra'; font-size: 26px; text-transform: uppercase; line-height: 1; margin-bottom: 5px; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 16px; color: #ddd !important; margin-bottom: 15px; }}
    
    .stat-box {{ 
        background-color: rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; color: white;
        border-bottom: 3px solid #cc0000; margin-bottom: 20px; padding-bottom: 5px;
    }}

    .highlight-gold {{ border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important; }}
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES AUXILIARES ---

@st.cache_data # Cacheamos para que no tenga que procesar la imagen cada vez que refrescas
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def format_score(val):
    if pd.isna(val) or val == "": return "-"
    if isinstance(val, float) and val.is_integer(): return int(val)
    return val

def draw_card(equipo, capitan, score_raw, label_score, border_class=""):
    score_display = format_score(score_raw)
    
    # Buscador de imágenes (ignora mayúsculas y busca diferentes extensiones)
    img_base64 = None
    if isinstance(capitan, str):
        cap_name = capitan.strip().lower()
        for file in os.listdir("."):
            name, ext = os.path.splitext(file)
            if name.lower() == cap_name and ext.lower() in [".png", ".jpg", ".jpeg"]:
                img_base64 = get_image_as_base64(file)
                break
            
    if img_base64:
        photo_html = f'<img src="data:image/png;base64,{img_base64}" class="captain-photo">'
    else:
        photo_html = '<div style="font-size: 60px; margin-bottom: 10px;">👤</div>'

    card_html = f"""
    <div class="fifa-card {border_class}">
        {photo_html}
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <span style="color: #eee; font-family: 'WuerthBook'; font-size: 14px;">{label_score}</span><br>
            <strong style="color: #fff; font-size: 24px; font-family: 'WuerthBold';">{score_display}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- 4. HEADER ---
c1, c2 = st.columns([1.5, 6])
with c1:
    logo = next((f for f in os.listdir(".") if "logo" in f.lower() and f.endswith((".png", ".jpg"))), None)
    if logo: st.image(logo, use_container_width=True)
    else: st.markdown("<div style='font-size: 80px; text-align: center;'>🏆</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- 5. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    
    # Lógica de clasificación
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    for grupo in grupos_labels:
        mask = df['Grupo'] == grupo
        for kpi, pts in reglas.items():
            if df.loc[mask, kpi].max() > 0:
                max_val = df.loc[mask, kpi].max()
                ganadores = df[mask][df[mask][kpi] == max_val].index
                df.loc[ganadores, 'Puntos_Fase2'] += pts

    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Destino'] = df.groupby('Grupo').cumcount().apply(lambda x: 'Mundial' if x == 0 else 'Confederaciones')

    # --- 6. VISUALIZACIÓN ---
    tab1, tab2, tab3, tab4 = st.tabs(["📢 SORTEO", "⚔️ GRUPOS", "🏆 MUNDIAL", "🥈 CONFEDERACIONES"])
    
    with tab1:
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].rename(columns={'F1_Venta_23_Ene_Porcentaje': 'Resultado'}), hide_index=True, use_container_width=True, height=450)

    with tab2:
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {grupo}</div>", unsafe_allow_html=True)
                for _, row in df[df['Grupo'] == grupo].iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)

    with tab3:
        st.dataframe(df[df['Destino'] == 'Mundial'][['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

    with tab4:
        st.dataframe(df[df['Destino'] == 'Confederaciones'][['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], hide_index=True, use_container_width=True)

except Exception as e:
    st.error(f"Error cargando datos: {e}")
