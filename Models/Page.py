__author__ = 'rubico'

from Database import Connection
import Settings


class Page:
    
    connection = Connection(Settings.sqllite_file_location)
    ID_POSITION = 0
    URL_POSITION = 1
    HTML_POSITION = 2
    PARSED_POSITION = 3
    
    
    id = None
    html = None
    url = None
    parsed = False
    
    def __init__(self, url, html, *args, **kwargs):
        if kwargs.has_tuple('tuple'):
            self.id = kwargs['tuple'][Page.ID_POSITION]
            self.url = kwargs['tuple'][Page.URL_POSITION]
            self.html = kwargs['tuple'][Page.HTML_POSITION]
            self.parsed = kwargs['tuple'][Page.PARSED_POSITION]
        else:
            self.url = url
            self.html = html
            self.parsed = False
            
    def save(self):
        self.connection.execute('INSERT INTO Page (url_id, html, parsed) VALUES (?, ?, ?)', (self.url.id, self.html, self.parsed))
        