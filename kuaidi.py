# coding = utf-8
import hashlib
import json
from flask import Flask, request
import requests
from ast import literal_eval


class KuaiDi100:
    def __init__(self):
        self.key = 'vSMrDIyO9655'  # TODO 客户授权key
        self.customer = '5B0B1D325BB4BAF4AF9C9437B2344811'  # TODO 查询公司编号
        self.url = 'https://poll.kuaidi100.com/poll/query.do'  # 请求地址

    def track(self, com, num, phone, ship_from, ship_to):
        """
        物流轨迹实时查询
        :param com: 查询的快递公司的编码，一律用小写字母
        :param num: 查询的快递单号，单号的最大长度是32个字符
        :param phone: 收件人或寄件人的手机号或固话（也可以填写后四位，如果是固话，请不要上传分机号）
        :param ship_from: 出发地城市，省-市-区，非必填，填了有助于提升签收状态的判断的准确率，请尽量提供
        :param ship_to: 目的地城市，省-市-区，非必填，填了有助于提升签收状态的判断的准确率，且到达目的地后会加大监控频率，请尽量提供
        :return: requests.Response.text
        """
        param = {
            'com': com,
            'num': num,
            'phone': phone,
            'from': ship_from,
            'to': ship_to,
            'resultv2': '1',  # 添加此字段表示开通行政区域解析功能。0：关闭（默认），1：开通行政区域解析功能，2：开通行政解析功能并且返回出发、目的及当前城市信息
            'show': '0',  # 返回数据格式。0：json（默认），1：xml，2：html，3：text
            'order': 'desc'  # 返回结果排序方式。desc：降序（默认），asc：升序
        }
        param_str = json.dumps(param)  # 转json字符串

        # 签名加密， 用于验证身份， 按param + key + customer 的顺序进行MD5加密（注意加密后字符串要转大写）， 不需要“+”号
        temp_sign = param_str + self.key + self.customer
        md = hashlib.md5()
        md.update(temp_sign.encode())
        sign = md.hexdigest().upper()
        # print(sign)
        request_data = {'customer': self.customer, 'param': param_str, 'sign': sign}
        # print(request_data)
        return requests.post(self.url, request_data).text  # 发送请求


class KuaiDi1002:
    def __init__(self):
        self.key = 'vSMrDIyO9655'  # TODO 客户授权key
        self.url = 'https://www.kuaidi100.com/autonumber/auto'  # 请求地址

    def auto_number(self, num):
        """
        智能单号识别
        :param num: 快递单号
        :return: requests.Response.text
        """
        codema=''
        req_params = {'key': self.key, 'num': num}
        kuaidi_code = requests.post(self.url, req_params).text
        new_list = literal_eval(kuaidi_code)

        kuaidi_name=new_list[0]["name"]
        # print(kuaidi_name)
        for i in new_list:
            codema = i["comCode"]
        return codema





input = input("输入快递单号:")
# input=""
result = KuaiDi1002().auto_number(input)
result = KuaiDi100().track(result, input, '', '', '')
json_object = json.loads(result)
for i in json_object["data"]:
    print(i["ftime"]+" ["+i["status"]+"] "+i["context"])

