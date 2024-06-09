"""
日志加上方便定位排查问题：
- 参考Jmeter工具，查看结果树里： 请求消息是什么  请求头  响应消息？？== 定位排查问题的时候查看的信息 记录日志
"""

import json

import allure
import requests
from tools.handle_path import file_path
from loguru import logger
from tools.handle_extract import extract_response
from tools.handle_replace import replace_mark
from tools.handle_presql import pre_sql
@allure.step("发送接口请求操作")
def requests_api(case,token=None): #因为有些接口没有token 所以给token设置一个默认值
    method = case["请求方法"]
    url = case["接口地址"]
    header = case["请求头"]
    params = case["请求参数"]
    presql = case["前置SQL"]
    # 前置sql执行之前 替换前置sql的占位符
    presql = replace_mark(presql)  # 替换presql的占位符
    # 替换头部和参数之前执行前置sql 把结果存到环境变量里 才能后续替换成功
    pre_sql(presql)

    # 在接口请求之前，一定要在反序列转化为字典之前 调用替换函数 完成参数和头部的替换
    header = replace_mark(header)  # 完成头部的替换 得到新的头部
    params = replace_mark(params) # 完成参数的替换 得到新的参数
    url = replace_mark(url) # 完成url地址的替换 得到新的url地址

    # 发送接口请求之前，头部和参数是json串，需要做反序列操作转化为字典
    # 因为有些用例没有头部和参数，没有的话就是None，我们先判空 否则反序列化的时候会报错
    if header is not None:
        header = json.loads(header)
        if token is not None:
            header["Authorization"] = token  #如果token 有传参进来，那么就增加或者更新这个Authorization键值对
    if params is not None:
        params = json.loads(params)
    # 发送接口请求：请求方法有 get post put 等 全部覆盖，所以不同判断分支发送不同方法的请求
    # 接口请求的四大要素记录日志
    logger.info("-----------------------------------请求消息--------------------------------")
    logger.info(f"请求方法是：{method}")
    logger.info(f"请求地址是：{url}")
    logger.info(f"请求头部是：{header}")
    logger.info(f"请求参数是：{params}")
    resp = None  # 设置一个初始值
    if method.lower() == "get":
        resp = requests.request(method,url,params=params,headers=header)
    elif method.lower() == "post":
        # post方法参数的格式有json data files不同的关键字接受 分三种不同的情况处理：
        # header = {"Content-Type":"application/json"}
        if header["Content-Type"] == "application/json":
            resp = requests.request(method, url, json=params, headers=header)
        if header["Content-Type"] == "application/x-www-form-urlencoded":
            resp = requests.request(method, url, data=params, headers=header)
        if header["Content-Type"] == "multipart/form-data":
            # 因为上传接口不能带这个Content-Type头部 会报错
            header.pop("Content-Type")
            # 文件参数对象：  file_param = {"file":open("code.png","rb")}
            # excel读取出来的参数：params = {"filename":"code.png"}
            filename = params["filename"]
            # 文件名字 = 文件路径+excel里文件名字
            file_param = {"file":open(file_path/filename,"rb")}
            logger.info(f"文件上传的文件对象参数：{file_param}")
            logger.info(f"文件上传的最终请求头：{header}")
            resp = requests.request(method, url, files=file_param, headers=header)
    elif method.lower() == "put":
        resp = requests.request(method,url,json=params,headers=header)
    # 响应消息的日记记录
    logger.info("---------------------------------响应消息----------------------------------------")
    logger.info(f"接口响应状态码：{resp.status_code}")
    logger.info(f"接口响应正文：{resp.text}")

    # 得到响应消息之后去提取数据 --调用提取的函数 ,把提取的数据设置到环境变量里。
    extract_response(resp,case["提取响应字段"])

    # 把接口的响应消息对象返回
    return resp
