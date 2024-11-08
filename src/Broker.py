## PROGRAMA DEL BROKER PARA INTERCONECTAR LOS NODOS DE PROCESAMIENTO
## Y EL CLIENTE

# El broker realiza las siguientes acciones:
# 1. Permitir la conexión de los diversos nodos de procesamiento.
# 2. Permitir la conexión del cliente.
# 2. Recibir el video del cliente.
# 3. Dividir el video con el numero de nodos de procesamiento.
# 3. Distribuir el video a los nodos de procesamiento.
# 4. Recibir el video procesado por los nodos de procesamiento.
# 5. Enviar el video procesado al cliente.

# IMPORTACIÓN DE LIBRERÍAS
import socket   # Librería para la conexión entre el broker y los nodos de procesamiento.
import struct   # Librería para el manejo de datos binarios.
import cv2      # Librería para el procesamiento de video.

class Broker:

  # Atributos
  def __init__(self):
    self.host = "localhost" # Dirección IP del broker
    self.port = 5000        # Puerto de conexión del broker
    self.video = None       # Atributo para almacenar el video recibido
    self.nodos_conectados = 0 # Contador de nodos conectados
    self.direcciones_nodos = {} # Diccionario para almacenar las direcciones de los nodos conectados
    self.partes_video = [] # Lista para almacenar las partes del video

  # Método genérico para permitir la conexión
  def PermitirConexion(self, tipo):
    try:
      # Creación y configuración del servidor usando create_server
      with socket.create_server((self.host, self.port)) as s:
        print(f"Esperando conexión del {tipo}...")
        conn, addr = s.accept()  # Aceptar la conexión
        print(f"Conexión establecida con el {tipo}: {addr}")
        if tipo == "nodo de procesamiento":
          self.nodos_conectados += 1  # Incrementar el contador de nodos conectados
          self.direcciones_nodos[self.nodos_conectados] = conn
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

  # Método para enviar un archivo (video)
  def EnviarArchivo(self, conn, archivo):
    try:
      with open(archivo, "rb") as f:
        data = f.read()
        # Empaquetar el tamaño del archivo y los datos
        file_size = struct.pack("!I", len(data))
        conn.sendall(file_size + data)
        print("Archivo enviado correctamente")
    except FileNotFoundError:
      print("Archivo no encontrado")
    except Exception as e:
      print(f"Error al enviar el archivo: {e}")

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
        data += packet # Almacenar el video recibido en el atributo
      with open("video_recibido.mp4", "wb") as f:
        f.write(data)
        print("Archivo recibido correctamente")
        self.video = f.name
      return True
    except Exception as e:
      print(f"Error al recibir el archivo: {e}")
      self.video = None
      return False

  # Método para dividir un video en partes iguales en base al número de nodos
  def DividirVideo(self):
    if not self.video:
      print("No hay video recibido para dividir.")
      return None
    
    try:
      # Leer el video con cv2
      cap = cv2.VideoCapture(self.video);
      total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      fps = cap.get(cv2.CAP_PROP_FPS)
      frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
      frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
      part_size = total_frames // self.nodos_conectados
      
      for i in range(self.nodos_conectados):
        start_frame = i * part_size
        end_frame = start_frame + part_size
        if i == self.nodos_conectados - 1:
          end_frame = total_frames
          
        part_filename = f"parte_{i+1}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(part_filename, fourcc, fps, (frame_width, frame_height))
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        for j in range(start_frame, end_frame):
          ret, frame = cap.read()
          if not ret:
            break
          out.write(frame)
      
        out.release()
        print(f"Parte {i+1} del video dividida correctamente y guardada en {part_filename}")
        self.partes_video.append(part_filename)

    except Exception as e:
      print(f"Error al dividir el video: {e}")
      return None

if __name__ == "__main__":
  broker = Broker() # Instanciamos el broker
  conn = broker.PermitirConexionCliente() # Permitimos la conexión del cliente
  if conn: # Si la conexión fue exitosa
    archivo_recibido = broker.RecibirArchivo(conn) # Recibimos el archivo del cliente (video)
    if archivo_recibido: # Si el archivo fue recibido correctamente
      while broker.nodos_conectados < 3:
        conn_nodo = broker.PermitirConexionNodo() # Permitimos la conexión de un nodo de procesamiento
      while True: # Bucle para permitir la conexión de más nodos de procesamiento
        agregar_mas = input("¿Desea agregar más nodos de procesamiento? (s/n): ")
        if agregar_mas.lower() == 's':
          conn_nodo = broker.PermitirConexionNodo() # Permitimos la conexión de un nodo de procesamiento
        else:
          break
      broker.DividirVideo()
      for i in range(broker.nodos_conectados):
        conn_nodo = broker.direcciones_nodos[i+1]
        broker.EnviarArchivo(conn_nodo, broker.partes_video[i])
        