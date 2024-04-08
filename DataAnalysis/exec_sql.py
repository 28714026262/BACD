import sys
import os
sys.path.append(r"..")
sys.path.append(r".")
import pymysql

class sql_controller:
    def __init__(self):
        self.db_info = {
            "host": "",
            "user_name": "",
            "password": "",
            "name": ""
        }
        self.db = ""

    def DataBaseInit(self):
        sql_database_create_http_analysis = "CREATE DATABASE IF NOT EXISTS HTTPAnalysis"
        sql_table_create_meta = """CREATE TABLE IF NOT EXISTS meta (
                                    ) """
        sql_table_create_full_req = """CREATE TABLE IF NOT EXISTS full_req (
                                    ) """
        sql_table_create_full_resp = """CREATE TABLE IF NOT EXISTS full_resp (
                                    ) """
        sql_table_create_web_if = """CREATE TABLE IF NOT EXISTS web_if (
                                    ) """
        sql_table_create_resp_structure = """CREATE TABLE IF NOT EXISTS resp_structure (
                                    ) """
        sql_table_create_req_param = """CREATE TABLE IF NOT EXISTS req_param (
                                    ) """
        sql_table_create_privacy_info = """CREATE TABLE IF NOT EXISTS privacy_info (
                                    ) """

    # after setting, controller will try to connect again
    def set_db_info(self, db_info: dict):
        self.db_info["host"] = db_info["host"]
        self.db_info["user_name"] = db_info["user_name"]
        self.db_info["password"] = db_info["password"]
        self.db_info["name"] = db_info["name"]
        try:
            self.db = pymysql.connect(host=self.db_info["host"],
                                      user=self.db_info["user_name"],
                                      password=self.db_info["password"],
                                      database=self.db_info["name"])
        except Exception as e:
            print(e)
            return False

        return True

    def connect_again(self):
        try:
            self.db = pymysql.connect(host=self.db_info["host"],
                                      user=self.db_info["user_name"],
                                      password=self.db_info["password"],
                                      database=self.db_info["name"])
        except Exception as e:
            print(e)
            return False

        return True

    def exec_sql_(self,sql):
        cursor = self.db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.db.rollback()
        if 'SELECT' in sql:
            results = cursor.fetchall()
            return results

def exec_sql(sql):
    sql_c = sql_controller()
    # input_dict = {
    #     "host": CONFIG_DICT["host"],
    #     "user_name": CONFIG_DICT["db_user"],
    #     "password": CONFIG_DICT["db_password"],
    #     "name": CONFIG_DICT["database"]
    input_dict = {
        "host": "",
        "user_name": "",
        "password": "",
        "name": ""
    }
    sql_c.set_db_info(input_dict)
    return sql_c.exec_sql_(sql) 

if __name__ == "__main__":
    sql_c = sql_controller()
    input_dict = {
        "host": "localhost",
        "user_name": "root",
        "password": "123456",
        "name": "logic_vul_det"
    }
    print(sql_c.set_db_info(input_dict))