__author__ = 'rubico'

import urllib2
import cgi
import os
import time

import Settings
from Fetcher import Fetcher


class FileFetcher(Fetcher):

    file = None
    server_file_size = 0
    file_path = ''
    refer_url = None

    def __init__(self, dispatcher, *args, **kwargs):
        super(FileFetcher, self).__init__(dispatcher, *args, **kwargs)
        self.refer_url = kwargs.get('refer_url', None)

    def fetch_url(self):
        request = urllib2.Request(self.work)
        if self.refer_url:
            request.add_header('Referer', self.refer_url)

        response = urllib2.urlopen(request)
        self.__extract_filepath(response)

        content = response.read()
        self.__write_file(content)

        while not self.__is_download_complete():
            time.sleep(self.wait_time)
            self.__resume_download()

    def __extract_filepath(self, response):
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        file_name = params['filename']
        self.file_path = Settings.storage_path + file_name

    def __get_server_file_size(self, response):
        self.server_file_size = int(response.info().getheaders('Content-Length')[0])

    def __get_local_file_size(self):
        return os.stat(self.file_path).st_size

    def __is_download_complete(self):
        return self.__get_local_file_size() == self.server_file_size

    def __resume_download(self):
        request = urllib2.Request(urllib2)
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

