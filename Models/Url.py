__author__ = 'rubico'

from urlparse import urlparse, urljoin
from Database.Connection import Connection
import Settings

class Url:
    
    connection = Connection(Settings.sqllite_file_location)
    ID_POSITION = 0
    URL_POSITION = 1

    id = None
    url = None
    
    def __init__(self, url=None, url_master=None, *args, **kwargs):
        if kwargs.has_key('tuple'):
            self.id = kwargs['tuple'][Url.ID_POSITION]
            self.__set_url__(kwargs['tuple'][Url.URL_POSITION], url_master)
        else:
            self.__set_url__(url, url_master)

    def fetch_id(self):
        id = self.connection.execute('SELECT id FROM Url WHERE url LIKE ?', (self.url,))
        if id is None:
            return None
        return id[0][Url.ID_POSITION] #It's a list with just one position

    def save(self):
        id = self.fetch_id()
        if id is None and self.id is None:
            self.connection.execute('INSERT INTO Url (url) VALUES(?)', (self.url,))
            self.id = self.fetch_id()
            pass

    def get_host(self):
        parsed_uri = urlparse(self.url)
        return parsed_uri.netloc
        
    def is_relative(self):
        return self.get_host() == ''

    def __set_url__(self, url, url_master):
        self.url = url
        if self.is_relative():
            self.url = urljoin(url_master, self.url)
