from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# 远程数据库连接配置
db_config = {
    "host": "8.138.123.42",
    "port": 23036,
    "user": "t330026038",
    "password": "123456",
    "database": "gym_0424_generate_at_0424_2257",
    "charset": "utf8mb4"
}

# 处理非JSON类型
def serialize(obj):
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode()
    if isinstance(obj, (int, float, str)):
        return obj
    if obj is None:
        return None
    return str(obj)

@app.route('/execute', methods=['POST'])
def execute_sql():
    data = request.get_json()
    sql = data.get('sql', '')

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        
        if sql.strip().lower().startswith('select'):
            rows = cursor.fetchall()
            # 将行数据里面的每个元素都进行序列化
            serialized_rows = [
                [serialize(value) for value in row]
                for row in rows
            ]
            result = {
                "status": "success",
                "data": serialized_rows
            }
        else:
            conn.commit()
            result = {
                "status": "success",
                "message": "SQL executed successfully"
            }

        cursor.close()
        conn.close()
        return jsonify(result)

    except pymysql.MySQLError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
