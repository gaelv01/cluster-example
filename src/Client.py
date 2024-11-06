# PROGRAMA DEL CLIENTE PARA LA CONEXIÓN CON EL BROKER
# El cliente realiza únicamente tres acciones:
# 1. Conectarse al broker
# 2. Insertar un video de 15 segundos
# 3. Recibir el video procesado por el broker y los nodos de procesamiento.

# IMPORTACIÓN DE LIBRERÍAS
import socket   # Librería para la conexión entre el cliente y el broker.
import struct   # Librería para el manejo de datos binarios.


class Cliente:

  # Atributos
  def __init__(self):
    self.nombre = "Cliente" # Nombre del cliente
    self.host = "localhost" # Dirección IP hacia el broker
    self.port = 5000        # Puerto de conexión con el broker
    self.archivo = "video.mp4" # Archivo a enviar al broker

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
    
  # Método para enviar un archivo
  def EnviarArchivo(self, conn):
    try:
      with open(self.archivo, "rb") as f:
        data = f.read()
        # Empaquetar el tamaño del archivo y los datos
        file_size = struct.pack("!I", len(data))
        conn.sendall(file_size + data)
        print("Archivo enviado correctamente")
    except FileNotFoundError:
      print("Archivo no encontrado")
    except Exception as e:
      print(f"Error al enviar el archivo: {e}")
    

if __name__ == "__main__":
  cliente = Cliente()
  s = cliente.Conectar()
  if s:
    cliente.EnviarArchivo(s)
