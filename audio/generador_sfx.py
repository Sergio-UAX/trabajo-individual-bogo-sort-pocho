import wave
import math
import struct
import os

def crear_sonido_pop():
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) #para detectar la ruta actual
    nombre_archivo = "pop.wav"
    ruta_completa = os.path.join(directorio_actual, nombre_archivo)
    print(f"[GENERADOR] Creando archivo en: {ruta_completa}...")
    sample_rate = 44100
    duration = 0.05
    frequency = 500
    n_samples = int(sample_rate * duration)
    
    try:
        with wave.open(ruta_completa, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(n_samples):
                t = i / sample_rate
                decay = 1.0 - (float(i) / n_samples)
                value = int(32767.0 * 0.5 * decay * math.sin(2.0 * math.pi * frequency * t))
                data = struct.pack('<h', value)
                wav_file.writeframes(data)
                
        print(f"[GENERADOR] ¡Éxito! 'pop.wav' listo.")
    except Exception as e:
        print(f"[GENERADOR] Error: {e}")
if __name__ == "__main__":
    crear_sonido_pop()

#arr.wav no flac ni mp3