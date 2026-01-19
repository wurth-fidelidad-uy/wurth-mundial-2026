import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# ==============================================================================
# 🎨 ESTILOS CSS Y FUENTES LOCALES
# ==============================================================================
ESTADIO_BG = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* 1. Fuentes Personalizadas */
    @font-face {{ font-family: 'WuerthExtra'; src: url('WuerthExtraBoldCond.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBold'; src: url('WuerthBold.ttf') format('truetype'); }}
    @font-face {{ font-family: 'WuerthBook'; src: url('WuerthBook.ttf') format('truetype'); }}

    /* 2. Estilos Generales */
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

    /* 3. Fondo de Estadio */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url('{ESTADIO_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 4. Separadores Verticales */
    [data-testid="column"] {{
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        padding-right: 15px; padding-left: 15px;
    }}
    [data-testid="column"]:last-child {{ border-right: none; }}

    /* 5. Tarjetas */
    .fifa-card {{
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 25px;
        transition: transform 0.2s;
        position: relative; /* Para posicionar elementos */
    }}
    .fifa-card:hover {{ transform: scale(1.02); border-color: #cc0000; }}

    /* FOTO DEL CAPITÁN */
    .captain-img {{
        width: 100px;
        height: 100px;
        border-radius: 50%; /* Círculo perfecto */
        object-fit: cover; /* Ajustar imagen sin estirar */
        border: 3px solid #cc0000; /* Borde rojo Würth */
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }}

    .card-title {{ 
        font-family: 'WuerthExtra'; font-size: 22px; text-transform: uppercase; color: #fff !important; margin-bottom: 2px; line-height: 1.1;
    }}
    
    /* ESTILO PJ (Partidos Jugados) - FUERA DEL CUADRO */
    .pj-text {{
        font-family: 'WuerthBold';
        font-size: 12px;
        color: #aaa !important; /* Gris claro */
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .card-subtitle {{ 
        font-family: 'WuerthBold'; font-size: 15px; color: #fff !important; margin-bottom: 10px; 
    }}
    
    /* Caja de Estadísticas */
    .stat-box {{ 
        background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 8px; margin-top: 5px; border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .group-header {{
        text-align: center; font-family: 'WuerthExtra'; font-size: 35px; color: white;
        border-bottom: 3px solid #cc0000; margin-bottom: 20px; padding-bottom: 5px;
        text-shadow: 2px 2px 4px #000;
    }}

    /* Fondo transparente para tablas */
    .stDataFrame {{ background-color: rgba(0,0,0,0.6) !important; }}
</style>
""", unsafe_allow_html=True)

# --- 3. FUNCIONES AUXILIARES ---

def format_score(val):
    if pd.isna(val) or val == "": return "-"
    if isinstance(val, float) and val.is_integer(): return int(val)
    return val

def get_image_base64(path):
    """Convierte una imagen local a base64 para que HTML la pueda leer."""
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except Exception:
        return None

def draw_card(equipo, capitan, score_raw, label_score, pj_actual=None, total_fechas=None, border_class=""):
    score_display = format_score(score_raw)
    
    # 1. BUSCAR IMAGEN DEL CAPITÁN
    # Busca un archivo que se llame igual que el capitán (ej: "Juan Perez.jpg")
    img_src = None
    extensions = [".png", ".jpg", ".jpeg", ".webp"]
    
    if isinstance(capitan, str): # Aseguramos que capitan sea texto
        for ext in extensions:
            possible_file = f"{capitan.strip()}{ext}"
            if os.path.exists(possible_file):
                img_src = get_image_base64(possible_file)
                break
    
    # Si no encuentra foto, usa una silueta genérica
    if img_src is None:
        # Silueta SVG en base64
        img_src = "https://cdn-icons-png.flaticon.com/512/3237/3237472.png" 

    # 2. TEXTO PJ
    html_pj = ""
    if pj_actual is not None:
        html_pj = f"""<div class="pj-text">PJ: {pj_actual} / {total_fechas}</div>"""

    # 3. CONSTRUCCIÓN HTML
    card_html = f"""
    <div class="fifa-card {border_class}">
        <img src="{img_src}" class="captain-img">
        
        <div class="card-title">{equipo}</div>
        {html_pj}
        <div class="card-subtitle">{capitan}</div>
        
        <div class="stat-box">
            <span style="color: #eee; font-family: 'WuerthBook'; font-size: 13px;">{label_score}</span><br>
            <strong style="color: #fff; font-size: 26px; font-family: 'WuerthBold';">{score_display}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- 4. HEADER INTELIGENTE ---
c1, c2 = st.columns([1.5, 6])
logo_encontrado = None
for archivo in os.listdir("."):
    if "logo" in archivo.lower() and (archivo.endswith(".png") or archivo.endswith(".jpg")):
        logo_encontrado = archivo
        break

with c1:
    if logo_encontrado:
        st.image(logo_encontrado, use_container_width=True)
    else:
        st.markdown("<div style='font-size: 80px; text-align: center;'>🏆</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- 5. LÓGICA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except FileNotFoundError:
    st.error(f"⚠️ ERROR: No encuentro '{archivo_excel}'. Súbelo a GitHub.")
    datos_cargados = False

if datos_cargados:
    # CALCULO PJ
    cols_juego = ['F2_Workout_Week_Score', 'F2_Sales_Battle_2_Score', 'F2_Customer_Month_Score', 'F2_Clientes_Compradores_Score']
    total_fechas = len(cols_juego)
    fechas_jugadas = 0
    for col in cols_juego:
        if df[col].max() > 0:
            fechas_jugadas += 1

    # CLASIFICACIÓN
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
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- 6. VISUALIZACIÓN ---
    tab1, tab2, tab_mundial, tab_conf = st.tabs(["📢 FASE 1: SORTEO", "⚔️ FASE 2: GRUPOS", "🏆 FINAL: MUNDIAL", "🥈 FINAL: CONFEDERACIONES"])
    
    # --- PESTAÑA 1 ---
    with tab1:
        st.markdown("### 📊 Ranking Inicial")
        df_display = df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo')
        df_display = df_display.rename(columns={'F1_Venta_23_Ene_Porcentaje': 'Resultado Final', 'Capitan': 'Capitán'})
        altura_tabla = (len(df_display) + 1) * 38 
        st.dataframe(df_display, hide_index=True, use_container_width=True, height=altura_tabla)

    # --- PESTAÑA 2 ---
    with tab2:
        st.markdown("### ⚔️ Fase de Grupos")
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"<div class='group-header'>GRUPO {grupo}</div>", unsafe_allow_html=True)
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(
                        equipo=row['Equipo'], 
                        capitan=row['Capitan'], 
                        score_raw=row['Puntos_Fase2'], 
                        label_score="Puntos Totales",
                        pj_actual=fechas_jugadas,
                        total_fechas=total_fechas,
                        border_class=estilo
                    )

    # --- PESTAÑA 3 ---
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
                st.write("Tabla de Posiciones:")
                df_show = df_mundial[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
                df_show = df_show.rename(columns={'F3_Pedidos_Por_Dia': 'Pedidos por Día', 'Capitan': 'Capitán'})
                df_show['Pedidos por Día'] = df_show['Pedidos por Día'].apply(format_score)
                altura_mundial = (len(df_show) + 1) * 38
                st.dataframe(df_show, hide_index=True, use_container_width=True, height=altura_mundial)

    # --- PESTAÑA 4 ---
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
            st.write("Tabla General:")
            df_show = df_conf[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
            df_show = df_show.rename(columns={'F3_Pedidos_Por_Dia': 'Pedidos por Día', 'Capitan': 'Capitán'})
            df_show['Pedidos por Día'] = df_show['Pedidos por Día'].apply(format_score)
            altura_conf = (len(df_show) + 1) * 38
            st.dataframe(df_show, hide_index=True, use_container_width=True, height=altura_conf)
