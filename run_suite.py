"""
    报告: htmltestreport
"""

# 1、导包
import os

from htmltestreport import HTMLTestReport
import unittest
from config import DIR_PATH

# 2、组合测试套件


suite = unittest.defaultTestLoader.discover("./script", pattern="test*.py")

# 指定测试报告存储路径
report_path = DIR_PATH + os.sep + "report" + os.sep + "p2p.html"
# 3、执行测试套件
HTMLTestReport(report_path, title="p2p接口自动化测试报告").run(suite)
