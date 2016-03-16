__author__ = 'rubico'

import urllib2
import cgi
import os
import time
from datetime import datetime

import Settings
from Fetcher import Fetcher


class FileFetcher(Fetcher):

    RETRY_TIME = 3

    file = None
    server_file_size = 0
    file_path = ''
    file_name = ''
    refer_url = None

    def __init__(self, dispatcher, *args, **kwargs):
        self.refer_url = kwargs.get('refer_url', None)
        self.file_path = kwargs.get('file_path', '')
        if self.file_path is None:
            raise Exception('FileFetcher needs a file path to work properly.')
        kwargs = {}  # Thread.__init__ doesn't expect a kwargs refer_url
        super(FileFetcher, self).__init__(dispatcher, *args, **kwargs)

    def fetch_url(self):
        try:
            request = urllib2.Request(self.work.url)
            if self.refer_url:
                request.add_header('Referer', self.refer_url)

            response = urllib2.urlopen(request)
            self.__extract_filepath(response)
            self.__get_server_file_size(response)

            print("\033[93m {}\033[00m" .format(str(datetime.now())+': Download started for: '+self.file_name))

            content = response.read()
            self.__write_file(content)

            while not self.__is_download_complete():
                time.sleep(self.RETRY_TIME)
                self.__resume_download()
                print("\033[94m {}\033[00m" .format(str(datetime.now())+': '+self.file_name+': '+str(int((float(self.__get_local_file_size())/self.server_file_size)*100))+'%'))

            self.work.is_downloaded = True
            self.work.save()
            print("\033[92m {}\033[00m" .format(str(datetime.now())+': Download complete for: '+self.work.url+' - '+self.file_name))
        except urllib2.URLError:
            self.dispatcher.fill_pool([self.work,])
            print("\033[91m {}\033[00m" .format(str(datetime.now())+': '+self.file_name))

    def __extract_filepath(self, response):
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        self.file_name = params['filename']
        self.__normalize_file_name()
        self.file_path = Settings.storage_path + self.file_name

    def __normalize_file_name(self):
        self.file_name = self.file_name.replace(':', '').replace('\\', '').replace('/', '')

    def __get_server_file_size(self, response):
        self.server_file_size = int(response.info().getheaders('Content-Length')[0])

    def __get_local_file_size(self):
        return os.stat(self.file_path).st_size

    def __is_download_complete(self):
        return self.__get_local_file_size() == self.server_file_size

    def __resume_download(self):
        request = urllib2.Request(self.work.url)
        if self.refer_url:
            request.add_header('Referer', self.refer_url)
        request.add_header('Range', 'bytes=%d-' % (self.__get_local_file_size(),))

        response = urllib2.urlopen(request)
        content = response.read()
        self.__write_file(content, 'ab+')

    def __write_file(self, content, mode='wb+'):
        self.file = open(self.file_path, mode)
        self.file.write(content)
        self.file.close()