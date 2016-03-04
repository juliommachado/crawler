__author__ = 'rubico'

from urlparse import urlparse
from Database import Connection
import Settings

class Url:
    
    connection = Connection(Settings.sqllite_file_location)
    ID_POSITION = 0
    URL_POSITION = 1

    id = None
    url = None
    
    def __init__(self, url, *args, **kwargs):
        if kwargs.has_key('tuple'):
            self.id = kwargs['tuple'][Url.ID_POSITION]
            self.url = kwargs['tuple'][Url.URL_POSITION]
        else:
            self.url = url

    def save(self):
        self.connection.execute('INSERT INTO Url (url) VALUES(?)', (self.url,))
        
    def get_host(self):
        parsed_uri = urlparse(self.url)
        return parsed_uri.netloc
        
    def is_relative(self):
        return self.get_host() == ''