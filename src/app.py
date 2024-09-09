import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, jsonify, request, redirect

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user="atr1ck",
            password="884621809",
            host="localhost",
            database="erogames",
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

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM galgame LIMIT {limit} OFFSET {offset}")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) as count FROM galgame")
    total_count = cursor.fetchone()['count']
    cursor.close()
    connection.close()
    
    return jsonify({
        'data': rows,
        'total_count': total_count,
        'page': page,
        'total_pages': (total_count + limit - 1) // limit  # 计算总页数
    })

@app.route('/')
def index():
    return render_template('index.html')  # 返回HTML页面

# 添加数据到数据库
@app.route('/add')
def add_data_page():
    return render_template('add.html') #返回添加数据页面

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

    connection = get_db_connection
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