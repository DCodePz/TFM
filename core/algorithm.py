from core.distance import distancia
from core.config import FACTOR_VACIO
from core.tasks import agrupar_tareas, cargar_tareas
from core.workers import cargar_operarios

def seleccionar_mejor_tarea(op, pendientes):
    return min(
        pendientes,
        key=lambda t:
            distancia(op["pos_x"], op["pos_y"], t["pickup_x"], t["pickup_y"]) * FACTOR_VACIO +
            distancia(t["pickup_x"], t["pickup_y"], t["dropoff_x"], t["dropoff_y"])
    )

def ejecutar_algoritmo(group_tareas):
    tareas_df = cargar_tareas()
    operarios_df = cargar_operarios()

    pendientes = agrupar_tareas(tareas_df, group_tareas)
    operarios = operarios_df.to_dict("records")

    while pendientes:
        for op in operarios:
            if not pendientes:
                break

            tareas_directas = [
                t for t in pendientes
                if t["pickup_x"] == op["pos_x"]
                and t["pickup_y"] == op["pos_y"]
            ]

            if tareas_directas:
                mejor = seleccionar_mejor_tarea(op, tareas_directas)

            else:
                mejor = seleccionar_mejor_tarea(op, pendientes)

                costo_vacio = distancia(op["pos_x"], op["pos_y"], mejor["pickup_x"], mejor["pickup_y"]) * FACTOR_VACIO

                if costo_vacio > 0:
                    op["acciones"].append({
                        "tipo": "Vacío",
                        "origen": (op["pos_x"], op["pos_y"]),
                        "destino": (mejor["pickup_x"], mejor["pickup_y"]),
                        "coste": costo_vacio
                    })
            
            pendientes.remove(mejor)

            transporte = distancia(
                mejor["pickup_x"], mejor["pickup_y"],
                mejor["dropoff_x"], mejor["dropoff_y"]
            )

            op["acciones"].append({
                "tipo": "Tarea",
                "task_ids": mejor["task_id"],
                "origen": (mejor["pickup_x"], mejor["pickup_y"]),
                "destino": (mejor["dropoff_x"], mejor["dropoff_y"]),
                "coste": transporte
            })

            op["pos_x"] = mejor["dropoff_x"]
            op["pos_y"] = mejor["dropoff_y"]

    return operarios