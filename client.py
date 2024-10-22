import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1',9999))
    print('Conectado al servidor...')

    # Enviar datos al servidor
    client.send('10'.encode())

    # Recibir los resultados del servidor
    response = client.recv(1024)
    print('Resultados:', response.decode())

    # Cerrar la conexión con el servidor
    client.close()

if __name__ == '__main__':
    main()