# 读取json工具
import json
import os
import logging.handlers
from config import DIR_PATH
from bs4 import BeautifulSoup
import pymysql


def read_json(filename, key):
    # 拼接读取文件的完整路径 os.sep动态获取/ \
    file_path = DIR_PATH + os.sep + "data" + os.sep + filename
    arr = []
    with open(file_path, "r", encoding="utf-8") as f:
        for data in json.load(f).get(key):
            arr.append(tuple(data.values())[1:])
    return arr


# 日志工具
class GetLog:
    log = None

    @classmethod
    def get_log(cls):
        cls.log = None
        if cls.log is None:
            # 1、获取日志器
            cls.log = logging.getLogger()
            # 设置日志级别 info
            cls.log.setLevel(logging.INFO)
            filepath = DIR_PATH + os.sep + "log" + os.sep + "p2p.log"
            # 2、获取处理器 TimedRotatingFileHandler: 日志保存到文件且根据时间去分割
            tf = logging.handlers.TimedRotatingFileHandler(filename=filepath, when="midnight", interval=1,
                                                           backupCount=3, encoding="utf-8")
            # 3、获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)

            # 4、将格式器添加到处理器中
            tf.setFormatter(fm)
            # 5、将处理器添加到日志器中
            cls.log.addHandler(tf)
        # 返回日志器
        return cls.log


# 提取html数据
def parser_html(result):
    # 1、提取html
    html = result.json().get("description").get("form")
    # 2、获取bs对象
    bs = BeautifulSoup(html, "html.parser")
    # 3、提取url
    url = bs.form.get("action")
    data = {}
    # 4、查找所有的input标签
    for input in bs.find_all("input"):
        data[input.get("name")] = input.get("value")
    return url, data
    # 5、遍历进行组装   data = {"version": "10", "xxx": "xxx"}


"""
    分析:
        查询语句: 返回所有的结果
        非查询语句: 返回受影响的行数DML
"""


# 连接库工具
def conn_mysql(sql):
    conn = None
    cursor = None
    try:
        # 1、获取连接对象
        conn = pymysql.connect(host="121.43.169.97", user="root", password="", database="czbk_member", port=3306,
                               charset="utf8", autocommit=True)
        # 2、获取游标对象
        cursor = conn.cursor()
        # 3、执行sql语句
        cursor.execute(sql)
        # 判断sql语句是否为查询
        if sql.split()[0].lower() == 'select':
            # 返回所有结果
            return cursor.fetchall()
        # 否则
        else:
            # 返回受影响的行数
            return f"受影响的行数: {cursor.rowcount}"
    except Exception as e:
        GetLog.get_log().error(e)
        raise
    finally:
        # 4、关闭游标
        cursor.close()

        # 5、关闭连接
        conn.close()


# 清除方法
def clear_data():
    sql1 = """
    """
    conn_mysql(sql1)
    sql2 = """
    """
    conn_mysql(sql2)
    sql3 = """
        """
    conn_mysql(sql3)
    sql4 = """
        """
    conn_mysql(sql4)


if __name__ == '__main__':
    sql = "select * from mb_member"
    sql2 = "delete from mb_member where phone='15958585801' "
    print(conn_mysql(sql2))
