"""
函数封装步骤： 任何功能代码都可以封装函数。
1、第一步：先把功能代码写出来 【逻辑】
2、第二步： def，封装函数
3、第三步：参数化，变化的数据参数化 ：不是固定，用户输入的数据，从其他地方获取数据等
4、第四步：判断是否需要返回值，return定义返回值

封装完之后 最好验证调试一下函数功能：
main里面调试
"""
import allure
from openpyxl import load_workbook
@allure.step("读取Excel表格操作")
def read_excel(file,sheet):
    wb = load_workbook(file)
    sh = wb[sheet]
    cases_all = list(sh.values)
    # 1、先得到标题行 - 列表取值 索引0
    title = cases_all[0]
    # 定义新列表 存储所有用例
    case_list = []
    # 2、for循环去遍历后面的用例数据每一行
    for case in cases_all[1:]:
        case_dict = dict(zip(title,case))
        case_list.append(case_dict)
    return case_list  # 返回所有用例的列表

if __name__ == '__main__':
    from tools.handle_path import excel_path
    print(read_excel(excel_path, "login"))
