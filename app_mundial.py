import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# --- ESTILOS CSS (FONDO DE ESTADIO + TARJETAS PREMIUM) ---
# Usamos una imagen de estadio de alta calidad (libre de derechos)
ESTADIO_URL = "https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* 1. Fondo de Estadio con capa oscura para leer bien el texto */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{ESTADIO_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    
    /* 2. Tarjetas con efecto 'Glassmorphism' (Vidrio ahumado) */
    .fifa-card {{
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(0, 0, 0, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }}
    
    .fifa-card:hover {{
        transform: translateY(-5px);
        border-color: #cc0000; /* Detalle rojo al pasar el mouse */
    }}

    /* 3. Tipografía y Detalles */
    .card-title {{ 
        font-size: 20px; 
        font-weight: 900; 
        text-transform: uppercase; 
        color: #fff; 
        letter-spacing: 1px;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}
    .card-subtitle {{ font-size: 14px; color: #ccc; margin-bottom: 15px; font-style: italic; }}
    
    /* Cajas de Estadísticas */
    .stat-box {{ 
        background-color: rgba(255, 255, 255, 0.1); 
        border-radius: 8px; 
        padding: 8px; 
        font-size: 14px; 
        margin-top: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    /* Bordes de Medallas Brillantes */
    .highlight-gold {{ border: 2px solid #FFD700; box-shadow: 0 0 20px rgba(255, 215, 0, 0.4); }}
    .highlight-silver {{ border: 2px solid #C0C0C0; box-shadow: 0 0 20px rgba(192, 192, 192, 0.4); }}
    .highlight-bronze {{ border: 2px solid #CD7F32; box-shadow: 0 0 20px rgba(205, 127, 50, 0.4); }}
    
    /* Ajustes generales de texto para fondo oscuro */
    h1, h2, h3, p, span, div {{ color: white !important; }}
    .stDataFrame {{ background-color: rgba(0,0,0,0.5); border-radius: 10px; padding: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN PARA DIBUJAR TARJETA ---
def draw_card(equipo, capitan, score_principal, label_score, border_class=""):
    card_html = f"""
    <div class="fifa-card {border_class}">
        <div style="font-size: 45px; margin-bottom: 10px;">👕</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <span style="color: #aaa; font-size: 12px;">{label_score}</span><br>
            <strong style="font-size: 18px;">{score_principal}</strong>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- HEADER CON LOGO ---
c1, c2 = st.columns([1, 6])
with c1:
    # Icono de copa (puedes cambiarlo por tu logo si lo subes)
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
    # 1. Ordenar y asignar grupos (A, B, C, D) según venta del 23 Ene
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # 2. Calcular Puntos Fase 2 (14 pts máx)
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

    # 3. Ranking Fase 2 y Destino (Mundial vs Confederaciones)
    df = df.sort_values(by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], ascending=[True, False, False])
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # --- VISUALIZACIÓN ---
    tab1, tab2, tab3 = st.tabs(["📢 FASE 1: SORTEO", "⚔️ FASE 2: GRUPOS", "🏆 FASE 3: FINALES"])
    
    with tab1:
        st.markdown("### 📊 Ranking Inicial (Objetivo Especial)")
        st.markdown("Los equipos se ordenan por su % de venta del 23 de Enero y se distribuyen en los 4 grupos.")
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True, use_container_width=True)

    with tab2:
        st.markdown("### ⚔️ Fase de Grupos")
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.markdown(f"#### GRUPO {grupo}")
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    estilo = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], f"{row['Puntos_Fase2']} pts", "Puntos Acumulados", estilo)

    with tab3:
        st.markdown("### 🏁 La Gran Final")
        col_mundial, col_conf = st.columns(2)
        
        with col_mundial:
            st.markdown("#### 🌍 COPA DEL MUNDO")
            df_mundial = df[df['Destino'] == 'Mundial'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
            if not df_mundial.empty:
                campeon = df_mundial.iloc[0]
                st.markdown(f"### 🥇 ¡CAMPEÓN!")
                draw_card(campeon['Equipo'], campeon['Capitan'], campeon['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-gold")
                if campeon['F3_Pedidos_Por_Dia'] > 0: st.balloons()
                
                st.divider()
                st.write("Tabla de Posiciones:")
                st.dataframe(df_mundial[['Equipo', 'F3_Pedidos_Por_Dia']], hide_index=True)

        with col_conf:
            st.markdown("#### 🥈 COPA CONFEDERACIONES")
            df_conf = df[df['Destino'] == 'Confederaciones'].sort_values('F3_Pedidos_Por_Dia', ascending=False)
            if not df_conf.empty:
                st.write("Podio de Ganadores:")
                c1, c2, c3 = st.columns(3)
                top3 = df_conf.head(3)
                emojis = ["🥇", "🥈", "🥉"]
                clases = ["highlight-gold", "highlight-silver", "highlight-bronze"]
                
                for i in range(len(top3)):
                    with [c1, c2, c3][i]:
                        r = top3.iloc[i]
                        st.markdown(f"<div style='text-align:center; font-size:20px;'>{emojis[i]}</div>", unsafe_allow_html=True)
                        draw_card(r['Equipo'], r['Capitan'], r['F3_Pedidos_Por_Dia'], "Pedidos/Día", clases[i])

            st.divider()
            st.dataframe(df_conf[['Equipo', 'F3_Pedidos_Por_Dia']], hide_index=True)
