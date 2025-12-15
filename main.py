import pygame
import random
import sys

# --- Función para pedir datos al usuario ---
def obtener_numero_barras():
    """Pide al usuario el número de barras por la terminal."""
    while True:
        try:
            entrada = input(">>> Introduce el número de barras a ordenar (ej: 50, 100, 200): ")
            n = int(entrada)
            if n > 1 and n <= 800: # Límite superior opcional para que se vea bien
                return n
            elif n > 800:
                 print("¡Son demasiadas barras para el ancho de la pantalla! Intenta con menos de 800.")
            else:
                print("Por favor, introduce un número mayor a 1.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")

# --- Configuración Inicial ---
# Pedimos el número ANTES de iniciar Pygame
N = obtener_numero_barras()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(f"Bogo Sort Visualizer - {N} Elementos")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont('Arial', 20)

# --- Funciones del Algoritmo ---

def generar_array(n):
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return arr

def esta_ordenado(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            return False
    return True

def paso_intercambio_aleatorio(arr):
    if esta_ordenado(arr):
        return arr, True, None, None
    else:
        n = len(arr)
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        while i == j and n > 1:
             j = random.randint(0, n - 1)
        
        arr[i], arr[j] = arr[j], arr[i]
        return arr, False, i, j

# --- Funciones de Dibujado ---

def dibujar_barras(arr, color_base, idx_rojo1=None, idx_rojo2=None):
    pantalla.fill(NEGRO)

    # Ancho dinámico según la cantidad de barras elegida por el usuario
    ancho_barra = ANCHO_PANTALLA / len(arr)
    escala_altura = ALTO_PANTALLA / len(arr)

    for i, valor in enumerate(arr):
        altura = valor * escala_altura
        x = i * ancho_barra
        y = ALTO_PANTALLA - altura
        
        color_actual = color_base
        if idx_rojo1 is not None and (i == idx_rojo1 or i == idx_rojo2):
            color_actual = ROJO

        # Ajuste visual: si hay muchas barras, quitamos el espacio negro entre ellas
        if ancho_barra > 3:
            ancho_final = ancho_barra - 1
        else:
            ancho_final = ancho_barra # Sin espacio si son muy finas
            
        rect = pygame.Rect(x, y, max(1, ancho_final), altura)
        pygame.draw.rect(pantalla, color_actual, rect)

def dibujar_info(retraso, intentos):
    # Fondo negro semitransparente para que se lea el texto
    s = pygame.Surface((450, 60))
    s.set_alpha(180)
    s.fill(NEGRO)
    pantalla.blit(s, (0,0))

    texto_velocidad = fuente.render(f"Retraso: {retraso}ms (Flechas ARRIBA/ABAJO)", True, BLANCO)
    texto_intentos = fuente.render(f"Intercambios: {intentos}", True, BLANCO)
    pantalla.blit(texto_velocidad, (10, 10))
    pantalla.blit(texto_intentos, (10, 35))

# --- Bucle Principal ---

def main():
    array_actual = generar_array(N)
    ordenando = True
    intentos = 0
    retraso_ms = 10 # Empezamos un poco más rápido por defecto
    
    idx_swap1, idx_swap2 = None, None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    retraso_ms = max(0, retraso_ms - 5)
                if evento.key == pygame.K_DOWN:
                    retraso_ms += 5
                if evento.key == pygame.K_r:
                    # Al reiniciar, usamos el mismo N que eligió el usuario
                    array_actual = generar_array(N)
                    ordenando = True
                    intentos = 0
                    idx_swap1, idx_swap2 = None, None

        color_base_dibujo = BLANCO
        
        if ordenando:
            array_actual, terminado, idx1, idx2 = paso_intercambio_aleatorio(array_actual)
            idx_swap1, idx_swap2 = idx1, idx2
            
            if not terminado:
                intentos += 1
            else:
                ordenando = False
                print(f"¡Ordenado en {intentos} intercambios!")
        
        if not ordenando:
            color_base_dibujo = VERDE
            idx_swap1, idx_swap2 = None, None

        dibujar_barras(array_actual, color_base_dibujo, idx_swap1, idx_swap2)
        dibujar_info(retraso_ms, intentos)
        
        if not ordenando:
             texto_fin = fuente.render("¡ORDENADO! Presiona 'R' para reiniciar.", True, VERDE)
             pantalla.blit(texto_fin, (ANCHO_PANTALLA//2 - 150, ALTO_PANTALLA//2))

        pygame.display.flip()
        pygame.time.delay(retraso_ms)
        reloj.tick(60) 

if __name__ == "__main__":
    main()


#arr pirata