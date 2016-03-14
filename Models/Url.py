from Models.UrlDownload import UrlDownload

__author__ = 'rubico'

from Models import UrlManager
from urlparse import urlparse, urljoin
from Database.Connection import Connection
import Settings


class Url:
    
    manager = UrlManager

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

    def save(self):
        Url.manager.save(self)

    def get_host(self):
        parsed_uri = urlparse(self.url)
        return parsed_uri.netloc
        
    def is_relative(self):
        return self.get_host() == ''

    def __set_url__(self, url, url_master):
        self.url = url
        if self.is_relative():
            self.url = urljoin(url_master, self.url)

    def to_urldownload(self):
        url_download = UrlDownload()
        url_download.url = self.url
        url_download.is_downloaded = False
        return url_download
