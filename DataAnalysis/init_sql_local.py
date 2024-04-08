import os
import sys
import sqlite3
sys.path.append(r"..")
sys.path.append(r".") 

class local_sql_controller:
    def __init__(self):
        self.db = ""

    # 初始化本地数据库连接
    def init_db_info(self):
        try:
            if not os.path.exists("db"):
                os.makedirs("db")
            self.db = sqlite3.connect("db"+ os.sep +"params.db")
            self.exec_sql_one("""CREATE TABLE IF NOT EXISTS params (
                                    Seq int(11) PRIMARY KEY,
                                    UAcount int(11),
                                    Source text  NOT NULL,
                                    Destination text  NOT NULL,
                                    Request mediumtext  NOT NULL,
                                    mimetype varchar(10)  NOT NULL,
                                    type varchar(10)  NOT NULL,
                                    status varchar(3) NOT NULL,
                                    header text  NOT NULL,
                                    Params_get mediumtext  NOT NULL,
                                    Params_post mediumtext  NOT NULL,
                                    Cookies mediumtext  NOT NULL,
                                    Response mediumtext  NOT NULL
                                    ) """)
        except Exception as e:
            print(e)
            return False

        return True

    def exec_sql_(self,sql,values):
        cursor = self.db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql,values)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.db.rollback()
        if 'SELECT' in sql:
            results = cursor.fetchall()
            return results

    def exec_sql_one(self,sql):
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

def local_exec_sql(sql,values):
    sql_c = local_sql_controller()
    sql_c.init_db_info()
    return sql_c.exec_sql_(sql,values)

def local_exec_sql_one(sql):
    sql_c = local_sql_controller()
    sql_c.init_db_info()
    return sql_c.exec_sql_one(sql)

if __name__ == "__main__":
    print(local_exec_sql_one("SELECT Source FROM params WHERE UAcount=7"))
