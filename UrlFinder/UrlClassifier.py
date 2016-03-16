__author__ = 'rubico'

from urlparse import urlparse
from enum import Enum
import re


class UrlClasses(Enum):
    TRASH = 0
    FETCH = 1
    DOWNLOAD = 2


class UrlClassifier:

    page = None
    page_domain = ''
    download_pattern = ''

    def __init__(self, page, download_pattern):
        self.page = page
        parsed_uri = urlparse(self.page.url.url)
        self.page_domain = parsed_uri.netloc
        self.download_pattern = download_pattern

    def classify(self, url):
        uri = url.url
        parsed_uri = urlparse(uri)
        if re.search(self.download_pattern, uri):
            return UrlClasses.DOWNLOAD
        elif self.page_domain == parsed_uri.netloc:
            return UrlClasses.FETCH
        else:
            return UrlClasses.TRASH