from Models.Url import Url
import Settings
import sqlite3
from Database.Connection import Connection

__author__= 'rubico'


class Dispatcher:
    connection = None
    pool = None
    
    def __init__(self, *args, **kwargs):
        self.pool = []

        connection = Connection(Settings.sqllite_file_location)
        results = None
        try:
            results = connection.execute('SELECT id, url FROM Url WHERE id NOT in (SELECT url_id FROM Page)')
        except sqlite3.OperationalError:
            print 'Dispatcher didn\'t load any url, Database on lock'

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