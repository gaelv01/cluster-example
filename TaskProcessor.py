import multiprocessing

class TaskProcessor:
    def __init__(self, num_processes=4):
        """
        Inicializa el procesador de tareas con el número de procesos especificado.
        
        :param num_processes: Número de procesos en el pool de multiprocessing.
        """
        self.num_processes = num_processes
    
    def task(self, num):
        """
        Define la tarea a realizar. En este caso, calcula el cubo de un número.
        
        :param num: Número a procesar.
        :return: El cubo del número.
        """
        return num * num * num
    
    def process_tasks(self, num_range):
        """
        Procesa una lista de tareas en paralelo usando multiprocessing.
        
        :param num_range: Rango de números a procesar.
        :return: Lista de resultados de las tareas procesadas.
        """
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            async_result = pool.map_async(self.task, num_range)
            results = async_result.get()
        return results
