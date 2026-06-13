import pandas as pd
import sqlite3
from core.config import DB_PATH


def cargar_operarios():
    """
    Carga todos los operarios desde la base de datos SQLite.

    Esta función se conecta a la base de datos definida en DB_PATH,
    ejecuta una consulta SQL sobre la tabla WORKERS y devuelve los
    datos como un DataFrame de pandas.

    Returns:
        pd.DataFrame: DataFrame con todos los registros de la tabla WORKERS.
            Cada fila representa un operario con sus atributos.
    """

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect(DB_PATH)

    try:
        # Consulta SQL para obtener todos los operarios
        query = "SELECT * FROM WORKERS"
        operarios_df = pd.read_sql_query(query, conn)

    finally:
        # Asegura el cierre de la conexión aunque haya errores
        conn.close()

    # ---------------------------------------------------------
    # COLUMNAS NUEVAS
    # ---------------------------------------------------------

    # Inicializamos acciones como lista vacía
    operarios_df["acciones"] = [[] for _ in range(len(operarios_df))]

    return operarios_df

def guardar_operarios(operarios):
    operarios = operarios[["operario", "pos_x", "pos_y"]]
    data = list(operarios.itertuples(index=False, name=None))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. borrar todo lo anterior
    cur.execute("DELETE FROM WORKERS")

    # 2. insertar nuevos valores
    cur.executemany("""
        INSERT INTO WORKERS (operario, pos_x, pos_y)
        VALUES (?, ?, ?)
    """, data)

    conn.commit()
    conn.close()
    

def devolver_acciones(operario, num_tareas, mostrar_vacios):
    if mostrar_vacios:
        acciones = operario["acciones"]
    else:
        acciones = [a for a in operario["acciones"] if a["tipo"] == "Tarea"]

    if num_tareas == 0:
        return acciones
    
    return acciones[:num_tareas]