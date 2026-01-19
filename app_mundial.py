import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS (DISEÑO INSTITUCIONAL + FUENTES)
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* Fuentes Personalizadas Würth */
    @font-face {{ font-family: 'WuerthExtra'; src: url('WuerthExtraBoldCond.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBold'; src: url('WuerthBold.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBook'; src: url('WuerthBook.ttf') format('truetype'); }}

    /* Estilos Generales */
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

    /* Fondo de Estadio */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('{ESTADIO_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Separadores Verticales en Columnas */
    [data-testid="column"] {{
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        padding-right: 15px; padding-left: 15px;
    }}
    [data-testid="column"]:last-child {{ border-right: none; }}

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

    .card-title {{ font-family: 'WuerthExtra'; font-size: 26px; text-transform: uppercase; color: #fff !important; margin-bottom: 5px; }}
    .card-subtitle {{ font-family: 'WuerthBold'; font-size: 16px; color: #ddd !important; margin-bottom: 15px; }}
    .stat-box {{ background-color: rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; color: white;
        border-bottom: 3px solid #cc0000; margin-bottom: 20px; padding-bottom: 5px;
    }}

    .stDataFrame {{ background-color: rgba(0,0,0,0.6) !important; }}
    .highlight-gold {{ border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important; }}
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES AUXILIARES ---

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
        <div class="stat-box">
            <span style="color: #eee; font-family: 'WuerthBook'; font-size: 14px;">{label_score}</span><br>
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
        st.markdown("<div style='font-size: 80px; text-align: center;'>🏆</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- 4. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except FileNotFoundError:
    st.error(f"⚠️ ERROR: No encuentro '{archivo_excel}'.")
    datos_cargados = False

if datos_cargados:
    # Procesamiento y Sorteo
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # Cálculo de Puntos
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

    # Definición de Clasificados
    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- 5. VISUALIZACIÓN EN PESTAÑAS ---
    tab1, tab2, tab_mundial, tab_conf, tab_externo = st.tabs([
        "📢 SORTEO", 
        "⚔️ GRUPOS", 
        "🏆 MUNDIAL", 
        "🥈 CONFEDERACIONES", 
        "🖼️ EQUIPOS"
    ])
    
    with tab1:
        st.markdown("### 📊 Ranking Inicial")
        df_display = df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo')
        df_display = df_display.rename(columns={'F1_Venta_23_Ene_Porcentaje': 'Resultado Final', 'Capitan': 'Capitán'})
        st.dataframe(df_display, hide_index=True, use_container_width=True, height=(len(df_display)+1)*38)

    with tab2:
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {grupo}</div>", unsafe_allow_html=True)
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)

    with tab_mundial:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        df_mundial = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        if not df_mundial.empty:
            best = df_mundial.iloc[0]
            val = best['F3_Pedidos_Por_Dia']
            hay_campeon = pd.notna(val) and val > 0
            
            c1, c2 = st.columns([1, 2])
            with c1:
                if hay_campeon:
                    st.markdown("### 🥇 ¡CAMPEÓN!")
                    st.balloons()
                    draw_card(best['Equipo'], best['Capitan'], val, "Pedidos/Día", "highlight-gold")
                else:
                    st.markdown("### ⏳ Esperando...")
                    draw_card(best['Equipo'], best['Capitan'], val, "Pedidos/Día")
            with c2:
                df_show = df_mundial[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
                df_show = df_show.rename(columns={'F3_Pedidos_Por_Dia': 'Pedidos por Día', 'Capitan': 'Capitán'})
                df_show['Pedidos por Día'] = df_show['Pedidos por Día'].apply(format_score)
                st.dataframe(df_show, hide_index=True, use_container_width=True)

    with tab_conf:
        st.markdown("## 🥈 FINAL COPA CONFEDERACIONES")
        df_conf = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        if not df_conf.empty:
            c1, c2, c3 = st.columns(3)
            top3 = df_conf.head(3)
            medals = ["🥇 Oro", "🥈 Plata", "🥉 Bronce"]
            classes = ["highlight-gold", "highlight-silver", "highlight-bronze"]
            for i in range(len(top3)):
                row = top3.iloc[i]
                val = row['F3_Pedidos_Por_Dia']
                estilo = classes[i] if (pd.notna(val) and val > 0) else ""
                with [c1, c2, c3][i]:
                    st.markdown(f"<h4 style='text-align:center'>{medals[i]}</h4>", unsafe_allow_html=True)
                    draw_card(row['Equipo'], row['Capitan'], val, "Pedidos/Día", estilo)
            st.divider()
            df_show = df_conf[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
            df_show = df_show.rename(columns={'F3_Pedidos_Por_Dia': 'Pedidos por Día', 'Capitan': 'Capitán'})
            df_show['Pedidos por Día'] = df_show['Pedidos por Día'].apply(format_score)
            st.dataframe(df_show, hide_index=True, use_container_width=True)

    with tab_externo:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 80px;'>
                <h2 style='
                    color: white !important; 
                    font-family: "WuerthExtra"; 
                    font-size: 45px; 
                    text-shadow: 2px 4px 8px rgba(0,0,0,0.8);
                    margin-bottom: 50px;
                '>
                    ⚽ EQUIPOS Y FORMACIONES
                </h2>
                
                <a href="http://www.wurth.com.uy" target="_blank" style="text-decoration: none;">
                    <div style='
                        display: inline-block;
                        padding: 22px 55px;
                        background-color: #cc0000;
                        border-radius: 50px;
                        border: 2px solid white;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                    '>
                        <span style='
                            color: white !important; 
                            font-family: "WuerthExtra"; 
                            font-size: 24px;
                            text-decoration: none !important;
                        '>
                            VER LA TARJETA DE CADA EQUIPO <span style="margin-left:12px;">🔗</span>
                        </span>
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)
