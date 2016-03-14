from Models.Url import Url
import Settings
import sqlite3
from Database.Connection import Connection

__author__= 'rubico'


class Dispatcher:
    pool = None
    
    def __init__(self, *args, **kwargs):
        self.pool = []
        self.connection = kwargs.get('connection', None)
        if self.connection is None:
            raise Exception('Dispatcher needs a connection to work properly')
        results = None
        try:
            results = self.__get_pending_pool()
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

    def __get_pending_pool(self):
        return Url.manager.get_pending_urls()