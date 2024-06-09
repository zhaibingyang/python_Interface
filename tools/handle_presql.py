import json

import allure

from tools.handle_mysql import HandleMysql
from data.setting import my_db
from data.envi_data import EnviData
from loguru import logger
@allure.step("前置SQL操作")
def pre_sql(sql_data):
    if sql_data is None:
        return
    logger.info("==========================前置sql执行开始=========================")
    # 第一步： 进行反序列化转化为字典
    sql_data = json.loads(sql_data)
    logger.info(f"前置sql提取表达式是：{sql_data}")
    # 第二步： 读取这个前置sql，for循环k v 得到这个变量和sql语句，sql去数据库里查
    for k,v in sql_data.items(): # k是变量名，v是sql语句
        #第三步：v是sql，调用我们之前封装的sql的类方法，得到的结果是个字典
        sql_result = HandleMysql(**my_db).query_data(v)  #数据库查询得到结果- 字典 {'mobile_code': '093271'}
        # 第四步： 查完后结果存储在环境变量作为属性。属性名就是k 变量名；
        for i,j in sql_result.items():
            setattr(EnviData,i,j) # 把数据库查询结果的键值 存到环境变量里： 属性名= 属性值
    logger.info(f"查询结果存到环境变量后属性为：{EnviData.__dict__}")

if __name__ == '__main__':
    sql_data = '''{"mobile_code":
    "select mobile_code  from tz_sms_log where user_phone='13422337768' order by rec_date desc limit 1;"}'''
    pre_sql(sql_data)