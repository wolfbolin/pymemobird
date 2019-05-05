# -*- coding: utf-8 -*-
# Common package
import time


# Personal package

class Util:
    class OperateError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class NetworkError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    @staticmethod
    def time_stamp():
        utc = time.time()
        local = time.localtime(utc)
        stamp = time.strftime('%Y-%m-%d %H:%M:%S', local)
        return stamp

    @staticmethod
    def api_url(suffix):
        if suffix == 'bind':
            return 'http://open.memobird.cn/home/setuserbind'
        elif suffix == 'print':
            return 'http://open.memobird.cn/home/printpaper'
        elif suffix == 'status':
            return 'http://open.memobird.cn/home/getprintstatus'
        elif suffix == 'pic':
            return 'http://open.memobird.cn/home/getSignalBase64Pic'

    @staticmethod
    def print_0(message, end='\n'):
        print('\033[0;30;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_1(message, end='\n'):
        print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_r(message, end='\n'):
        print('\033[0;31;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_g(message, end='\n'):
        print('\033[0;32;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_y(message, end='\n'):
        print('\033[0;33;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_b(message, end='\n'):
        print('\033[0;34;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_cyan(message, end='\n'):
        # 青色
        print('\033[0;36;0m{}\033[0m'.format(str(message)), end=end)

    @staticmethod
    def print_gray(message, end='\n'):
        # 灰色
        print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)
