"""
conftest夹具共享文件 写一个登录夹具
- 返回token ：
"""
import pytest
import requests
from jsonpath import jsonpath
from loguru import logger

@pytest.fixture()
def login_fixture():
    """写登录请求方法"""
    url = "http://shop.lemonban.com:8107/login"
    param = {"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType": 0}
    response = requests.request(method="post", url=url, json=param)
    access_token = jsonpath(response.json(), '$..access_token')[0]
    token_type = jsonpath(response.json(), '$..token_type')[0]  # bearer
    token = token_type+access_token
    logger.info(f"登录的返回的token：{token}")
    yield token  # 返回值token
