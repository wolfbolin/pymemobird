# -*- coding: utf-8 -*-
# Common package
import json
import requests
# Personal package
from .util import Util


class Device:
    """
    打印机相关参数与函数
    """
    user_id = None
    access_key = None
    memobird_id = None

    def __init__(self, memobird_id):
        """
        初始化打印机编号
        :param memobird_id: 咕咕机设备编号
        """
        self.memobird_id = memobird_id

    def is_init(self):
        if self.memobird_id is None:
            return False
        else:
            return True

    def is_bind(self):
        """
        检查打印机是否与用户绑定
        :return: 绑定状态True/False
        """
        if self.memobird_id is None or self.user_id is None:
            return False
        else:
            return True

    def bind_user(self, user):
        """
        将打印机与用户绑定，获取API_ID
        :param user: 用户类
        :return: Device设备对象
        """
        if user.is_init() and self.is_init():
            data = {
                'ak': user.access_key,
                'timestamp': Util.time_stamp(),
                'memobirdID': self.memobird_id,
                'useridentifying': user.user_identify
            }
            http_result = requests.get(Util.api_url('bind'), data=data)
            if http_result.status_code == 200:
                Util.print_g('绑定用户...OK {}'.format(http_result.status_code))
            else:
                Util.print_r('绑定用户...RE {}'.format(http_result.status_code))
                raise Util.NetworkError('绑定用户失败：HTTP {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['showapi_res_code'] != 1:
                raise Util.NetworkError('绑定设备失败：%s' % json_data['showapi_res_error'])
            else:
                self.access_key = user.access_key
                self.user_id = json_data['showapi_userid']
            return self
        else:
            raise Util.OperateError('用户或设备类未完成初始化')

    def print_paper(self, paper):
        """
        打印纯文本纸条
        :param paper: 被打印的纸条对象
        :return: Paper纸条对象
        """
        if self.is_bind():
            data = {
                'ak': self.access_key,
                'timestamp': Util.time_stamp(),
                'memobirdID': self.memobird_id,
                'userID': self.user_id,
                'printcontent': paper.get_content()
            }
            http_result = requests.get(Util.api_url('print'), data=data)
            if http_result.status_code == 200:
                Util.print_g('打印纸条...OK {}'.format(http_result.status_code))
            else:
                Util.print_r('打印纸条...RE {}'.format(http_result.status_code))
                raise Util.NetworkError('纸条打印失败：HTTP {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['showapi_res_code'] != 1:
                raise Util.NetworkError('纸条打印失败：%s' % json_data['showapi_res_error'])
            else:
                # 修改纸条发送状态（信息填充）
                paper.update(json_data['printcontentid'], json_data['result'])
                return paper
        else:
            raise Util.OperateError('设备未绑定用户或未成功')
