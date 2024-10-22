import socket
import threading
import multiprocessing

class Server:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tarea(self, num):
        return num * num

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            if not data:
                return

            num_range = range(int(data.decode()))

            with multiprocessing.Pool(processes=4) as pool:
                async_result = pool.map_async(self.tarea, num_range)
                resultados = async_result.get()

            client_socket.send(str(resultados).encode())
        finally:
            client_socket.close()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'Servidor escuchando en el puerto {self.port}...')

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f'Conexión aceptada desde {addr}')
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()



