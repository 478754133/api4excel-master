#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: 赫本
# 业务包：通用函数


from prettytable import PrettyTable

import constants as cs
import core.excel as excel
import core.log as log
import core.mysql as mysql
import core.request as request

logging = log.get_logger()


class ApiTest:
    """接口测试业务类"""
    filename = cs.FILE_NAME

    def __init__(self):
        pass

    def prepare_data(self, host, user, password, db, sql):
        """数据准备，添加测试数据"""
        mysql.connect(host, user, password, db)
        res = mysql.execute(sql)
        mysql.close()
        logging.info("Run sql: the row number affected is %s", res)
        return res

    def get_excel_sheet(self, path, module):
        """依据模块名获取sheet"""
        excel.open_excel(path)
        return excel.get_sheet(module)

    def get_prepare_sql(self, sheet):
        """获取预执行SQL"""
        return excel.get_content(sheet, cs.SQL_ROW, cs.SQL_COL)

    def run_test(self, sheet, url):
        """再执行测试用例"""
        rows = excel.get_rows(sheet)
        fail = 0
        for i in range(2, rows):
            testNumber = str(excel.get_content(sheet, i, cs.CASE_NUMBER))
            testData = excel.get_content(sheet, i, cs.CASE_DATA)
            testName = excel.get_content(sheet, i, cs.CASE_NAME)
            testUrl = excel.get_content(sheet, i, cs.CASE_URL)
            testUrl = url + testUrl
            testMethod = excel.get_content(sheet, i, cs.CASE_METHOD)
            testHeaders = eval(excel.get_content(sheet, i, cs.CASE_HEADERS))
            testCode = excel.get_content(sheet, i, cs.CASE_CODE)
            actualCode = str(request.api(testMethod, testUrl, testData, testHeaders))
            expectCode = str(int(testCode))
            failResults = PrettyTable(["Number", "Method", "Url", "Data", "ActualCode", "ExpectCode"])
            failResults.align["Number"] = "l"
            failResults.padding_width = 1
            failResults.add_row([testNumber, testMethod, testUrl, testData, actualCode, expectCode])

            if actualCode != expectCode:
                logging.info("失败用例名称 %s", testName)

                print(failResults)
                fail += 1
            else:
                logging.info("用例编号: %s", testNumber)
                logging.info("用例名称 %s", testName)
                logging.info("返回状态码：%s PASS",actualCode)
                logging.info("------------------")
        if fail > 0:
            return False
        return True
