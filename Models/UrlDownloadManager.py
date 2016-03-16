__author__ = 'rubico'

from Database.Connection import Connection
import Models
import Settings


class UrlDownloadManager:

    __connection = Connection(Settings.sqllite_file_location)

    @staticmethod
    def get_by_id(id):
        result = UrlDownloadManager.__connection.execute('SELECT id, url, is_downloaded FROM UrlDownload WHERE id = ?', (id,))
        return Models.UrlDownload.UrlDownload(tuple=result[0]) if result else None

    @staticmethod
    def get_by_url(url):
        result = UrlDownloadManager.__connection.execute('SELECT id, url, is_downloaded FROM UrlDownload WHERE url LIKE ?', (url,))
        return Models.UrlDownload.UrlDownload(tuple=result[0]) if result else None

    @staticmethod
    def exists(url):
        result = UrlDownloadManager.__connection.execute('SELECT id FROM UrlDownload WHERE url like ?', (url,))
        return result is not None

    @staticmethod
    def save(url_download_object):
        database_url = UrlDownloadManager.get_by_url(url_download_object.url)
        if database_url is not None:
            UrlDownloadManager.__connection.execute(
                'UPDATE UrlDownload SET url = ?, is_downloaded = ? WHERE id = ?',
                (url_download_object.url, url_download_object.is_downloaded, database_url.id)
            )
        else:
            UrlDownloadManager.__connection.execute(
                'INSERT INTO UrlDownload(url, is_downloaded) VALUES (?, ?)',
                (url_download_object.url, False)
            )
        return UrlDownloadManager.get_by_url(url_download_object.url)

    @staticmethod
    def get_pending_download_urls():
        results = UrlDownloadManager.__connection.execute(
            'SELECT id, url, is_downloaded FROM UrlDownload WHERE is_downloaded = 0'
        )
        download_urls = []
        if results:
            for result in results:
                download_url = Models.UrlDownload.UrlDownload(tuple=result)
                download_urls.append(download_url)

        return download_urls if download_urls else None