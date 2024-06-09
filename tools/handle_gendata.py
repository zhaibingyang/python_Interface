import allure
from faker import Faker
from tools.handle_mysql import HandleMysql
from data.setting import my_db
from loguru import logger
@allure.step("生成随机的手机号码操作")
class GenData:
    def gen_unregister_phone(self):
        fk = Faker(locale='zh_CN')
        while True:
            # 1、生成随机的手机号码
            phone_number = fk.phone_number()  #手机号码
            # 2、去数据库查询是否已经存在了
            sql = f'select * from tz_user where user_mobile  = "{phone_number}";'
            sql_result = HandleMysql(**my_db).query_data(sql)  # 要么是字典，要么是None
            if sql_result is None:
                logger.info(f"生成的可以用的手机号码是:{phone_number}")
                return phone_number  # 用了函数的话 不需要break return直接会结束函数运行

    def gen_unregister_name(self):
        fk = Faker(locale='zh_CN')
        while True:
            # 1、生成随机的手机号码
            user_name = fk.pystr(min_chars=4,max_chars=16)  #手机号码
            # 2、去数据库查询是否已经存在了
            sql = f'select * from tz_user where nick_name  = "{user_name}";'
            sql_result = HandleMysql(**my_db).query_data(sql)  # 要么是字典，要么是None
            if sql_result is None:
                logger.info(f"生成的可以用的手机号码是:{user_name}")
                return user_name  # 用了函数的话 不需要break return直接会结束函数运行

if __name__ == '__main__':
    print('GenData().gen_unregister_phone()')
    # 执行引号里的函数 --eval()
    print(eval('GenData().gen_unregister_phone()'))

    print(GenData().gen_unregister_name())