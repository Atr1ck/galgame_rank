import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    connection = mysql.connector.connect(
        user="atr1ck",
        password="884621809",
        host="localhost",
        database="galgame",
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci'
    )
    if connection.is_connected():
        print("成功连接到 MariaDB 数据库")                      

        # 创建游标对象
        cursor = connection.cursor()

        # 执行 SQL 查询
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("你连接的数据库是: ", record)

        # 删除表
        cursor.execute("DROP TABLE IF EXISTS galgame")
        print("已删除数据表")
        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS galgame(
                id INT AUTO_INCREMENT PRIMARY KEY,  
                game_name VARCHAR(255) NOT NULL,
                game_link VARCHAR(255),
                img_link VARCHAR(255),
                brand_name VARCHAR(255),
                brand_link VARCHAR(255),
                medium_value INT,
                average_value FLOAT,
                standard_deviation INT,
                comments INT
              );
        """)
        print("表创建成功")

        # 插入数据
        games = pd.read_csv("games_info.csv")
        # 顺便转换成excel文件
        games.to_excel('games_info.xlsx', index=False)
        games = games.where(pd.notnull(games), None)
        for row in games.itertuples():
            cursor.execute('''INSERT INTO galgame (game_name, game_link, img_link, brand_name, brand_link, medium_value, average_value, standard_deviation, comments) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (row.游戏名称, row.批评空间链接, row.图片链接, row.会社, row.游戏官网, row.中央值, row.平均值, row.标准偏差, row.评论数))
        connection.commit()
        print("数据插入成功")

        # 查询数据
        cursor.execute("SELECT * FROM galgame;")
        rows = cursor.fetchall()
        print("查询结果:")
        for row in rows:
            print(row)

        # 更新数据
        #cursor.execute("UPDATE galgame SET gamename = %s WHERE name = %s", ("秽翼的尤斯蒂娅", "穢翼のユースティア"))
        #connection.commit()
        #print("数据更新成功")

        # 删除数据
        #cursor.execute("DELETE FROM galgame WHERE name = %s", ("秽翼的尤斯蒂娅",))
        #connection.commit()
        #print("数据删除成功")

except Error as e:
    print(f"数据库连接或操作失败: {e}")

finally:
    # 关闭数据库连接
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("数据库连接已关闭")