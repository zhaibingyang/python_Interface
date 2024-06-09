"""
入口文件：
1、pytest.main收集并执行执行所有模块的用例
2、执行完成后生成allure 测试报告
3、把日志持久化存储 -- 日志文件存储
"""
import pytest
from loguru import logger
from tools.handle_path import log_path,report_path


# 日志写入文件--持久化存储
logger.add(sink=log_path/"Mall_API.log",  #调用路径处理的变量
           encoding="utf8",
           level="INFO",
           rotation = "1 day",
           retention = 20
           )

# 收集并执行用例 并生成测试报告
pytest.main(["-v","-s",f"--alluredir={report_path}","--clean-alluredir"])