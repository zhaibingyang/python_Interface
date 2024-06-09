import allure
import pytest
from tools.handle_excel import read_excel
from tools.handle_path import case_path
from tools.handle_response_assert import response_assert
from tools.handle_requests import requests_api

#第一步： 调用这个读取excel函数，得到所有登录模块测试用例
case_all = read_excel(case_path,"购物车")
# 添加这行代码就可以把excel用例的标题 作为用例的标题展示
@allure.title("{case[用例标题]}")
@allure.suite("添加购物车")
#第二步： 用pytest框架执行这模块用例
@pytest.mark.parametrize("case",case_all)
def test_login_case(case):  #调用登录的夹具
    expected = case["预期结果"]
    resp = requests_api(case)  #传参 token值
    #调用封装好的断言方法
    response_assert(expected,resp)
