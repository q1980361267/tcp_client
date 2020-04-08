import xlrd
def getExcel(file, sheet, column):
    """获取表格中的数据"""
    excel = xlrd.open_workbook(file)  # 获得表格实例

    # 判断sheet的数值类型
    if isinstance(sheet, int):
        table = excel.sheet_by_index(sheet)
    elif isinstance(sheet, str):
        table = excel.sheet_by_name(sheet)
    else:
        raise ("sheet值只能为int或者str型")
    cols = table.col_values(column)
    return cols