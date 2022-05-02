

def setup_db(app):

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'pande'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def cursor(mysql):
    return mysql.connection.cursor()

def getUserInfo(mysql,username):
    cur = cursor(mysql)
    cur.execute("SELECT * FROM users WHERE username=%s",(username,))
    result = cur.fetchall()
    cur.close()
    return result

def addUser(mysql,username,hash):
    cur = cursor(mysql)
    cur.execute("INSERT INTO users VALUES(NULL,%s,%s)",(username,hash,))    
    mysql.connection.commit()
    cur.close()
    return "OK"