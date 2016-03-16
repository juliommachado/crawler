__author__ = 'rubico'

from urlparse import urlparse, urljoin

from Models.UrlDownloadManager import UrlDownloadManager


class UrlDownload:

    manager = UrlDownloadManager

    ID_POSITION = 0
    URL_POSITION = 1
    IS_DOWNLOADED_POSITION = 2

    def __init__(self, url=None, is_downloaded=None, url_master=None, *args, **kwargs):
        if kwargs.has_key('tuple'):
            self.id = kwargs['tuple'][UrlDownload.ID_POSITION]
            self.__set_url(kwargs['tuple'][UrlDownload.URL_POSITION], url_master)
            self.is_downloaded = kwargs['tuple'][UrlDownload.IS_DOWNLOADED_POSITION]
        else:
            self.url = url
            self.is_downloaded = is_downloaded

    def save(self):
        return self.manager.save(self)

    def get_host(self):
        parsed_uri = urlparse(self.url)
        return parsed_uri.netloc

    def is_relative(self):
        return self.get_host() == ''

    def __set_url(self, url, url_master):
        self.url = url
        if self.is_relative():
            self.url = urljoin(url_master, self.url)


