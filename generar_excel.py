import pandas as pd

# Definimos las columnas exactas que leerá el programa
# Se incluyen 12 filas de ejemplo para los 12 equipos
data = {
    "Equipo": [f"Equipo {i}" for i in range(1, 13)],
    "Capitan": [f"Capitán {i}" for i in range(1, 13)],
    
    # --- FASE 1: Sorteo y Grupos ---
    # Dato del 23/1 para definir quién va a qué grupo (A, B, C o D)
    "F1_Venta_23_Ene_Porcentaje": [0.0] * 12,       

    # --- FASE 2: Fase de Grupos (14 Puntos en Juego) ---
    # Puntos que saca el equipo en cada campaña (llenar con el valor real del KPI)
    "F2_Workout_Week_Score": [0.0] * 12,            # Gana 3 pts el mejor del grupo
    "F2_Sales_Battle_2_Score": [0.0] * 12,          # Gana 2 pts el mejor del grupo
    "F2_Customer_Month_Score": [0.0] * 12,          # Gana 4 pts el mejor del grupo
    "F2_Clientes_Compradores_Score": [0.0] * 12,    # Gana 5 pts el mejor del grupo
    
    # Criterio de desempate para Fase 2
    "F2_TieBreak_Nuevos_Clientes": [0] * 12,      

    # --- FASE 3: Finales (Mundial y Confederaciones) ---
    # KPI único "Pedidos por Día" para definir a los campeones
    "F3_Pedidos_Por_Dia": [0.0] * 12                
}

# Crear el DataFrame y guardar en Excel
df = pd.DataFrame(data)
nombre_archivo = "Planilla_Wurth_World_Cup_2026.xlsx"
df.to_excel(nombre_archivo, index=False)

print(f"✅ Archivo '{nombre_archivo}' generado exitosamente.")
print("Ahora puedes abrirlo, cargar los datos reales y subirlo a GitHub.")
