import pygame
import os

class ReproductorMusica:
    def __init__(self):
        # Inicializamos el mixer de pygame
        try:
            pygame.mixer.init()
            self.disponible = True
            self.efecto_sonido = None
            self.volumen = 0.3 # Volumen inicial (30%)
        except Exception as e:
            print(f"Error al inicializar audio: {e}")
            self.disponible = False

    def cargar_efecto(self, ruta_archivo): #para cargar el efecto corto (pop.wav) en la memoria
        if self.disponible and os.path.exists(ruta_archivo):
            try:
                self.efecto_sonido = pygame.mixer.Sound(ruta_archivo)
                self.efecto_sonido.set_volume(self.volumen)
            except Exception as e:
                print(f"Error cargando efecto: {e}")# No lanzamos error si no existe, solo un aviso timidillo en la consola
        elif not os.path.exists(ruta_archivo):
             print(f"Aviso: No se encontró el sonido en {ruta_archivo}")

    def reproducir_efecto(self):
        if self.disponible and self.efecto_sonido:
            self.efecto_sonido.play()

    def reproducir_musica(self, ruta_archivo): #para reproducir musica de fondo
        if self.disponible and os.path.exists(ruta_archivo):
            try:
                pygame.mixer.music.load(ruta_archivo)
                pygame.mixer.music.set_volume(self.volumen)
                pygame.mixer.music.play(loops=-1) # bucle infinito
            except Exception as e:
                print(f"Error música: {e}")

    def modificar_volumen(self, cambio): #para subir o bajar el volumen
        if self.disponible:
            nuevo_volumen = self.volumen + cambio
            self.volumen = max(0.0, min(1.0, nuevo_volumen))
            # iniciar efectos
            if self.efecto_sonido:
                self.efecto_sonido.set_volume(self.volumen)
            # iniciar musica
            try:
                pygame.mixer.music.set_volume(self.volumen)
            except:
                pass
        return int(self.volumen * 100)
    
    def detener_todo(self): #para detener todo el audio
        if self.disponible:
            try:
                pygame.mixer.music.fadeout(500)
                pygame.mixer.stop()
            except:
                pass

#arr pirata