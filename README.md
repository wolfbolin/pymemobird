# pymemobird
![Windows](https://img.shields.io/badge/Windows-support-green.svg)
![Linux](https://img.shields.io/badge/Linux-support-green.svg)
![Python](https://img.shields.io/badge/Python-3.6-blue.svg)
![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)

咕咕机开发工具包，Github源码地址：[https://github.com/wolfbolin/pymemobird](https://github.com/wolfbolin/pymemobird)

> 本工具包使用官方提供的API接口进行开发，支持常用接口的调用。采用面向对象的编程形式，减少使用者对调用过程的学习过程。理论上可在全系列的打印机上运行，采用蓝牙的打印机需要保持手机连接。

*更新日志请看到 [更新日志](#三、更新日志)，开发者主页 [https://wolfbolin.com](https://wolfbolin.com)*

## 一、安装方式

请使用pip安装该工具包

```
$ pip install pymemobird
```

## 二、使用说明

### 1、使用前提

首先你需要拥有一台**咕咕机**并且申请开发者KEY，开发者权限申请网址：[http://open.memobird.cn](http://open.memobird.cn)

#### 1.1、数据字典

| 单词          | 示例                             | 含义                  |
| ------------- | -------------------------------- | --------------------- |
| access_key    | 7ffa6c1fc9f340e6969c74f1d4b6aa50 | 开发者凭证/申请的ak值 |
| user_identify | 2778553                          | 咕咕号/用户唯一标识符 |
| user_id       | 840268                           | 绑定设备后的用户凭证  |
| memobird_id   | 9d15e1b2671043ee                 | 咕咕机设备编号        |
| paper_id      | 35331944                         | 纸条编号              |
| print_flag    | 'success','printing','error'     | 纸条状态              |
| http_proxy    | "http://127.0.0.1:12639"         | HTTP网络代理          |
| https_proxy   | "https://example.com"            | HTTPS网络代理         |



#### 1.2、代码样例

```python
# coding=utf-8
import time
import base64
import pymemobird

pymemobird.http_proxy = "http://127.0.0.1:12639"

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

```



### 2、用户类User

该类功能较少，仅保存了用户的凭证信息

#### 2.1、声明用户类

* 函数名
  * `__init__(self, access_key, user_identify)`

* 参数
  * `access_key`：开发者访问凭证
  * `user_identify`：用户身份标识

#### 2.2、初始化验证

验证用户实例是否已经传入的初始化参数

* 函数名
  * `is_init(self)`

* 参数
  * 无
* 返回
  * 检测结果True/False

### 3、设备类Device

完成设备绑定，纸条打印等功能

#### 3.1、声明用户类

* 函数名
  
* `__init__(self, memobird_id)`
  
* 参数
  * `memobird_id`：咕咕机设备编号
  

#### 3.2、初始化验证

验证设备实例是否已经传入的初始化参数

* 函数名
  * `is_init(self)`

* 参数
  * 无
* 返回
  * 检测结果True/False

#### 3.3、用户绑定

将用户标识与设备关联，获取纸条发送的凭证信息

- 函数名
  - `bind_user(self, user)`
- 参数
  - 用户类（User）实例
- 返回
  - 修改并返回设备实例
- 异常
  - 操作异常OperateError：使用未完成初始化的类
  - 网络异常NetworkError：在绑定设备时发生异常

#### 3.4、绑定验证

验证设备实例是否已经绑定用户

- 函数名
  - `is_bind(self)`
- 参数
  - 无
- 返回
  - 检测结果True/False

#### 3.5、打印纸条

将纸条类中的信息发送至打印队列，并更新纸条状态。一条纸条可以发送多次。

- 函数名
  - `print_paper(self, paper)`
- 参数
  - 纸条类（Paper）实例
- 返回
  - 修改并返回纸条实例
- 异常
  - 操作异常OperateError：使用未完成初始化的类
  - 网络异常NetworkError：在打印纸条时发生异常

### 4、纸条类Paper

该类可完成纸条内容的连接，并可以刷新纸条打印状态

#### 4.1、声明用户类

- 函数名
- `__init__(self, access_key)`
- 参数
  - `access_key`：开发者访问凭证

#### 3.2、初始化验证

验设备实例是否已经传入的初始化参数

- 函数名
  - `is_init(self)`
- 参数
  - 无
- 返回
  - 检测结果True/False

#### 3.3、纸条发送验证

验证纸条打印任务是否已经发送至打印队列

- 函数名
  - `is_send(self)`
- 参数
  - 无
- 返回
  - 检测结果True/False



#### 3.4、添加文本

在纸条最后添加文本（并不会立即打印），可以多次添加。

- 函数名
  - `add_text(self, text)`
- 参数
  - `text`：需要在纸条上打印的纯文本信息，支持中文（GBK）打印，支持转义符
- 返回
  - 修改并返回纸条类（Paper）实例

#### 3.5、添加图片

在纸条最后添加图片（并不会立即打印），可以多次添加。

程序将利用官方API完成图片的预处理，不使用PIL

- 函数名
  - `add_pic(self, file)`
- 参数
  - `file`：需要在纸条上打印的图片对象（需要支持read()获取字符串的对象即可），支持JPG、PNG格式
- 返回
  - 修改并返回纸条类（Paper）实例
- 异常
  - 操作异常OperateError：使用未完成初始化的类
  - 网络异常NetworkError：在打印纸条时发生异常

#### 3.6、添加Base64图片

在纸条最后添加Base64编码的图片（并不会立即打印），可以多次添加。

程序将利用官方API完成图片的预处理，不使用PIL

- 函数名
  - `add_base64_pic(self, file)`
- 参数
  - `file`：图片经过Base64编码的字符串，支持JPG、PNG格式
- 返回
  - 修改并返回纸条类（Paper）实例
- 异常
  - 操作异常OperateError：使用未完成初始化的类
  - 网络异常NetworkError：在打印纸条时发生异常

#### 3.7、获取打印状态

获取当前纸条的打印状态，可能的状态有`success`,`printing`,`error`

- 函数名
  - `status(self, file)`
- 参数
  - 无
- 返回
  - 返回纸条的打印状态
- 异常
  - 操作异常OperateError：使用未完成初始化的类

#### 3.8、同步纸条状态

同步此刻该纸条的打印状态

- 函数名
  - `sync(self)`
- 参数
  - 无
- 返回
  - 修改并返回纸条类（Paper）实例
- 异常
  - 操作异常OperateError：使用未完成初始化的类
  - 网络异常NetworkError：在打印纸条时发生异常

#### 3.9、获取纸条全文

响应值为经过编码的纸条内容。

包内部调用，若有需要请查看源码。

#### 3.10、更新纸条状态

包内部调用，若有需要请查看源码。

### 三、更新日志

### v0.2.2

新增

* 新增代理配置，适应在复杂网络环境下的代理需求

修复

* 换用POST接口，修复GET接口在代理模式下的异常

### v0.2.1

修复

* 多次声明纸条对象时，旧数据未清空导致的重复打印问题。

### v0.2.0

正式版

测试问题：纸条打印顺序与添加顺序不同

新增功能：`add_base64_pic`函数，可实现图片Base64数据直接添加。

### v0.1.0

正式版

通过测试，修复若干BUG，样例可运行

### v0.0.1

测试版



****

**Designed by WolfBolin**

![Logo](Logo.jpg)



