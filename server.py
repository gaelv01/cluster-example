import socket
import threading
from TaskProcessor import TaskProcessor

class Server:
    def __init__(self, host='127.0.0.1', port=9999):
        """
        Inicializa el servidor con la dirección y el puerto especificados.
        
        :param host: Dirección IP en la que el servidor escuchará.
        :param port: Puerto en el que el servidor escuchará.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.task_processor = TaskProcessor()

    def handle_client(self, client_socket):
        """
        Maneja la conexión con un cliente.
        
        :param client_socket: Socket de la conexión con el cliente.
        """
        try:
            data = client_socket.recv(1024)
            if not data:
                return

            num_range = range(int(data.decode()))
            resultados = self.task_processor.process_tasks(num_range)
            client_socket.send(str(resultados).encode())
        finally:
            client_socket.close()

    def start(self):
        """
        Inicia el servidor para escuchar conexiones entrantes.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'Servidor escuchando en el puerto {self.port}...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f'Conexión aceptada desde {addr}')
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

def main():
    """
    Función principal para iniciar el servidor.
    """
    server = Server()
    server.start()

if __name__ == '__main__':
    main()
