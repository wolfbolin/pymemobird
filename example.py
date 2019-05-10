# -*- coding: utf-8 -*-
import time
import base64
import pymemobird

if __name__ == '__main__':
    # 申请到的开发者编号
    access_key = '7ffa6c1fc9f340e6969c74f1d4b6aa50'

    # 初始化用户
    user_identify = '2778553'
    user = pymemobird.User(access_key, user_identify)
    print('用户初始化...%s' % user.is_init())  # 验证初始化（可选）

    # 初始化设备
    memobird_id = '9d15e1b2671043ee'
    device = pymemobird.Device(memobird_id)
    print('设备初始化...%s' % device.is_init())  # 验证初始化（可选）

    # 绑定用户
    device.bind_user(user)
    print('绑定用户...%s' % device.is_bind())  # 验证绑定状态（可选）

    # 初始化纸条
    paper = pymemobird.Paper(access_key)
    print('纸条初始化...%s' % paper.is_init())  # 验证初始化（可选）

    # 向纸条中添加文本和图片
    paper.add_text('Hello,world!你好呀！')
    pic = open('Logo.jpg', 'rb')
    paper.add_pic(pic)
    pic.close()
    pic = open('Logo.jpg', 'rb')
    pic_data = pic.read()
    pic_base64 = base64.b64encode(pic_data)
    paper.add_base64_pic(pic_base64)
    pic.close()

    # 打印纸条相关操作
    print('开始打印...%s' % paper.is_send())  # 验证纸条是否已经发送至打印列表
    device.print_paper(paper)  # 打印纸条
    print('开始打印...%s' % paper.is_send())  # 验证纸条是否已经发送至打印列表
    while paper.status() == 'printing':
        time.sleep(1)
        paper.sync()  # 刷新纸条打印状态
        print('打印状态...%s' % paper.status())  # 获取纸条打印状态
