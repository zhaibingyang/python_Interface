import json

import allure
from jsonpath import jsonpath
from loguru import logger
from data.envi_data import EnviData
@allure.step("数据提取操作")
def extract_response(response,extract_data):
    if extract_data is None:
        logger.info("没有要从响应结果里提取的数据！")
        return
    extract_data = json.loads(extract_data)
    logger.info(f"提取的响应结果的表达式是：{extract_data}")
    for k,v in extract_data.items():  #k变量名/属性名， v是text，之前v是json表达式【$..】
        if v.startswith("$"):
            value = jsonpath(response.json(),v)[0]
            setattr(EnviData,k,value)
        elif v == "text":
            value = response.text  # 直接获取文本
            setattr(EnviData, k, value)
    logger.info(f"提取并设置环境变量后的类属性为：{EnviData.__dict__}")

