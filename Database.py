__author__ = 'rubico'
 
import sqlite3
 
 
class Connection:
    
    file_name = ''
    
    def __init__(self, file, *args, **kwargs):
        self.file_name = file
        
    def execute(self, command, *args):
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()
        data = cursor.execute(command, *args)
        conn.commit()
        conn.close()
        return data