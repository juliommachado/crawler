__author__= 'rubico'

class Dispatcher:
    pool = None
    
    def __init__(self, *args, **kwargs):
        self.pool = []
        
    def has_work(self):
        return len(self.pool) is not 0
        
    def get_work(self):
        return self.pool.pop(0)
        
    def fill_pool(self, workload):
        self.pool = self.pool + workload