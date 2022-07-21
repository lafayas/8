import unittest
import requests
from parameterized import parameterized
from api import log
from api.api_approve_trust import ApiApproveTrust
from api.api_register_login import ApiRegisterLogin
from util import parser_html, read_json, clear_data


class TestApproveTrust(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 清除数据
        clear_data()
    # 初始化
    def setUp(self) -> None:
        # 1、获取session
        self.session = requests.Session()
        # 2、获取ApiApproveTrust对象
        self.approve = ApiApproveTrust(self.session)
        # 3、调用登录成功
        ApiRegisterLogin(self.session).api_login()

    # 结束
    def tearDown(self) -> None:
        self.session.close()

    # 1、认证接口 测试
    def test01_approve(self):
        try:
            # 调用认证接口
            r = self.approve.api_approve()
            log.info("接口执行结果为: {}".format(r.text))
            # 断言
            self.assertIn("提交成功", r.text)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 2、查询认证状态接口 测试
    def test02_approve_status(self):
        try:
            # 调用认证接口
            r = self.approve.api_approve_status()
            log.info("接口执行结果为: {}".format(r.text))
            # 断言
            self.assertIn("华", r.text)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 3、开户接口 测试
    def test03_trust(self):
        try:
            # 调用认证接口
            r = self.approve.api_trust()
            log.info("接口执行结果为: {}".format(r.json()))
            # 断言
            self.assertIn("form", r.text)
            print("请求后台开户结果为: ", r.json())
            log.info("断言通过！")
            # 三方开户
            result = parser_html(r)
            # 期望 http://xxx,{"version": "10",})
            r = self.session.post(url=result[0], data=result[1])
            log.info("接口执行结果为: {}".format(r.text))
            print("三方开户的结果为: ", r.text)
            self.assertIn("OK", r.text)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 4、获取图片验证码接口 测试
    @parameterized.expand(read_json("approve_trust.json", "img_code"))
    def test04_img_code(self, random, expect_code):
        try:
            # 调用接口
            r = self.approve.api_img_code(random)
            log.info("接口执行结果为: {}".format(r.status_code))
            # 断言
            self.assertEqual(expect_code, r.status_code)
            log.info("断言通过！")
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise

    # 5、充值接口 测试
    @parameterized.expand(read_json("approve_trust.json", "recharge"))
    def test05_recharge(self, valicode, expect_text):
        try:
            # 调用图片验证码
            self.approve.api_img_code(123123)
            # 调用接口
            r = self.approve.api_recharge(valicode)
            log.info("接口执行结果为: {}".format(r.json()))
            if valicode == 8888:
                # 断言
                self.assertIn("form", r.text)
                log.info("断言通过！")
                # 三方充值
                result = parser_html(r)
                # 期望 http://xxx,{"version": "10",})
                r = self.session.post(url=result[0], data=result[1])
                log.info("接口执行结果为: {}".format(r.text))
                print("三方充值的结果为: ", r.text)
                self.assertIn(expect_text, r.text)
                log.info("断言通过！")
            else:
                self.assertIn(expect_text, r.text)
                print("验证码错误, 响应结果为: ", r.text)
        except Exception as e:
            # 日志
            log.error("断言错误！原因: {}".format(e))
            # 抛异常
            raise
