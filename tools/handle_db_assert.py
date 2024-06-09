import json

import allure

from tools.handle_mysql import HandleMysql
from data.setting import my_db
from loguru import logger
from tools.handle_replace import replace_mark
@allure.step("做数据库断言")
def db_assert(db_assert_data):
    if db_assert_data is None:
        return
    logger.info("==========================数据库断言开始了！===========================")
    # 加一步： 先替换占位符-得到直接可用sql
    db_assert_data = replace_mark(db_assert_data)

    # 第一步： 反序列化转化为字典
    db_assert_data = json.loads(db_assert_data)
    logger.info(f"数据库断言的表达式：{db_assert_data}")
    # 第二步： for循环取到k  v
    for k,v in db_assert_data.items(): # k- sql语句，v- 预期结果
        # 第三步： 用k-sql 调用数据库方法查询数据库结果
        sql_result = HandleMysql(**my_db).query_data(k) #结果是{'count(1)': 1}，{'status': 2}
        # 第四步： 拿到数据库结果字典的value值--执行结果 ，跟预期结果-v 断言
        for i in sql_result.values(): # 通过for循环取values -拿到执行结果数据
            logger.info(f"数据库查询的实际结果：{i}")
            logger.info(f"数据库查询的预期结果：{v}")
            try:
                assert i == v
                logger.info("数据库断言成功！")
            except AssertionError as err:
                logger.error("数据库断言失败！")
                raise err

if __name__ == '__main__':
    db_assert_data = '''{"select count(1) from tz_order where order_number = '1796523031183757312'":1, 
    "select status from tz_order where order_number = '1796523031183757312'":1}'''
    db_assert(db_assert_data)