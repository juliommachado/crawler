from Database.Connection import Connection
import Settings

__author__ = 'rubico'


class UrlDownloadManager:

    __connection = Connection(Settings.sqllite_file_location)

    @staticmethod
    def get_by_id(id):
        return UrlDownloadManager.__connection.execute('SELECT id, url, is_downloaded FROM UrlDownload WHERE id ?', (id,))

    @staticmethod
    def get_by_url(url):
        return UrlDownloadManager.__connection.execute('SELECT id, url, is_downloaded FROM UrlDownload WHERE url LIKE ?', (url,))

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