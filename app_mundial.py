import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# --- ESTILOS CSS (FONDO DE ESTADIO + TARJETAS PREMIUM) ---
ESTADIO_URL = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* 1. Fondo de Estadio */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url('{ESTADIO_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    /* 2. Tarjetas con efecto Vidrio */
    .fifa-card {{
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(0, 0, 0, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        backdrop-filter: blur(5px);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }}
    .fifa-card:hover {{ transform: translateY(-5px); border-color: #cc0000; }}

    /* Textos */
    .card-title {{ font-size: 20px; font-weight: 800; text-transform: uppercase; color: #fff; margin-bottom: 5px; }}
    .card-subtitle {{ font-size: 14px; color: #ccc; margin-bottom: 15px; font-style: italic; }}
    
    /* Cajas de Estadísticas */
    .stat-box {{ 
        background-color: rgba(255, 255, 255, 0.08); 
        border-radius: 8px; padding: 10px; 
        font-size: 14px; margin-top: 10px; border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    /* Bordes de Medallas */
    .highlight-gold {{ border: 2px solid #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.3); }}
    .highlight-silver {{ border: 2px solid #C0C0C0; box-shadow: 0 0 25px rgba(192, 192, 192, 0.3); }}
    .highlight-bronze {{ border: 2px solid #CD7F32; box-shadow: 0 0 25px rgba(205, 127, 50, 0.3); }}
    
    /* Ajustes generales */
    h1, h2, h3 {{ color: white !important; text-shadow: 0 2px 4px rgba(0,0,0,0.8); }}
    .stDataFrame {{ background-color: rgba(0,0,0,0.6); border-radius: 10px; padding: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN AUXILIAR: LIMPIAR VALORES ---
def format_score(val):
    """Convierte NaN o vacíos en un guion '-'"""
    if pd.isna(val) or val == "":
        return "-"
    # Si es número, lo formateamos bonito (sin decimales .0 innecesarios)
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val

# --- FUNCIÓN PARA DIBUJAR TARJETA ---
def draw_card(equipo, capitan, score_raw, label_score, border_class=""):
    score_display = format_score(score_raw)
    
    card_html = f"""
    <div class="fifa-card {border_class}">
        <div style="font-size: 45px; margin-bottom: 10px;">👕</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <span style="color: #aaa; font-size: 12px;">{label_score}</span><br>
            <strong style="font-size: 20px;">{score_display}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([1, 6])
with c1:
    st.markdown("<div style='font-size: 60px; text-align: center;'>🏆</div>", unsafe_allow_html=True)
with c2:
    st.title("WÜRTH WORLD CUP 2026")
    st.markdown("##### ⚽ Tablero Oficial de Competencia")

# --- CARGA DE DATOS ---
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"
try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except FileNotFoundError:
    st.error(f"⚠️ No se encuentra el archivo: {archivo_excel}")
    datos_cargados = False

if datos_cargados:
    # --- PROCESAMIENTO ---
    # 1. Asignar grupos
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # 2. Puntos Fase 2
    df['Puntos_Fase2'] = 0
    reglas = {'F2_Workout_Week_Score': 3, 'F2_Sales_Battle_2_Score': 2, 'F2_Customer_Month_Score': 4, 'F2_Clientes_Compradores_Score': 5}
    
    for grupo in grupos_labels:
        mask = df['Grupo'] == grupo
        df_g = df[mask]
        for kpi, pts in reglas.items():
            max_val = df_g[kpi].max()
            if max_val > 0: # Si hay datos
                ganadores = df_g[df_g[kpi] == max_val].index
                df.loc[ganadores, 'Puntos_Fase2'] += pts

    # 3. Destinos
    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- VISUALIZACIÓN EN 4 PESTAÑAS ---
    # Definimos las pestañas nuevas
    tab1, tab2, tab_mundial, tab_conf = st.tabs(["📢 FASE 1: SORTEO", "⚔️ FASE 2: GRUPOS", "🏆 FINAL: MUNDIAL", "🥈 FINAL: CONFEDERACIONES"])
    
    # --- PESTAÑA 1: SORTEO ---
    with tab1:
        st.markdown("### 📊 Ranking Inicial (Objetivo Especial)")
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True, use_container_width=True)

    # --- PESTAÑA 2: GRUPOS ---
    with tab2:
        st.markdown("### ⚔️ Fase de Grupos")
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"#### GRUPO {grupo}")
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], row['Puntos_Fase2'], "Puntos Totales", estilo)
        st.caption("🟡 Borde Dorado: Clasifica al Mundial | ⚪ Sin Borde: Pasa a Copa Confederaciones")

    # --- PESTAÑA 3: COPA DEL MUNDO ---
    with tab_mundial:
        st.markdown("## 🌍 FINAL COPA DEL MUNDO")
        st.info("Participan únicamente los 1° de cada grupo. Gana quien tenga más Pedidos por Día.")
        
        df_mundial = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        
        if not df_mundial.empty:
            # Mostrar Campeón Grande
            best = df_mundial.iloc[0]
            # Solo celebramos si hay un dato real (mayor a 0 y no NaN)
            val_campeon = best['F3_Pedidos_Por_Dia']
            hay_campeon = pd.notna(val_campeon) and val_campeon > 0

            col_center, col_rest = st.columns([1, 2])
            
            with col_center:
                if hay_campeon:
                    st.markdown("### 🥇 ¡CAMPEÓN!")
                    st.balloons()
                    draw_card(best['Equipo'], best['Capitan'], val_campeon, "Pedidos/Día", "highlight-gold")
                else:
                    st.markdown("### ⏳ Esperando Resultados...")
                    draw_card(best['Equipo'], best['Capitan'], val_campeon, "Pedidos/Día")

            with col_rest:
                st.write("Tabla de Posiciones:")
                # Preparamos tabla bonita para mostrar "-" si es NaN
                df_show = df_mundial[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
                df_show['F3_Pedidos_Por_Dia'] = df_show['F3_Pedidos_Por_Dia'].apply(format_score)
                st.dataframe(df_show, hide_index=True, use_container_width=True)

    # --- PESTAÑA 4: COPA CONFEDERACIONES ---
    with tab_conf:
        st.markdown("## 🥈 FINAL COPA CONFEDERACIONES")
        st.info("Participan los 2° y 3° de cada grupo (8 equipos). Se premia al Top 3.")

        df_conf = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
        
        if not df_conf.empty:
            # Top 3
            c1, c2, c3 = st.columns(3)
            top3 = df_conf.head(3)
            medals = ["🥇 Oro", "🥈 Plata", "🥉 Bronce"]
            classes = ["highlight-gold", "highlight-silver", "highlight-bronze"]
            
            for i in range(len(top3)):
                row = top3.iloc[i]
                val = row['F3_Pedidos_Por_Dia']
                # Chequear si hay datos reales para mostrar colores
                real_data = pd.notna(val) and val > 0
                estilo = classes[i] if real_data else ""
                
                with [c1, c2, c3][i]:
                    st.markdown(f"<h4 style='text-align:center'>{medals[i]}</h4>", unsafe_allow_html=True)
                    draw_card(row['Equipo'], row['Capitan'], val, "Pedidos/Día", estilo)

            st.divider()
            st.write("Tabla General:")
            df_show_conf = df_conf[['Equipo', 'Capitan', 'F3_Pedidos_Por_Dia']].copy()
            df_show_conf['F3_Pedidos_Por_Dia'] = df_show_conf['F3_Pedidos_Por_Dia'].apply(format_score)
            st.dataframe(df_show_conf, hide_index=True, use_container_width=True)
