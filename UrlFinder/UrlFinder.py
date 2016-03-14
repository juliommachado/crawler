__author__ = 'rubico'

from threading import Thread
from Models.Page import Page
from UrlClassifier import UrlClassifier, UrlClasses
from sqlite3 import OperationalError
from Models.Url import Url
import Dispatcher
from UrlExtractor import UrlExtractor
from Database.Connection import Connection
import Settings


class UrlFinder(Thread):

    dispatcher = None
    connection = None
    url_extractor = None
    page = None
    download_pattern = ''
    
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.connection = kwargs.get('connection', None)
        if self.connection is None:
            raise Exception('UrlFinder needs a connection to work properly.')
        self.dispatcher = kwargs.get('dispatcher', None)
        if self.dispatcher is None:
            raise Exception('UrlFinder needs a dispatcher to work properly')
        self.url_extractor = kwargs.get('url_extractor', None)
        if self.url_extractor is None:
            raise Exception('UrlFinder needs an extractor to work properly')
        self.start()
        
    def look_for_page(self):
        result = None
        try:
            result = self.__get_pending_urls()
        except OperationalError:
            print '\n Database on lock \n'

        self.page = None
        if result is not None:
            self.page = Page(tuple=result[0])

    def run(self):
        while True:
            self.look_for_page()
            if self.page is not None:
                try:
                    self.url_extractor.feed(self.page)
                    urls = self.url_extractor.urls

                    #Classify all the urls
                    url_classifier = UrlClassifier(self.page)
                    for url in urls[:]:
                        if url_classifier.classify(url) == UrlClasses.TRASH:
                            urls.remove(url)
                        elif url_classifier.classify(url) == UrlClasses.FETCH and Url.manager.exists(url.url):
                            urls.remove(url)
                        else:
                            url.save()

                    self.page.mark_as_parsed()
                    self.dispatcher.fill_pool(urls)
                except OperationalError:
                    print '\n Database on lock \n'

    def __get_pending_urls(self):
        return Url.manager.get_pending_urls()