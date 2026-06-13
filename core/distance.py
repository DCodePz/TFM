def distancia(x1, y1, x2, y2):
    """
    Calcula la distancia Manhattan entre dos puntos en un plano 2D.

    La distancia Manhattan es la suma de las diferencias absolutas
    entre las coordenadas en X e Y. Es decir, mide el recorrido
    en una cuadrícula (sin diagonales).

    Args:
        x1 (int | float): Coordenada X del primer punto.
        y1 (int | float): Coordenada Y del primer punto.
        x2 (int | float): Coordenada X del segundo punto.
        y2 (int | float): Coordenada Y del segundo punto.

    Returns:
        int | float: Distancia Manhattan entre los dos puntos.
    """

    return abs(x2 - x1) + abs(y2 - y1)