import multiprocessing
import socket

# Tarea específica
def tarea(num):
    return num * num

def handle_client(client_socket):
    # Recibir datos del cliente
    data = client_socket.recv(1024)
    if not data:
        return
    # Convertir los datos recibidos a un rango de números
    num_range = range(int(data.decode()))

    # Crear un grupo de procesos con 4 procesos
    with multiprocessing.Pool(processes=4) as pool:
        # Ejecutar la tarea en paralelo de manera asíncrona
        async_result = pool.map_async(tarea, num_range)
        print('Esperando a que se completen las tareas...')
        # Obtener los resultados
        resultados = async_result.get()
    
    # Enviar los resultados al cliente
    client_socket.send(str(resultados).encode())
    # Cerrar la conexión con el cliente
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1',9999))
    print('Servidor escuchando en el puerto 9999...')
    while True:
        server.listen(5)
        client, addr = server.accept()
        print(f'Conexión aceptada desde {addr}')
        handle_client(client)

if __name__ == '__main__':
    main()
