"""
replace方法只能替换 变量-->环境变量的值 ，不能处理函数
- 如果占位符是函数的话 需要去执行占位符里的函数的

"""

import re

import allure
from loguru import logger
from data.envi_data import EnviData
from tools.handle_gendata import GenData
@allure.step("数据替换操作")
def replace_mark(str_data):
    # 判空处理
    if str_data is None:
        logger.info("数据为空，不需要做替换操作！")
        return
    result = re.findall("#(.*?)#",str_data)
    if result: # 如果是空列表 下面的代码不会执行了  不是空的 也就是意味着有占位符要替换 那么就执行替换操作
        logger.info("============================开始替换数据===============================")
        logger.info(f"原始字符串是：{str_data}")
        logger.info(f"要替换的占位符有：{result}")
        for mark in result: # for循环遍历列表里的占位符变量名
            # 判断mark是函数还是变量？ --怎么判断是函数-有括号就是函数
            if mark.endswith("()"): # 占位符里面就是函数 -gen_unregister_phone() -字符串类型
                gen_data = eval(f'GenData().{mark}')  # eval执行引号里的函数的调用
                # 把生成的数据存到环境变量里 -- 属性名用函数名
                fun_name = mark.strip("()") #去掉括号 得到属性名
                setattr(EnviData,fun_name,gen_data)  #存环境变量 属性名 属性值
                logger.info(f"环境变量的数据为：{EnviData.__dict__}")
                # 本身数据替换占位符 == 拿上面自己生成的数据替换占位符位置- {"mobile":"#gen_unregister_phone()#"}
                str_data = str_data.replace(f"#{mark}#",str(gen_data))   # 自己生成的手机号码替换占位符--数字转化为字符串
            else:
                # 判断一下环境变量里是否有这个属性名 如果有 就替换
                if hasattr(EnviData,mark):
                    str_data = str_data.replace(f"#{mark}#",str(getattr(EnviData,mark))) # replace 生成新的字符串，要存变量得到新字符串
                    # replace方法替换两个参数都必须是字符串 所以要转化类型-str()
    else:
        logger.info(f"要替换的占位符为空：{result},不需要做替换！")
    logger.info(f"替换完成之后的字符串是：{str_data}")
    return str_data


if __name__ == '__main__':
    str_data = '{"mobile":"#gen_unregister_phone()#"}'
    print(replace_mark(str_data))
