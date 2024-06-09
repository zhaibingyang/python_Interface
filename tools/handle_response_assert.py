"""
TypeError: the JSON object must be str, bytes or bytearray, not NoneType
- 原因： json反序列化的操作的时候闯进来的不是str 而是None。

有些用例可能没有断言，要处理： 判断是否要断言 ===判空处理
- 如果需要断言： expected_result不为空的
- 如果需要断言： expected_result为 None值

"""

import json

import allure
from jsonpath import jsonpath
from loguru import logger

@allure.step("数据库断言操作")
def response_assert(expected_result,response):  # response是响应消息对象
    logger.info("=============================开始断言=================================")
    # 判空处理
    if expected_result is None:
        logger.info("用例不需要做断言！")
        return  #直接返回 后面都不需要执行了。
    expected_result = json.loads(expected_result)
    logger.info(f"期望结果的表示式是：{expected_result}")
    for k,v in expected_result.items():
        if k.startswith("$"):
            actrual_result = jsonpath(response.json(),k)[0]
            logger.info(f"执行结果是：{actrual_result}")
            try:
                assert actrual_result == v
                logger.info("断言成功！")
            except AssertionError as e:
                logger.error("断言失败！")
                raise e
        elif k == "text":
            actrual_result = response.text
            logger.info(f"执行结果是：{actrual_result}")
            try:
                assert response.text == v
                logger.info("断言成功！")
            except AssertionError as e:
                logger.error("断言失败！")
                raise e

