from pathlib import Path

# log文件路径
log_path = Path(__file__).absolute().parent.parent / "outputs" / "logs"

# excel路径
excel_path = Path(__file__).absolute().parent.parent / "data"/ "testcase68.xlsx"

# case路径
case_path = Path(__file__).absolute().parent.parent / "data"/ "testcase_mall.xlsx"

# 上传文件路径 --因为上传的文件会变 不要写死 在测试用例里控制测试数据
file_path = Path(__file__).absolute().parent.parent / "data"

# 测试报告的路径
report_path = Path(__file__).absolute().parent.parent / "outputs" / "reports_allure"

if __name__ == '__main__':
    print(log_path)
    print(excel_path)
    print(report_path)

