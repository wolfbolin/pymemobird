# -*- coding: utf-8 -*-


class User:
    """
    保存用户相关属性
    """
    access_key = None
    user_identify = None

    def __init__(self, access_key, user_identify):
        """
        初始化用户编号与访问凭证
        :param access_key: 开发者访问凭证
        :param user_identify: 用户身份标识
        """
        self.access_key = access_key
        self.user_identify = user_identify

    def is_init(self):
        if self.access_key is None or self.user_identify is None:
            return False
        else:
            return True
