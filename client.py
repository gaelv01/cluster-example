import socket

class Client:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.client_sock.connect((self.host, self.port))
        print('Conectado al servidor...')

    def send_data(self, data):
        self.client_sock.send(data.encode())

    def receive_data(self):
        response = self.client_sock.recv(1024)
        print('Resultados:', response.decode())
    
    def close(self):
        self.client_sock.close()


def main():
    client = Client()
    client.connect()
    client.send_data('10')
    client.receive_data()
    client.close()

if __name__ == '__main__':
    main()