from .helpers import esta_ordenado, mezclar_lista
import time

def bogo_sort(lista):
    """
    Algoritmo principal.
    Demuestra: Uso de bucle 'while' para control de flujo.
    """
    intentos = 0
    
    # BUCLE: Mientras la lista NO esté ordenada, seguimos mezclando
    while not esta_ordenado(lista):
        mezclar_lista(lista)
        intentos += 1
        
        # Opcional: Imprimir estado cada 50 intentos para no saturar la consola
        if intentos % 50 == 0:
            print(f"Intento {intentos}: {lista}")
            
    return lista, intentos

#arr pirata