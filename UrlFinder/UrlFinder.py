

__author__ = 'rubico'

from threading import Thread
from sqlite3 import OperationalError
import time

from UrlExtractor import UrlExtractor
from Models.Page import Page
from Models.UrlDownload import UrlDownload
from UrlClassifier import UrlClassifier, UrlClasses
from Models.Url import Url


class UrlFinder(Thread):

    dispatcher = None
    download_dispatcher = None
    url_extractor = None
    page = None
    download_pattern = ''
    
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.dispatcher = kwargs.get('dispatcher', None)
        if self.dispatcher is None:
            raise Exception('UrlFinder needs a dispatcher to work properly')
        self.url_extractor = kwargs.get('url_extractor', None)
        if self.url_extractor is None:
            self.url_extractor = UrlExtractor()
        self.download_dispatcher = kwargs.get('download_dispatcher', None)
        if self.download_dispatcher is None:
            print 'Download dispatcher not defined.'
        self.download_patter = kwargs.get('download_pattern', None)
        if self.download_pattern is None:
            print 'Download pattern not defined'
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
        download_urls = []
        url_classifier = UrlClassifier(self.page, self.download_pattern)
        for url in urls[:]:
            _class = url_classifier.classify(url)
            if _class == UrlClasses.TRASH:
                urls.remove(url)
            elif _class == UrlClasses.DOWNLOAD:
                if self.download_dispatcher:
                    url_download = url.to_urldownload()
                    download_urls.append(url_download)
                    url_download.save()
                    urls.remove(url)
            elif _class == UrlClasses.FETCH and Url.manager.exists(url.url):
                urls.remove(url)
            else:
                url.save()

        self.page.is_parsed = True
        self.page.save()

        self.dispatcher.fill_pool(urls)
        if self.download_dispatcher:
            self.download_dispatcher.fill_pool(download_urls)