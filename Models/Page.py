__author__ = 'rubico'

from Models.PageManager import PageManager
from Models.Url import Url


class Page:

    manager = PageManager

    ID_POSITION = 0
    URL_POSITION = 1
    HTML_POSITION = 2
    PARSED_POSITION = 3

    id = None
    html = None
    url = None
    is_parsed = False
    
    def __init__(self, url=None, html=None, *args, **kwargs):
        if kwargs.has_key('tuple'):
            self.id = kwargs['tuple'][Page.ID_POSITION]

            self.url = Url.manager.get_by_id(kwargs['tuple'][Page.URL_POSITION])

            self.html = kwargs['tuple'][Page.HTML_POSITION]
            self.is_parsed = kwargs['tuple'][Page.PARSED_POSITION]
        else:
            self.url = url
            self.html = html
            self.is_parsed = False

    def save(self):
        return Page.manager.save(self)