import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, jsonify, request, redirect
from pathlib import Path
from flask_cors import CORS

current_dir = Path(__file__).resolve().parent
app = Flask(__name__)
CORS(app)
def get_db_connection():
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
            return connection
        
    except Error as e:
        print(f"数据库连接或操作失败: {e}")

# 从数据库获取数据
@app.route('/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 200))
    offset = (page - 1) * limit
    query = request.args.get('query', '')
    search_by = request.args.get('searchBy', 'name')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if query == '':
        cursor.execute(f"SELECT * FROM galgame LIMIT {limit} OFFSET {offset}")
        rows = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) as count FROM galgame ")
        total_count = cursor.fetchone()['count']
    else:
        if search_by == 'name':
            cursor.execute("SELECT * FROM galgame WHERE LOWER(game_name) LIKE %s LIMIT %s OFFSET %s", (f"%{query.lower()}%", limit, offset))
            rows = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as count FROM galgame WHERE LOWER(game_name) LIKE %s", (f"%{query.lower()}%",))
            total_count = cursor.fetchone()['count']
        elif search_by == 'brand':
            cursor.execute("SELECT * FROM galgame WHERE LOWER(brand_name) LIKE %s LIMIT %s OFFSET %s", (f"%{query.lower()}%", limit, offset))
            rows = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as count FROM galgame WHERE LOWER(game_name) LIKE %s", (f"%{query.lower()}%",))
            total_count = cursor.fetchone()['count']

    cursor.close()
    connection.close()

    return jsonify({
        'data': rows,
        'total_pages': (total_count + limit - 1) // limit  # 计算总页数
    })

@app.route('/check', methods=['GET'])
def check():
   return  

@app.route('/add', methods=['POST'])
def add_data():
    game_name = request.form['Name']
    game_link = request.form['ScaLink']
    img_link = request.form['ImgLink']
    brand_name = request.form['BrName']
    brand_link = request.form['OffiWeb']
    medium_value = request.form['Medium']
    average_value = request.form['Average']
    standard_deviation = request.form['Standard']
    comments = request.form['Comments']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO galgame (game_name, game_link, img_link, brand_name, brand_link, medium_value, average_value, standard_deviation, comments) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (game_name, game_link, img_link, brand_name, brand_link, medium_value, average_value, standard_deviation, comments))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/')
    
# 删除数据库中的数据
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM galgame WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': '数据已删除'})

if __name__ == '__main__':
    app.run(debug=True)