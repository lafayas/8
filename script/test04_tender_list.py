import unittest

import requests
from parameterized import parameterized
from api.api_approve_trust import ApiApproveTrust
from api import log
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util import parser_html, read_json, clear_data


class TestTenderList(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 清除数据
        clear_data()
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegisterLogin对象
        self.reg = ApiRegisterLogin(self.session)
        # 获取ApiApproveTrust对象
        self.approve = ApiApproveTrust(self.session)
        # 获取ApiTender对象
        self.tender = ApiTender(self.session)

    def tearDown(self) -> None:
        # 关闭session
        self.session.close()

    def test01_tender_list(self):
        phone = "13612341113"
        img_code = 8888
        pwd = "test123"
        phone_code = 666666
        card_id = "630102199003072373"
        # 1、获取图片验证码
        self.reg.api_img_code(123123)
        # 2、获取短信验证码
        self.reg.api_phone_code(phone, img_code)
        # 3、注册
        self.reg.api_register(phone, pwd, img_code, phone_code)
        # 4、登录
        self.reg.api_login(phone, pwd)
        # 5、认证
        self.approve.api_approve(card_id)
        # 6、后台开户
        r = self.approve.api_trust()
        # 7、三方开户
        result = parser_html(r)
        # 期望 http://xxx,{"version": "10",})
        r = self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为: {}".format(r.text))
        print("三方开户的结果为: ", r.text)
        self.assertIn("OK", r.text)
        log.info("断言通过！")
        # 8、获取充值验证码
        self.approve.api_img_code(123123)
        # 9、后台充值
        r = self.approve.api_recharge(img_code)
        # 10、三方充值
        result = parser_html(r)
        # 期望 http://xxx,{"version": "10",})
        r = self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为: {}".format(r.text))
        print("三方充值的结果为: ", r.text)
        self.assertIn("OK", r.text)
        log.info("断言通过！")
        # 11、后台投资
        r = self.tender.api_tender(100)
        # 12、三方投资
        result = parser_html(r)
        # 期望 http://xxx,{"version": "10",})
        r = self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为: {}".format(r.text))
        print("三方投资的结果为: ", r.text)
        self.assertIn("OK", r.text)
        log.info("断言通过！")
