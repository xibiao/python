import pymysql
from flask import Flask, request, render_template


class User(object):
    def __init__(self, id, username, password, mobile):
        self.id = id
        self.username = username
        self.password = password
        self.mobile = mobile


def connect():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root123', db='mytest_python',
                           charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()


def insert(username, password, mobile):
    conn, cursor = connect()
    sql = "insert into t_python_django_user(username,password,mobile) values(%s,%s,%s)"
    # val = (username, password, mobile)
    val = [username, password, mobile]
    # sql = "insert into t_python_django_user(username,password,mobile) values(%(n1)s,%(n2)s,%(n3)s)"
    # val = {"n1": username, "n2": password, "n3": mobile}
    print(sql, val)
    cursor.execute(sql, val)
    conn.commit()
    close(conn, cursor)


def queryById(id):
    conn, cursor = connect()
    sql = "select * from t_python_django_user where id = %s"
    val = (id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    print(result)
    close(conn, cursor)
    return result

def queryBatchById(ids):
    conn, cursor = connect()
    param = ','.join(['%s'] * len(ids))
    sql = f"select * from t_python_django_user where id in ({param})"
    print(sql)
    cursor.execute(sql, ids)
    result = cursor.fetchall()
    print(result)
    close(conn, cursor)
    return result

def queryAll():
    conn, cursor = connect()
    sql = "select * from t_python_django_user"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    close(conn, cursor)
    return result


def updateById(id, password):
    conn, cursor = connect()
    sql = "update t_python_django_user set password = %s where id = %s"
    val = [password, id]
    cursor.execute(sql, val)
    conn.commit()
    close(conn, cursor)


def deleteById(id):
    conn, cursor = connect()
    sql = "delete from t_python_django_user where id = %s"
    val = [id]
    cursor.execute(sql, val)
    conn.commit()
    close(conn, cursor)



def operate_db():
    """
    # 测试新增数据
    lists = [
        {"username": "admin", "password": "123456", "mobile": "123456780"},
        {"username": "super", "password": "111111", "mobile": "987654321"},
        {"username": "test", "password": "222222", "mobile": "543216789"}
    ]
    for dic in lists:
        insert(dic["username"], dic["password"], dic["mobile"])
    """

    # 测试查询数据
    # queryById(1)
    # queryBatchById([1, 2, 3])
    # queryAll()

    """
    # 测试修改数据
    print("修改之前：")
    queryById(1)
    updateById(1, '666666')
    print("修改之后：")
    queryById(1)
    updateById(1, '123456')
    """

    # 测试删除数据
    # deleteById(3)


app = Flask(__name__)


@app.route('/add/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template("add_query_user.html")
    else:
        form = request.form
        username = form.get('username')
        password = form.get('password')
        mobile = form.get('mobile')
        print("username:",username,", password:",password,", mobile:",mobile)
        insert(username, password, mobile)
        return render_template("add_query_user.html")


@app.route('/query/user', methods=['GET'])
def query_user():
    users = queryAll()
    print("查询结果：", users)
    """
    # 在add_query_user.html中使用Flask从users中获取数据时，若使用{{ user.id }}格式，
    # 则必须将查询结果转成字典列表，因为查询结果是元组格式，元组只能通过下标获取，例如user[0]、user[1]
    raw_users = queryAll()
    # 将元组数据转为字典列表
    users = []
    for user in raw_users:
        users.append({
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'mobile': user[3]
        })
    """
    return render_template("add_query_user.html", users=users)


if __name__ == '__main__':
    # operate_db()
    app.run(debug=True)
