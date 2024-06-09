import allure
import pymysql
from pymysql.cursors import DictCursor
from loguru import logger
@allure.step("连接数据库操作")
class HandleMysql:
    def __init__(self,user,password,database,port,host):
        """
        多个方法都要共享数据库连接 conn，共享curs需要定义实例属性。
        """
        self.conn = pymysql.connect(
            user=user,
            password=password,
            database=database,
            port=port,
            host=host,
            charset="utf8mb4",
            cursorclass=DictCursor
        )
        self.curse = self.conn.cursor()

    def query_data(self,sql,fetch_num=1,size=None):  #size当fetch_num 为1和-1的时候 没意义的，所以设置一个默认值 不需要传参
        """
        这是一个数据库查询的函数，可以选择获取几条数据查询结果
        :param sql: 传入查询sql语句
        :param fetch_num: 输入你要获取的数据库的条数：【输入1：获取1条，输入2：获取多条，输入-1:获取所有】
                           大部分情况查询较多，所以可以设置一个默认值为1
        :param size: 这个参数只有当fetch_num=2的时候才需要传入，控制具体获取几条数据
        :return: 返回最终的查询结果数据。 如果没有任何数据查询到 这个实例方法返回值是 None
        """
        try:
            result = self.curse.execute(sql)
            logger.info(f"数据库的查询结果条数为{result}")
            if result > 0:
                if fetch_num == 1:
                    data = self.curse.fetchone()
                    logger.info(f"查询结果是：{data}")
                    return data
                elif fetch_num == 2:
                    data = self.curse.fetchmany(size=size)  #size为None 默认就是1条结果。
                    logger.info(f"查询结果是：{data}")
                    return data
                elif fetch_num == -1:
                    data = self.curse.fetchall()
                    logger.info(f"查询结果是：{data}")
                    return data
            logger.info("数据库没有查询到任何结果！")
        except Exception as err:
            logger.error(f"数据库操作异常了：{err}")
        finally: #不管有没有捕获异常都可以执行的代码
            self.curse.close()  # 关闭游标
            self.conn.close()  # 关闭连接

if __name__ == '__main__':
    from data.setting import my_db
    # 实例化类对象 调用实例方法
    sql = 'select user_phone ,mobile_code  from tz_sms_log where user_phone = "13455443321" order by rec_date desc;'
    print(HandleMysql(**my_db).query_data(sql))
