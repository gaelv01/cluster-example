# PROGRAMA DEL CLIENTE PARA LA CONEXIÓN CON EL BROKER
# El cliente realiza únicamente tres acciones:
# 1. Conectarse al broker
# 2. Insertar un video de 15 segundos
# 3. Recibir el video procesado por el broker y los nodos de procesamiento.

# IMPORTACIÓN DE LIBRERÍAS
import socket   # Librería para la conexión entre el cliente y el broker.
import cv2      # Librería para el manejo de videos.


class Cliente:

  # Atributos
  def __init__(self):
    self.nombre = "Cliente" # Nombre del cliente
    self.host = "localhost" # Dirección IP hacia el broker
    self.port = 5000        # Puerto de conexión con el broker
    self.ruta_video = "/video/video.mp4" # Ruta del video a enviar

  ## MÉTODOS ##

  # Método para conectarse al broker

  def Conectar(self):
    try:
      # Creación y conexión del socket con el broker
      s = socket.create_connection((self.host, self.port))
      print("Conexión establecida con el broker")
      return s
    except socket.error as e:
      print(f"Error al conectar con el broker: {e}")
      return None
  

if __name__ == "__main__":
  cliente = Cliente()
  cliente.Conectar()