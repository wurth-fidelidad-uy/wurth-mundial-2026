import streamlit as st
import pandas as pd

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

# --- CARGA DE DATOS ---
uploaded_file = st.file_uploader("Cargar Planilla Excel Oficial", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # ---------------- LÓGICA DE NEGOCIO ----------------
    
    # 1. FASE 1 Y ASIGNACIÓN DE GRUPOS
    # Ordenar por % Venta 23 Ene
    df = df.sort_values(by="F1_Venta_23_Ene_Porcentaje", ascending=False).reset_index(drop=True)
    grupos_labels = ['A', 'B', 'C', 'D']
    # Asignación correlativa: 1->A, 2->B, 3->C, 4->D, 5->A...
    df['Grupo'] = [grupos_labels[i % 4] for i in range(len(df))]
    
    # 2. CÁLCULO DE PUNTOS FASE 2 (14 Pts en juego)
    df['Puntos_Fase2'] = 0
    
    # Reglas de Puntos por Campaña (Gana el mejor de cada grupo)
    reglas_puntos = {
        'F2_Workout_Week_Score': 3,
        'F2_Sales_Battle_2_Score': 2,
        'F2_Customer_Month_Score': 4,
        'F2_Clientes_Compradores_Score': 5
    }
    
    # Iterar por grupo y asignar puntos al mejor de cada KPI
    for grupo in grupos_labels:
        mask_grupo = df['Grupo'] == grupo
        df_g = df[mask_grupo]
        
        for col_kpi, pts in reglas_puntos.items():
            max_score = df_g[col_kpi].max()
            if max_score > 0: # Solo dar puntos si jugaron
                # Sumar puntos a quien tenga el max score (o empate)
                equipos_ganadores = df_g[df_g[col_kpi] == max_score].index
                df.loc[equipos_ganadores, 'Puntos_Fase2'] += pts

    # 3. RANKING FASE 2 (Puntos + Desempate)
    df = df.sort_values(
        by=['Grupo', 'Puntos_Fase2', 'F2_TieBreak_Nuevos_Clientes'], 
        ascending=[True, False, False]
    )
    
    # Determinar posición en el grupo (1, 2, 3)
    df['Posicion_Grupo'] = df.groupby('Grupo').cumcount() + 1
    
    # Determinar a qué copa van
    df['Destino'] = df['Posicion_Grupo'].apply(lambda x: 'Mundial' if x == 1 else 'Confederaciones')

    # ---------------- VISUALIZACIÓN ----------------
    
    tab1, tab2, tab3 = st.tabs(["Fase 1: Sorteo", "Fase 2: Grupos", "Fase 3: Finales"])
    
    with tab1:
        st.header("📢 Asignación de Grupos")
        st.info("Basado en el resultado del 23 de Enero (160% Objetivo Especial)")
        st.dataframe(df[['Equipo', 'Capitan', 'F1_Venta_23_Ene_Porcentaje', 'Grupo']].sort_values('Grupo'))

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
        
        st.caption("*El borde DORADO indica clasificación a la Copa del Mundo.*")

    with tab3:
        st.header("🏁 LA FINAL (Definición por Pedidos/Día)")
        
        # --- COPA DEL MUNDO (Solo los 1ros) ---
        st.subheader("🌍 COPA DEL MUNDO WÜRTH (Top 4)")
        df_mundial = df[df['Destino'] == 'Mundial'].copy()
        # Todos contra todos definido por KPI Final
        df_mundial = df_mundial.sort_values(by='F3_Pedidos_Por_Dia', ascending=False).reset_index(drop=True)
        
        if not df_mundial.empty:
            best_mundial = df_mundial.iloc[0] # El Campeón
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/FIFA_World_Cup_Trophy_%282%29.svg/166px-FIFA_World_Cup_Trophy_%282%29.svg.png", width=100) # Placeholder copa
                st.markdown("### 🥇 CAMPEÓN DEL MUNDO")
                draw_card(best_mundial['Equipo'], best_mundial['Capitan'], best_mundial['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-gold")
                if best_mundial['F3_Pedidos_Por_Dia'] > 0:
                    st.balloons()
            
            with c2:
                st.write("Tabla de Posiciones Final:")
                st.dataframe(df_mundial[['Equipo', 'Capitan', 'Grupo', 'F3_Pedidos_Por_Dia']])

        st.divider()

        # --- COPA CONFEDERACIONES (2dos y 3ros) ---
        st.subheader("🥈 COPA CONFEDERACIONES (8 Equipos)")
        df_conf = df[df['Destino'] == 'Confederaciones'].copy()
        df_conf = df_conf.sort_values(by='F3_Pedidos_Por_Dia', ascending=False).reset_index(drop=True)
        
        if not df_conf.empty:
            c1, c2, c3 = st.columns(3)
            
            # Ganadores Oro, Plata, Bronce
            top_3 = df_conf.head(3)
            
            if len(top_3) > 0:
                with c1:
                    st.markdown("#### 🥇 Oro")
                    r = top_3.iloc[0]
                    draw_card(r['Equipo'], r['Capitan'], r['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-gold")
            if len(top_3) > 1:
                with c2:
                    st.markdown("#### 🥈 Plata")
                    r = top_3.iloc[1]
                    draw_card(r['Equipo'], r['Capitan'], r['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-silver")
            if len(top_3) > 2:
                with c3:
                    st.markdown("#### 🥉 Bronce")
                    r = top_3.iloc[2]
                    draw_card(r['Equipo'], r['Capitan'], r['F3_Pedidos_Por_Dia'], "Pedidos/Día", "highlight-bronze")
            
            st.write("Tabla General Copa Confederaciones:")
            st.dataframe(df_conf[['Equipo', 'Capitan', 'Grupo', 'F3_Pedidos_Por_Dia']])

else:
    st.info("👆 Por favor, carga el archivo Excel para ver los resultados.")
