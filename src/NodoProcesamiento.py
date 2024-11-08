### PROGRAMA DEL NODO DE PROCESAMIENTO PARA PROCESAMIENTO DE VIDEO
### Y CONEXIONES CON EL BROKER.

# El nodo de procesamiento realiza las siguientes acciones:
# 1. Conectarse al broker.
# 2. Recibir una parte del video a procesar.
# 3. Descomponer el video en frames.
# 4. Aplicar un filtro (monocromático) a cada frame.
# 5. Devolver el video procesado al broker.

# IMPORTACIÓN DE LIBRERÍAS
import socket   # Librería para la conexión entre el nodo de procesamiento y el broker.
import struct   # Librería para el manejo de datos binarios.  
import cv2     # Librería para el procesamiento de video.

class NodoProcesamiento:

  ## ATRIBUTOS ##

  def __init__(self):
    self.host = "localhost" # Dirección IP del broker
    self.port = 5000       # Puerto de conexión del broker  
  
  ## METODOS ##
  
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
    
  # Método para recibir un archivo (video)
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
        print("Archivo recibido correctamente")
        self.video = f.name
      return True
    except Exception as e:
      print(f"Error al recibir el archivo: {e}")
      self.video = None
      return False
  
  # Método para descomponer el video en frames
  def DescomponerVideo(self):
    if not self.video:
      print("No se ha recibido el video")
      return False
    
    frames = []
    try:
      cap = cv2.VideoCapture(self.video)
      while True:
        ret, frame = cap.read()
        if not ret:
          break
        frames.append(frame)
      cap.release()
      print(f"Video descompuesto en {len(frames)} frames")
      return frames
    except Exception as e:
      print(f"Error al descomponer el video: {e}")
      return False
    
    
if __name__ == "__main__":
  nodo = NodoProcesamiento()
  conn = nodo.Conectar()
  if conn:
    archivo_recibido = nodo.RecibirArchivo(conn)
    if archivo_recibido:
      frames = nodo.DescomponerVideo()
    