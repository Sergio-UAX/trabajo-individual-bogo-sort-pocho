import random

def esta_ordenado(lista):
    # Recorre desde el primero hasta el penúltimo elemento para verificar el orden ascendente del bogo
    for i in range(len(lista) - 1):
        # Si el actual es mayor que el siguiente, no está ordenado (;-;)
        if lista[i] > lista[i + 1]:
            return False
    return True

def mezclar_lista(lista):
    #Mezcla los elementos de la lista aleatoriamente (in-place)
    random.shuffle(lista)

#arr atento a navegantes