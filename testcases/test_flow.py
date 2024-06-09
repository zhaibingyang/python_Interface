import allure
import pytest
from tools.handle_excel import read_excel
from tools.handle_path import case_path
from tools.handle_response_assert import response_assert
from tools.handle_requests import requests_api
from tools.handle_db_assert import db_assert

#第一步： 调用这个读取excel函数，得到所有登录模块测试用例
case_all = read_excel(case_path,"业务流5")
# 添加这行代码就可以把excel用例的标题 作为用例的标题展示
@allure.title("{case[用例标题]}")
#第二步： 用pytest框架执行这模块用例
@pytest.mark.parametrize("case",case_all)
def test_login_case(case):  #调用登录的夹具
    expected = case["预期结果"]
    db_assert_data = case["数据库断言"]
    resp = requests_api(case)  #传参 token值
    #调用封装好的断言方法
    response_assert(expected,resp)
    # 调用数据库断言方法
    db_assert(db_assert_data)