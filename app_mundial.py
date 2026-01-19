import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS CON TIPOGRAFÍAS WÜRTH
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    @font-face {{ font-family: 'WuerthExtra'; src: url('WuerthExtraBoldCond.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBold'; src: url('WuerthBold.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBook'; src: url('WuerthBook.ttf') format('truetype'); }}

    html, body, [class*="css"], .stDataFrame, p, span, div {{
        font-family: 'WuerthBook', sans-serif;
        color: #ffffff !important;
    }}
    
    h1, h2, h3, h4 {{ font-family: 'WuerthExtra', sans-serif !important; color: white !important; }}

    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url('{ESTADIO_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    [data-testid="column"] {{ border-right: 1px solid rgba(255, 255, 255, 0.15); padding: 0 15px; }}
    [data-testid="column"]:last-child {{ border-right: none; }}

    .fifa-card {{
        background: linear-gradient(135deg, rgba(35, 35, 35, 0.95) 0%, rgba(5, 5, 5, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 12px 24px rgba(0,0,0,0.7);
        margin-bottom: 25px;
    }}

    .captain-img {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #cc0000;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(204, 0, 0, 0.4);
    }}

    .card-title {{ font-family: 'WuerthExtra'; font-size: 26px; text-transform: uppercase; line-height: 1; margin-bottom: 5px; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 16px; color: #ddd !important; margin-bottom: 15px; }}
    
    .info-box {{
        background-color: rgba(204, 0, 0, 0.15);
        border-radius: 10px;
        padding: 10px;
        border: 1px solid rgba(204, 0, 0, 0.3);
    }}
    .pts-label {{ font-family: 'WuerthBook'; font-size: 13px; color: #aaa !important; }}
    .big-num {{ font-family: 'WuerthExtra'; font-size: 28px; color: #fff !important; }}

    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 38px;
        border-bottom: 3px solid #cc0000; margin-bottom: 25px; padding-bottom: 5px;
    }}

    .highlight-gold {{ border: 3px solid #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.4); }}
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES DE APOYO ---

def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except: return None

def draw_card(equipo, capitan, score_raw, border_class=""):
    img_src = None
    # Buscador de imágenes flexible
    if isinstance(capitan, str):
        capitan_clean = capitan.strip()
        archivos_en_repo = os.listdir(".")
        for archivo in archivos_en_repo:
            # Comparamos nombre sin extensión ignorando mayúsculas
            nombre_base, ext = os.path.splitext(archivo)
            if nombre_base.lower() == capitan_clean.lower() and ext.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                img_src = get_image_base64(archivo)
                break
    
    if not img_src: 
        img_src = "https://cdn-icons-png.flaticon.com/512/3237/3237472.png"

    st.markdown(f"""
    <div class="fifa-card {border_class}">
        <img src="{img_src}" class="captain-img">
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="info-box">
            <span class="pts-label">PUNTOS ACUMULADOS</span><br>
            <span class="big-num">{int(score_raw) if pd.notna(score_raw) else 0} PTS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
c1, c2 = st.columns([1.5, 6])
logo_file = next((f for f in os.listdir(".") if "logo" in f.lower() and f.endswith((".png", ".jpg", ".jpeg"))), None)

with c1:
    if logo_file: st.image(logo_file, use_container_width=True)
    else: st.markdown("<div style='font-size: 80px; text-align: center;'>🏆</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Resultados")

# --- 4. CARGA Y LÓGICA ---
archivo = "Planilla_Wurth_World_Cup_2026.xlsx"
if os.path.exists(archivo):
    df = pd.read_excel(archivo)
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos[i % 4] for i in range(len(df))]
    
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    for g in grupos:
        mask = df['Grupo'] == g
        for kpi, pts in reglas.items():
            if df.loc[mask, kpi].max() > 0:
                max_val = df.loc[mask, kpi].max()
                ganadores = df[mask][df[mask][kpi] == max_val].index
                df.loc[ganadores, 'Puntos_Fase2'] += pts

    df = df.sort_values(by=['Grupo', 'Puntos_Fase2'], ascending=[True, False])
    df['Destino'] = df.groupby('Grupo').cumcount().apply(lambda x: 'Mundial' if x == 0 else 'Confederaciones')

    t1, t2, t3, t4 = st.tabs(["📢 SORTEO", "⚔️ GRUPOS", "🏆 MUNDIAL", "🥈 CONFEDERACIONES"])
    
    with t1:
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].rename(columns={'F1_Venta_23_Ene_Porcentaje': 'Resultado'}), hide_index=True, use_container_width=True, height=480)

    with t2:
        cols = st.columns(4)
        for i, g in enumerate(grupos):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {g}</div>", unsafe_allow_html=True)
                for _, r in df[df['Grupo'] == g].iterrows():
                    borde = "highlight-gold" if r['Destino'] == 'Mundial' else ""
                    draw_card(r['Equipo'], r['Capitan'], r['Puntos_Fase2'], borde)

    with t3:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        df_m = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        st.dataframe(df_m[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], use_container_width=True, hide_index=True)

    with t4:
        st.markdown("## 🥈 COPA CONFEDERACIONES")
        df_c = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        st.dataframe(df_c[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']], use_container_width=True, hide_index=True)
else:
    st.error("Archivo no encontrado.")
