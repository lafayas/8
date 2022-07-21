import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util import parser_html, read_json, clear_data


class TestTender(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 清除数据
        clear_data()
    # 初始化
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.Session()
        # 获取 ApiTender对象
        self.tender = ApiTender(self.session)
        # 调用登录
        ApiRegisterLogin(self.session).api_login()

    # 结束
    def tearDown(self) -> None:
        self.session.close()

    # 测试方法
    @parameterized.expand(read_json("tender.json", "tender"))
    def test01_tender(self, amount, expect_text):
        try:
            # 调用投资方法
            r = self.tender.api_tender(amount)
            if amount == 100:
                # 调用三方投资
                result = parser_html(r)
                # 期望 http://xxx,{"version": "10",})
                r = self.session.post(url=result[0], data=result[1])
                log.info("接口执行结果为: {}".format(r.text))
                print("三方投资的结果为: ", r.text)
                # 断言
                self.assertIn(expect_text, r.text)
                log.info("断言通过！")
            else:
                self.assertIn(expect_text, r.text)
        except Exception as e:
            log.error(e)
            raise
