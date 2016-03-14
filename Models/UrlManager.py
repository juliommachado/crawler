__author__ = 'rubico'

import Models
from Database.Connection import Connection
import Settings


class UrlManager:

    __connection = Connection(Settings.sqllite_file_location)

    @staticmethod
    def get_by_id(id):
        result = UrlManager.__connection.execute('SELECT id, url FROM Url WHERE id ?', (id,))
        return Models.Url.Url(tuple=result[0]) if result else None

    @staticmethod
    def get_by_url(url):
        result = UrlManager.__connection.execute('SELECT id, url FROM Url WHERE url LIKE ?', (url,))
        return Models.Url.Url(tuple=result[0]) if result else None

    @staticmethod
    def exists(url):
        result = UrlManager.__connection.execute('SELECT id FROM Url WHERE url like ?', (url,))
        return result is not None

    @staticmethod
    def save(url_object):
        database_url = UrlManager.get_by_url(url_object.url)
        if database_url is not None:
            UrlManager.__connection.execute(
                'UPDATE Url SET url = ? WHERE id = ?',
                (url_object.url, database_url.id)
            )
        else:
            UrlManager.__connection.execute(
                'INSERT INTO Url(url) VALUES (?)',
                (url_object.url,)
            )
        return UrlManager.get_by_url(url_object.url)

    @staticmethod
    def get_pending_urls():
        results = UrlManager.__connection.execute('SELECT id, url FROM Url WHERE id NOT in (SELECT url_id FROM Page)')
        urls = []
        for result in results:
            url = Models.Url.Url(tuple=result)
            urls.append(url)

        return urls if urls else None
