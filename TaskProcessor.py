import multiprocessing

class TaskProcessor:
    def __init__(self, num_processes=4):
        self.num_processes = num_processes
    
    def task(self, num):
        return num * num * num
    
    def process_tasks(self, num_range):
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            async_result = pool.map_async(self.task, num_range)
            results = async_result.get()
        return results
    
    
