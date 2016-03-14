__author__ = 'rubico'

import Models
from Database.Connection import Connection
import Settings


class PageManager:

    __connection = Connection(Settings.sqllite_file_location)

    @staticmethod
    def get_by_id(id):
        result = PageManager.__connection.execute('SELECT id, url_id, html, is_parsed FROM Page WHERE id = ?', (id,))
        return Models.Page.Page(tuple=result[0]) if result else None

    @staticmethod
    def get_by_url_id(url_id):
        result = PageManager.__connection.execute(
            'SELECT id, url_id, html, is_parsed FROM Page WHERE url_id = ?', (url_id,)
        )
        return Models.Page.Page(tuple=result[0]) if result else None

    @staticmethod
    def save(page_object):
        if PageManager.get_by_url_id(page_object.url.id):
            PageManager.__connection.execute(
                'UPDATE Page SET url_id = ?, html = ?, is_parsed = ? WHERE url_id = ?',
                (page_object.url.id, page_object.html, page_object.is_parsed, page_object.url.id)
            )
        else:
            PageManager.__connection.execute(
                'INSERT INTO Page(url_id, html, is_parsed) VALUES (?, ?, ?)',
                (page_object.url.id,page_object.html, page_object.is_parsed)
            )
        return PageManager.get_by_url_id(page_object.url.id)


    @staticmethod
    def get_page_not_parsed():
        result = PageManager.__connection.execute('SELECT id, url_id, html, is_parsed FROM Page WHERE is_parsed = 0 LIMIT 1')
        return Models.Page.Page(tuple=result[0]) if result else None