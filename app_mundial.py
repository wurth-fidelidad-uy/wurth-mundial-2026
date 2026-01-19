import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth World Cup 2026", layout="wide", page_icon="🏆")

# --- ESTILOS CSS (DISEÑO TARJETAS NEGRAS) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .fifa-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border: 2px solid #333;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.6);
        margin-bottom: 20px;
        color: white;
    }
    .card-title { font-size: 18px; font-weight: bold; text-transform: uppercase; color: #fff; }
    .card-subtitle { font-size: 14px; color: #aaa; margin-bottom: 10px; }
    .stat-box { 
        background-color: #222; border-radius: 5px; padding: 5px; 
        font-size: 12px; margin-top: 5px; border: 1px solid #444; 
    }
    .highlight-gold { border-color: #FFD700; box-shadow: 0 0 10px #FFD700; }
    .highlight-silver { border-color: #C0C0C0; box-shadow: 0 0 10px #C0C0C0; }
    .highlight-bronze { border-color: #CD7F32; box-shadow: 0 0 10px #CD7F32; }
    h1, h2, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN PARA MOSTRAR TARJETA ---
def draw_card(equipo, capitan, score_principal, label_score, border_class=""):
    card_html = f"""
    <div class="fifa-card {border_class}">
        <div style="font-size: 40px;">👕</div>
        <div class="card-title">{equipo}</div>
        <div class="card-subtitle">{capitan}</div>
        <div class="stat-box">
            <strong>{label_score}:</strong> {score_principal}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🏆 WÜRTH WORLD CUP 2026")
st.markdown("### Tablero Oficial de Competencia")

# --- CARGA AUTOMÁTICA DE DATOS ---
# El sistema busca el archivo en el mismo lugar donde está el código
archivo_excel = "Planilla_Wurth_World_Cup_2026.xlsx"

try:
    df = pd.read_excel(archivo_excel)
    datos_cargados = True
except FileNotFoundError:
    st.error(f"⚠️ No se encuentra el archivo de datos: {archivo_excel}")
    st.info("Asegúrate de haber subido el Excel al repositorio de GitHub junto con este código.")
    datos_cargados = False

if datos_cargados:
    # ---------------- LÓGICA DE NEGOCIO ----------------
    
    # 1. FASE 1 Y ASIGNACIÓN DE GRUPOS
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # 2. CÁLCULO DE PUNTOS FASE 2 (14 Pts en juego)
    df['Puntos_Fase2'] = 0
    reglas_puntos = {
        'F2_Workout_Week_Score': 3,
        'F2_Sales_Battle_2_Score': 2,
        'F2_Customer_Month_Score': 4,
        'F2_Clientes_Compradores_Score': 5
    }
    
    for grupo in grupos_labels:
        mask_grupo = df['Grupo'] == grupo
        df_g = df[mask_grupo]
        for col_kpi, pts in reglas_puntos.items():
            max_score = df_g[col_kpi].max()
            if max_score > 0:
                equipos_ganadores = df_g[df_g[col_kpi] == max_score].index
                df.loc[equipos_ganadores, 'Puntos_Fase2'] += pts

    # 3. RANKING FASE 2
    df = df.sort_values(
        by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], 
        ascending=[True, False, False]
    )
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # ---------------- VISUALIZACIÓN PARA EL PÚBLICO ----------------
    
    tab1, tab2, tab3 = st.tabs(["Fase 1: Sorteo", "Fase 2: Grupos", "Fase 3: Finales"])
    
    with tab1:
        st.header("📢 Asignación de Grupos")
        st.info("Ranking basado en Objetivo Especial (23 Ene)")
        # Mostramos una tabla limpia, sin columnas técnicas raras
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'), hide_index=True)

    with tab2:
        st.header("⚔️ Fase de Grupos - Puntos Acumulados")
        cols = st.columns(4)
        for i, grupo in enumerate(grupos_labels):
            with cols[i]:
                st.subheader(f"GRUPO {grupo}")
                df_grupo = df[df['Grupo'] == grupo]
                for _, row in df_grupo.iterrows():
                    borde = "highlight-gold" if row['Destino'] == 'Mundial' else ""
                    draw_card(row['Equipo'], row['Capitan'], f"{row['Puntos_Fase2']} pts", "Total Puntos", borde)
        
    with tab3:
        st.header("🏁 LA FINAL")
        
        col_mundial, col_conf = st.columns(2)
        
        with col_mundial:
            st.subheader("🌍 COPA DEL MUNDO")
            df_mundial = df[df['Destino'] == 'Mundial'].sort_values(by='F3_Pedidos_Por_Dia', ascending=False)
            if not df_mundial.empty:
                campeon = df_mundial.iloc[0]
                st.markdown(f"### 🏆 {campeon['Equipo']}")
                draw_card(campeon['Equipo'], campeon['Capitan'], campeon['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-gold")
                if campeon['F3_Pedidos_Por_Dia'] > 0:
                    st.balloons()
            st.dataframe(df_mundial[['Equipo', 'F3_Pedidos_Por_Dia']], hide_index=True)

        with col_conf:
            st.subheader("🥈 COPA CONFEDERACIONES")
            df_conf = df[df['Destino'] == 'Confederaciones'].sort_values(by='F3_Pedidos_Por_Dia', ascending=False)
            if not df_conf.empty:
                st.write("Top 3:")
                for i in range(min(3, len(df_conf))):
                    row = df_conf.iloc[i]
                    medalla = ["🥇", "🥈", "🥉"][i]
                    st.write(f"{medalla} **{row['Equipo']}** ({row['F3_Pedidos_Por_Dia']} ped/día)")
            st.dataframe(df_conf[['Equipo', 'F3_Pedidos_Por_Dia']], hide_index=True)
