

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
        self.dispatcher = kwargs.get('dispatcher', None)
        if self.dispatcher is None:
            raise Exception('UrlFinder needs a dispatcher to work properly')
        self.url_extractor = kwargs.get('url_extractor', None)
        if self.url_extractor is None:
            self.url_extractor = UrlExtractor()
        self.download_dispatcher = kwargs.get('download_dispatcher', None)
        if self.download_dispatcher is None:
            print 'Download dispatcher not defined.'
        self.download_pattern = kwargs.get('download_pattern', None)
        if self.download_pattern is None:
            print 'Download pattern not defined'
        kwargs = {} #Thread init doesn't expect any of our kwargs.
        Thread.__init__(self, *args, **kwargs)
        self.start()
        
    def look_for_page(self):
        result = None
        try:
            self.page = self.__get_pending_page()
        except OperationalError:
            print '\nDatabase on lock \n'

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
                    print '\nDatabase on lock \n'
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
                    url_download = url_download.save()
                    download_urls.append(url_download)
                    urls.remove(url)
            elif _class == UrlClasses.FETCH and Url.manager.exists(url.url):
                urls.remove(url)
            else:
                urls.remove(url)
                url = url.save()
                urls.append(url)

        self.page.is_parsed = True
        self.page.save()

        self.dispatcher.fill_pool(urls)
        if self.download_dispatcher:
            self.download_dispatcher.fill_pool(download_urls)