__author__ = 'rubico'

import urllib2
import cgi
import Settings
import os
from Fetcher import Fetcher
from datetime import datetime


class FileFetcher(Fetcher):
    """
        This class is extremely coupled.
        Need a refactor urgent.
    """
    file = None
    file_total_size = 0

    def fetch_url(self):
        request = urllib2.Request(self.work)
        request.add_header('Referer', Settings.referer)
        filename = ''
        file_path = ''
        try:
            response = urllib2.urlopen(request)
            self.file_total_size = int(response.info().getheaders('Content-Length')[0])
            filename = self.__get_file_name(response)
            file_path = Settings.storage_path+filename
            self.file = open(file_path, 'wb+')
            self.file.write(response.read())
            self.file.close()
        except:
            self.dispatcher.fill_pool([self.work,])
            print '\n ### '+str(datetime.now())+' ' + self.work.url+'\n'

        if self.file and not self.__check_file_download(file_path):
            os.remove(file_path)
            self.dispatcher.fill_pool([self.work,])
            print '\tDownload not completed: %s' % (filename,)

    def __get_file_name(self, response):
        _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        filename = params['filename']
        return filename

    def __check_file_download(self, file_path):
        return os.stat(file_path).st_size == self.file_total_size
