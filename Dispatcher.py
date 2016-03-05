from Models.Url import Url
import Settings
from Database.Connection import Connection

__author__= 'rubico'


class Dispatcher:
    connection = None
    pool = None
    
    def __init__(self, *args, **kwargs):
        self.pool = []

        connection = Connection(Settings.sqllite_file_location)
        results = connection.execute('SELECT id, url FROM Url WHERE id NOT in (SELECT url_id FROM Page)')
        if results is not None:
            for result in results:
                url = Url(tuple=result)
                self.pool.append(url)
        
    def has_work(self):
        return len(self.pool) is not 0
        
    def get_work(self):
        return self.pool.pop(0)
        
    def fill_pool(self, workload):
        self.pool = self.pool + workload