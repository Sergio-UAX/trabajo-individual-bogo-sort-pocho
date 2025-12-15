import random

def esta_ordenado(lista):
    """
    Verifica si una lista está ordenada ascendentemente.
    Demuestra: Bucle 'for', acceso por índice y condicional 'if'.
    """
    # Recorremos desde el primero hasta el penúltimo elemento
    for i in range(len(lista) - 1):
        # Condicional: Si el actual es mayor que el siguiente, no está ordenado
        if lista[i] > lista[i + 1]:
            return False
    return True

def mezclar_lista(lista):
    """
    Mezcla los elementos de la lista aleatoriamente (in-place).
    Demuestra: Manipulación de colecciones.
    """
    random.shuffle(lista)

#arr pirata