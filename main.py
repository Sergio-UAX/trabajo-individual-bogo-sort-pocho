import pygame
import random
import sys
import os
import time
import subprocess 

try:
    from audio.player import ReproductorMusica
except ImportError:
    print("\n[ERROR CRÍTICO] No se encuentra 'audio/player.py'.")
    print("Asegúrate de que player.py esté dentro de la carpeta 'audio'.")
    sys.exit()

# configuracion antes de comenzar el bogogogo

def preguntar_generar_sfx():
    ruta_script = os.path.join("audio", "generador_sfx.py")
    
    if not os.path.exists(ruta_script):
        if os.path.exists("generador_sfx.py"):
            ruta_script = "generador_sfx.py"
        else:
            print(f"\n[AVISO] No se encontró el generador en '{ruta_script}'.")
            return

    print("\n--- CONFIGURACIÓN DE AUDIO ---")
    while True:
        resp = input("¿Quieres generar el efecto 'pop.wav'? (s/n): ").lower()
        if resp == 's':
            print("Ejecutando generador...")
            try:
                subprocess.run([sys.executable, ruta_script], check=True)
            except Exception as e:
                print(f"Error: {e}")
            break
        elif resp == 'n':
            break

def obtener_datos():
    print("\n--- CONFIGURACIÓN DE BOGO SORT ---")
    while True:
        try:
            n = int(input("Número de barras (ej: 10, 50): "))
            if n > 1: break
            print("Debe ser mayor a 1.")
        except ValueError:
            print("Número inválido.")
            
    print("\n--- MODO ---")
    print("1. VISUAL (Gráficos y Audio)")
    print("2. TERMINAL (Velocidad pura)")
    while True:
        m = input("Elige (1 o 2): ")
        if m == "1": return n, "visual"
        if m == "2": return n, "terminal"

# algoritmo bogo sort visual y terminal (los dos modos usan estas funciones)

def generar_array(n):
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return arr

def esta_ordenado(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]: return False
    return True

def paso_intercambio(arr):
    if esta_ordenado(arr): return arr, True, None, None
    n = len(arr)
    i, j = random.randint(0, n-1), random.randint(0, n-1)
    while i == j and n > 1: j = random.randint(0, n-1)
    arr[i], arr[j] = arr[j], arr[i]
    return arr, False, i, j
# los modos visual y terminal
def modo_visual(N):
    ANCHO, ALTO = 800, 600
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(f"Bogo Sort - {N} Elementos")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont('Arial', 20)
    
    # sfx
    reproduc = ReproductorMusica()
    
    # Rutas para el efecto y la música de fondo
    path_sfx = os.path.join(os.getcwd(), "audio", "pop.wav")
    path_music = os.path.join(os.getcwd(), "audio", "cancion.mp3")
    
    reproduc.cargar_efecto(path_sfx)
    reproduc.reproducir_musica(path_music)
    
    volumen_display = 30

    def dibujar(arr, color, i1, i2):
        pantalla.fill((0,0,0))
        w = ANCHO / len(arr)
        h_esc = ALTO / len(arr)
        w_f = max(1, w - 1) if w > 3 else w
        for i, val in enumerate(arr):
            color_b = (255,0,0) if (i1 is not None and (i==i1 or i==i2)) else color
            pygame.draw.rect(pantalla, color_b, (i*w, ALTO - val*h_esc, w_f, val*h_esc))

    def info(ms, intentos, vol):
        s = pygame.Surface((450, 90)); s.set_alpha(180); s.fill((0,0,0))
        pantalla.blit(s, (0,0))
        pantalla.blit(fuente.render(f"Velocidad: {ms}ms (UP/DOWN)", 1, (255,255,255)), (10,10))
        pantalla.blit(fuente.render(f"Intentos: {intentos}", 1, (255,255,255)), (10,35))
        pantalla.blit(fuente.render(f"Volumen: {vol}% (+/-)", 1, (255,255,255)), (10,60))

    arr = generar_array(N)
    ordenando, intentos, retraso = True, 0, 10
    idx1, idx2 = None, None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                reproduc.detener_todo(); pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: retraso = max(0, retraso - 5)
                if e.key == pygame.K_DOWN: retraso += 5
                if e.key in [pygame.K_PLUS, pygame.K_KP_PLUS]: volumen_display = reproduc.modificar_volumen(0.1)
                if e.key in [pygame.K_MINUS, pygame.K_KP_MINUS]: volumen_display = reproduc.modificar_volumen(-0.1)
                if e.key == pygame.K_r: 
                    arr = generar_array(N); ordenando = True; intentos = 0

        if ordenando:
            arr, fin, i1, i2 = paso_intercambio(arr)
            idx1, idx2 = i1, i2
            if not fin:
                intentos += 1
                reproduc.reproducir_efecto()
            else:
                ordenando = False
                print(f"¡Ordenado en {intentos}!")
        
        dibujar(arr, (255,255,255) if ordenando else (0,255,0), idx1, idx2)
        info(retraso, intentos, volumen_display)
        pygame.display.flip()
        pygame.time.delay(retraso)
        reloj.tick(60)

def modo_terminal(N):
    print(f"\n[TERMINAL] Ordenando {N} elementos...")
    arr = generar_array(N)
    intentos, inicio = 0, time.time()
    try:
        while not esta_ordenado(arr):
            n = len(arr)
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            arr[i], arr[j] = arr[j], arr[i]
            intentos += 1
            if intentos % 100000 == 0: print(f"Intentos: {intentos}...")
    except KeyboardInterrupt:
        sys.exit()
    print(f"¡Listo! {intentos} intentos en {time.time()-inicio:.2f}s")
    input("Enter para salir...")

if __name__ == "__main__":
    preguntar_generar_sfx()
    n, modo = obtener_datos()
    modo_visual(n) if modo == "visual" else modo_terminal(n)

#arr pirateta-tento a navegantes

""" Este es el link de github: https://github.com/Sergio-UAX/trabajo-individual-bogo-sort-pocho """