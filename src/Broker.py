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

class Broker:

  # Atributos
  def __init__(self):
    self.host = "localhost" # Dirección IP del broker
    self.port = 5000        # Puerto de conexión del broker

  ## MÉTODOS ##

  # Método para permitir la conexión del cliente
  def PermitirConexionCliente(self):
    try:
      # Creación y configuración del servidor usando create_server
      with socket.create_server((self.host, self.port)) as s:
        print("Esperando conexión del cliente...")
        conn, addr = s.accept()  # Aceptar la conexión
        print(f"Conexión establecida con el cliente: {addr}")
        return conn
    except socket.error as e:
        print(f"Error en la conexión del cliente: {e}")
        return None

if __name__ == "__main__":
  broker = Broker()
  broker.PermitirConexionCliente()