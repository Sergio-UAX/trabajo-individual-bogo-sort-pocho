from .helpers import esta_ordenado, mezclar_lista
import time

def bogo_sort(lista):
    #Algoritmo principal. Realiza el ordenamiento de la lista utilizando el método Bogo Sort (el mejor de todos de lejos).
    intentos = 0
    
    #Mientras que la lista no esté ordenada, sigue mezclándola
    while not esta_ordenado(lista):
        mezclar_lista(lista)
        intentos += 1
        
        # Imprimir estado cada 50 intentos para no saturar la consola (tips de la ia)
        if intentos % 50 == 0:
            print(f"Intento {intentos}: {lista}")
            
    return lista, intentos

#arr pirata