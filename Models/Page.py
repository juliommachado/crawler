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
    
    def __init__(self, url=None, html=None, *args, **kwargs):
        if kwargs.has_tuple('tuple'):
            self.id = kwargs['tuple'][Page.ID_POSITION]
            self.url = kwargs['tuple'][Page.URL_POSITION]
            self.html = kwargs['tuple'][Page.HTML_POSITION]
            self.parsed = kwargs['tuple'][Page.PARSED_POSITION]
        else:
            self.url = url
            self.html = html
            self.parsed = False

    def fetch_id(self):
        id = self.connection.execute('SELECT id FROM Page WHERE url_id LIKE ?', (self.url.id,))
        if id is None:
            return None
        return id[0][Page.ID_POSITION] #It's a list with just one position

    def save(self):
        self.connection.execute('INSERT INTO Page (url_id, html, parsed) VALUES (?, ?, ?)', (self.url.id, self.html, self.parsed))

    def mark_as_parsed(self):
        self.connection.execute('UPDATE Page SET is_parsed = ? WHERE url_id = ?', (True, self.url.id))
        self.parsed = True