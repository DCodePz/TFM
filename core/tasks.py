import pandas as pd
import sqlite3
from core.config import DB_PATH


def cargar_tareas():
    """
    Carga las tareas desde la base de datos SQLite y aplica filtros de limpieza.

    Returns:
        pd.DataFrame: DataFrame con las tareas filtradas:
            - Elimina tareas con mismo origen y destino (pickup == dropoff)
            - Elimina tareas ya asignadas (assigned_to no es NaN)
    """

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect(DB_PATH)

    try:
        # Consulta SQL para obtener todas las tareas
        query = "SELECT * FROM TASKS"
        tareas_df = pd.read_sql_query(query, conn)

    finally:
        # Asegura el cierre de la conexión aunque haya errores
        conn.close()

    # ---------------------------------------------------------
    # FILTRO 1: eliminar tareas con origen == destino
    # ---------------------------------------------------------
    tareas_df = tareas_df[
        ~(
            (tareas_df[["pickup_x", "pickup_y"]].values ==
            tareas_df[["dropoff_x", "dropoff_y"]].values).all(axis=1)
        )
    ]

    # ---------------------------------------------------------
    # FILTRO 2: eliminar tareas ya asignadas a un operario
    # (solo dejamos tareas con assigned_to = NULL)
    # ---------------------------------------------------------
    tareas_df = tareas_df[tareas_df["assigned_to"].isna()]

    return tareas_df


def agrupar_tareas(tareas_df, group_tareas):
    """
    Agrupa tareas por origen y destino.

    Args:
        tareas_df (pd.DataFrame): DataFrame con tareas limpias.
        group_tareas: Tamaño máximo de los grupos de tareas.

    Returns:
        list[dict]: Lista de grupos de tareas donde cada grupo contiene:
            - pickup_x, pickup_y
            - dropoff_x, dropoff_y
            - task_id (lista de IDs de tareas agrupadas)
    """

    grouped = tareas_df.groupby(
        ["pickup_x", "pickup_y", "dropoff_x", "dropoff_y"],
        as_index=False
    ).agg(task_id=("task_id", list))

    result = []

    for row in grouped.to_dict("records"):
        task_ids = row["task_id"]

        # dividir en chunks
        for i in range(0, len(task_ids), group_tareas):
            chunk = task_ids[i:i + group_tareas]

            result.append({
                "pickup_x": row["pickup_x"],
                "pickup_y": row["pickup_y"],
                "dropoff_x": row["dropoff_x"],
                "dropoff_y": row["dropoff_y"],
                "task_id": chunk
            })

    return result