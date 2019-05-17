# -*- coding: utf-8 -*-
# Common package
import json
import base64
import requests
# Personal package
from .util import Util


class Paper:
    """
    保存纸条相关功能
    """
    content = []
    paper_id = None
    print_flag = None
    access_key = None

    def __init__(self, access_key):
        """
        初始化访问凭证
        :param access_key: 开发者访问凭证
        """
        self.content = []
        self.paper_id = None
        self.print_flag = None
        self.access_key = access_key

    def is_init(self):
        if self.access_key is None:
            return False
        else:
            return True

    def is_send(self):
        """
        检查纸条是否已被发送
        :return: 发送状态True/False
        """
        if self.paper_id is None or self.print_flag is None:
            return False
        else:
            return True

    def add_text(self, text):
        """
        添加文本类型纸条内容，兼容中文
        :param text: 需要打印的文本内容，支持转义符
        :return: Paper对象
        """
        content = base64.b64encode(text.encode('gbk'))
        self.content.append('T:{}'.format(str(content, 'utf8')))
        return self

    def add_pic(self, file):
        """
        添加图片类型纸条内容，兼容JPG、PNG
        通过网络完成图片转换，避免使用PIL
        :param file: 文件句柄或可read字符串的对象
        :return: Paper对象
        """
        if self.is_init():
            file_data = file.read()
            pic_base64 = base64.b64encode(file_data)
            data = {
                'ak': self.access_key,
                'imgBase64String': pic_base64
            }
            http_result = requests.get(Util.api_url('pic'), data=data)
            if http_result.status_code == 200:
                Util.print_g('转换图片...OK {}'.format(http_result.status_code))
            else:
                Util.print_r('转换图片...RE {}'.format(http_result.status_code))
                raise Util.NetworkError('转换图片失败：HTTP {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['showapi_res_code'] != 1:
                raise Util.NetworkError('转换图片失败：%s' % json_data['showapi_res_error'])
            else:
                self.content.append('P:{}'.format(json_data['result']))
                return self
        else:
            raise Util.OperateError('纸条类未完成初始化')

    def add_base64_pic(self, base64_pic):
        """
        添加图片类型纸条内容，兼容JPG、PNG
        通过网络完成图片转换，避免使用PIL
        :param base64_pic: 经过Base64编码的图片
        :return: Paper对象
        """
        if self.is_init():
            data = {
                'ak': self.access_key,
                'imgBase64String': base64_pic
            }
            http_result = requests.get(Util.api_url('pic'), data=data)
            if http_result.status_code == 200:
                Util.print_g('转换图片...OK {}'.format(http_result.status_code))
            else:
                Util.print_r('转换图片...RE {}'.format(http_result.status_code))
                raise Util.NetworkError('转换图片失败：HTTP {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['showapi_res_code'] != 1:
                raise Util.NetworkError('转换图片失败：%s' % json_data['showapi_res_error'])
            else:
                self.content.append('P:{}'.format(json_data['result']))
                return self
        else:
            raise Util.OperateError('纸条类未完成初始化')

    def get_content(self):
        """
        获取打印内容全文
        :return: 格式化纸条内容
        """
        if self.content is None or len(self.content) == 0 or isinstance(self.content, list) is False:
            raise Util.OperateError('未设置纸条内容，无法打印')
        else:
            return '|'.join(self.content)

    def update(self, pid=None, flag=None):
        """
        更新纸条打印状态
        :param pid: 纸条编号
        :param flag: 打印状态
        :return: 打印状态
        """
        self.paper_id = pid
        if flag == 1:
            self.print_flag = 'success'
        elif flag == 2 or flag == 0:
            self.print_flag = 'printing'
        else:
            self.print_flag = 'error'

    def status(self):
        """
        展示纸条打印状态
        :return:
        """
        if self.is_send():
            return self.print_flag
        else:
            raise Util.OperateError('纸条未发送至打印队列')

    def sync(self):
        """
        同步纸条打印状态
        :return: Paper对象
        """
        if self.is_send():
            data = {
                'ak': self.access_key,
                'timestamp': Util.time_stamp(),
                'printcontentid': self.paper_id
            }
            http_result = requests.get(Util.api_url('status'), data=data)
            if http_result.status_code == 200:
                Util.print_g('同步状态...OK {}'.format(http_result.status_code))
            else:
                Util.print_r('同步状态...RE {}'.format(http_result.status_code))
                raise Util.NetworkError('同步状态失败：HTTP {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['showapi_res_code'] != 1:
                raise Util.NetworkError('状态同步失败：%s' % json_data['showapi_res_error'])
            else:
                self.update(json_data['printcontentid'], json_data['printflag'])
                return self
        else:
            raise Util.OperateError('纸条内容未发送至打印机')
