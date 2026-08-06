import pandas as pd
import pymysql

class Config:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '123456'
    DATABASE = 'db_travel'
    PORT = '3306'

# 连接数据库
conn = pymysql.connect(
    host=Config.HOST,
    user=Config.USER,
    password=Config.PASSWORD,
    database=Config.DATABASE
)
cursor = conn.cursor()

# 插入SQL语句
sql = """
INSERT INTO home_travelinfo(unique_id, area, name, review_count, rating, is_ad, is_recommended, city, image_url, distance_from_center, tags, 
detail_link, market_price, discount_price, discount_description, actual_price, price_type, price_type_description, is_free, longitude, latitude, popularity_score, province)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# 读取处理后的CSV
df = pd.read_csv('data_pro.csv')
# 缺失值填充
df = df.fillna('暂无')

# 批量插入数据
for index, row in df.iterrows():
    cursor.execute(sql, tuple(row))

# 提交并关闭连接
conn.commit()
cursor.close()
conn.close()