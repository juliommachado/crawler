__author__ = 'rubico'
 
import sqlite3
 
 
class Connection:
    
    file_name = ''
    
    def __init__(self, file, *args, **kwargs):
        self.file_name = file
        
    def execute(self, command, *args):
        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()
        cursor = cursor.execute(command, *args)
        data = []
        for row in cursor:
            data.append(row)
        conn.commit()
        conn.close()

        if not data:
            return None
        return data