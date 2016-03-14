__author__ = 'rubico'

from Database.Connection import Connection
import Settings


class PageManager:

    __connection = Connection(Settings.sqllite_file_location)

    @staticmethod
    def get_by_id(id):
        return PageManager.__connection.execute('SELECT id, html,is_parsed FROM Page WHERE id ?', (id,))

    @staticmethod
    def save(page_object):
        PageManager.__connection.execute(
            'INSERT INTO Page(url_id, html, is_parsed) VALUES (?, ?, ?)',
            (page_object.url.id,page_object.html, page_object.is_parsed)
        )

    @staticmethod
    def get_page_not_parsed():
        return PageManager.__connection.execute('SELECT id, url_id, html, is_parsed FROM Page WHERE is_parsed = 0 LIMIT 1')

    @staticmethod
    def set_as_parsed(page_object):
        PageManager.__connection.execute(
            'UPDATE Page SET is_parsed = ? WHERE url_id = ?',
            (1, page_object.url.id)
        )