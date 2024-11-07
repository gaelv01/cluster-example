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
    
    
if __name__ == "__main__":
  nodo = NodoProcesamiento()
  conn = nodo.Conectar()