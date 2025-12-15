import pygame
import os

class ReproductorMusica:
    def __init__(self):
        # Inicializamos el módulo de sonido de pygame
        # (Ver justificacion.txt para detalles sobre el uso de esta librería)
        try:
            pygame.mixer.init()
            self.disponible = True
        except Exception as e:
            print(f"Error al inicializar audio: {e}")
            self.disponible = False

    def reproducir_musica(self, ruta_archivo):
        """Carga y reproduce el archivo en bucle infinito."""
        if self.disponible and os.path.exists(ruta_archivo):
            try:
                pygame.mixer.music.load(ruta_archivo)
                # loops=-1 indica que se repite infinitamente
                pygame.mixer.music.play(loops=-1) 
            except Exception as e:
                print(f"No se pudo reproducir la música: {e}")
        elif not os.path.exists(ruta_archivo):
            print(f"Advertencia: No se encontró el archivo de música en {ruta_archivo}")

    def detener_musica(self):
        """Detiene la música con un efecto de desvanecimiento (fadeout)."""
        if self.disponible:
            try:
                pygame.mixer.music.fadeout(1000)
            except Exception:
                pass # Ignorar errores al cerrar si no estaba sonando

#arr pirata