# PROGRAMA DEL CLIENTE PARA LA CONEXIÓN CON EL BROKER
# El cliente realiza únicamente tres acciones:
# 1. Conectarse al broker
# 2. Enviar un archivo (video) al broker
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
    
  # Método para enviar un archivo (video)
  def EnviarArchivo(self, conn, nombre_destino):
    try:
      with open(self.archivo, "rb") as f:
        data = f.read()
        # Empaquetar el tamaño del archivo, los datos y el nombre del archivo
        file_size = struct.pack("!I", len(data))
        file_name = nombre_destino.encode()
        file_name_size = struct.pack("!I", len(file_name))
        conn.sendall(file_name_size + file_name + file_size + data)
        print("Archivo enviado correctamente")
    except FileNotFoundError:
      print("Archivo no encontrado")
    except Exception as e:
      print(f"Error al enviar el archivo: {e}")

  # Método para recibir un archivo
  def RecibirArchivo(self, conn):
    try:
      # Recibir el tamaño del nombre del archivo
      file_name_size = conn.recv(4)
      file_name_size = struct.unpack("!I", file_name_size)[0]
      # Recibir el nombre del archivo
      file_name = conn.recv(file_name_size).decode()
      # Recibir el tamaño del archivo
      file_size = conn.recv(4)
      file_size = struct.unpack("!I", file_size)[0]
      data = b''
      while len(data) < file_size:
        packet = conn.recv(4096)
        if not packet:
          break
        data += packet # Almacenar el video recibido en el atributo
      with open(file_name, "wb") as f:
        f.write(data)
        print("Archivo recibido correctamente y guardado como", file_name)
        self.video = f.name
      return True
    except Exception as e:
      print(f"Error al recibir el archivo: {e}")
      self.video = None
      return False
    

if __name__ == "__main__":
  cliente = Cliente()
  conn = cliente.Conectar()
  if conn:
    cliente.EnviarArchivo(conn, "video_recibido.mp4")
    cliente.RecibirArchivo(conn)
    
