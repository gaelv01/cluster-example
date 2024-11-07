## PROGRAMA DEL BROKER PARA INTERCONECTAR LOS NODOS DE PROCESAMIENTO
## Y EL CLIENTE

# El broker realiza las siguientes acciones:
# 1. Permitir la conexión de los diversos nodos de procesamiento.
# 2. Permitir la conexión del cliente.
# 2. Recibir el video del cliente.
# 3. Distribuir el video a los nodos de procesamiento.
# 4. Recibir el video procesado por los nodos de procesamiento.
# 5. Enviar el video procesado al cliente.

# IMPORTACIÓN DE LIBRERÍAS
import socket   # Librería para la conexión entre el broker y los nodos de procesamiento.
import struct   # Librería para el manejo de datos binarios.

class Broker:

  # Atributos
  def __init__(self):
    self.host = "localhost" # Dirección IP del broker
    self.port = 5000        # Puerto de conexión del broker
    self.video = None       # Atributo para almacenar el video recibido

  # Método genérico para permitir la conexión
  def PermitirConexion(self, tipo):
    try:
      # Creación y configuración del servidor usando create_server
      with socket.create_server((self.host, self.port)) as s:
        print(f"Esperando conexión del {tipo}...")
        conn, addr = s.accept()  # Aceptar la conexión
        print(f"Conexión establecida con el {tipo}: {addr}")
        return conn
    except socket.error as e:
      print(f"Error en la conexión del {tipo}: {e}")
      return None

  # Método para permitir la conexión del cliente
  def PermitirConexionCliente(self):
    return self.PermitirConexion("cliente")

  # Método para permitir la conexión del nodo de procesamiento
  def PermitirConexionNodo(self):
    return self.PermitirConexion("nodo de procesamiento")

  # Método para recibir un archivo
  def RecibirArchivo(self, conn):
    try:
      # Recibir el tamaño del archivo
      file_size = conn.recv(4)
      file_size = struct.unpack("!I", file_size)[0]
      data = b''
      while len(data) < file_size:
        packet = conn.recv(4096)
        if not packet:
          break
        data += packet
      self.video = data  # Almacenar el video recibido en el atributo
      with open("video_recibido.mp4", "wb") as f:
        f.write(data)
        print("Archivo recibido correctamente")
    except Exception as e:
      print(f"Error al recibir el archivo: {e}")
      self.video = None

if __name__ == "__main__":
  broker = Broker()
  conn = broker.PermitirConexionCliente()
  if conn:
    broker.RecibirArchivo(conn)
    broker.PermitirConexionNodo()