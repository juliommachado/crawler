__author__ = 'rubico'

from threading import Thread
from sqlite3 import OperationalError
import time

from Models.Page import Page
from Models.UrlDownload import UrlDownload
from UrlClassifier import UrlClassifier, UrlClasses
from Models.Url import Url


class UrlFinder(Thread):

    dispatcher = None
    download_dispatcher = None
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
        self.download_dispatcher = kwargs.get('download_dispatcher', None)
        if self.download_dispatcher is None:
            print 'Download dispatcher not defined.'
        self.start()
        
    def look_for_page(self):
        result = None
        try:
            result = self.__get_pending_page()
        except OperationalError:
            print '\n Database on lock \n'

        self.page = None
        if result is not None:
            self.page = Page(tuple=result[0])

    def run(self):
        self.__resume_crawling()
        while True:
            self.look_for_page()
            if self.page is not None:
                try:
                    self.url_extractor.feed(self.page)
                    urls = self.url_extractor.urls

                    #Classify all the urls
                    self.__classify_urls(urls)
                except OperationalError:
                    print '\n Database on lock \n'
            else:
                time.sleep(7)

    def __resume_crawling(self):
        urls = self.__get_pending_urls()
        if urls:
            self.dispatcher.fill_pool(urls)
        if self.download_dispatcher:
            download_urls = self.__get_pending_download_urls()
            if download_urls:
                self.download_dispatcher.fill_pool(download_urls)

    def __get_pending_urls(self):
        return Url.manager.get_pending_urls()

    def __get_pending_download_urls(self):
        return UrlDownload.manager.get_pending_download_urls()

    def __get_pending_page(self):
        return Page.manager.get_pending_page()

    def __classify_urls(self, urls):
        urls_download = []
        url_classifier = UrlClassifier(self.page)
        for url in urls[:]:
            _class = url_classifier.classify(url)
            if _class == UrlClasses.TRASH:
                urls.remove(url)
            elif _class == UrlClasses.DOWNLOAD:
                url_download = url.to_urldownload()
                urls_download.append(url_download)
                url_download.save()
                urls.remove(url)
            elif _class == UrlClasses.FETCH and Url.manager.exists(url.url):
                urls.remove(url)
            else:
                url.save()

        self.page.mark_as_parsed()
        self.dispatcher.fill_pool(urls)
        self.download_dispatcher.fill_pool(urls_download)