import multiprocessing

# Tarea específica
def tarea(num):
    return num * num

if __name__ == '__main__':
    # Crear un grupo de procesos con 4 procesos
    with multiprocessing.Pool(processes=4) as pool:
        # Ejecutar la tarea en paralelo de manera asíncrona
        async_result = pool.map_async(tarea, range(10))
        print('Esperando a que se completen las tareas...')
        # Obtener los resultados
        resultados = async_result.get()
    # Imprimir los resultados
    print(resultados)
