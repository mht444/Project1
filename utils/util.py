import pymysql


class Config:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '123456'
    DATABASE = 'db_travel'
    PORT = 3306

# 建立数据库连接
def conn():
    con = pymysql.connect(host=Config.HOST, port=Config.PORT,
                          user=Config.USER, password=Config.PASSWORD, db=Config.DATABASE)
    cur = con.cursor()
    return con, cur

# 关闭
def close():
    con, cur = conn()
    cur.close()
    con.close()

# 查询
def query(sql):
    con, cur = conn()
    cur.execute(sql)
    res = cur.fetchall()
    close()
    return res

# 插入、更新、删除
def insert(sql):
    con, cur = conn()
    cur.execute(sql)
    con.commit()
    close()