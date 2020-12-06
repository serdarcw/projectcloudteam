# Import Flask modules
from flask import Flask, request, render_template, redirect
from flaskext.mysql import MySQL

# Create an object named app
app = Flask(__name__)

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = 'database-1.cuxdz3m00nkr.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ProjectGroup_1'
app.config['MYSQL_DATABASE_DB'] = 'logindb'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

def init_login_db():
    login_table = """
    CREATE TABLE IF NOT EXISTS logindb.login(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    number VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(login_table)


def insert_person(name, number):
    query = f"""
    SELECT * FROM login WHERE name='{name}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        insert = f"""
        INSERT INTO login (name, number)
        VALUES ('{name}', '{number}');
        """
        cursor.execute(insert)
        result = cursor.fetchall()
        return f'Person {name} added successfully. To connect you website, please login again with your credentials'
    
    if row[1] == name and row[2] != number:
        return f'Hi {name}.... Your username has been selected or your password is wrong. Please try again!'

    if row[2] == number and row[2] == number:
        return 'checkpoint'


def redirect_person(name, number):
    query = f"""
    SELECT * FROM login WHERE name='{name}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row[2] == {number}:
        return redirect("http://ec2-184-73-128-179.compute-1.amazonaws.com:3000", code=302)

@app.route('/', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Username can not be empty', show_result=False)
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Username should be text', show_result=False)

        number = request.form['password']
        if number is None or number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Password number can not be empty', show_result=False)
        elif not number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Password should be in numeric format', show_result=False)

        result = insert_person(name, number)
        if result != 'checkpoint':
            return render_template('add-update.html', show_result=True, result=result, not_valid=False)
        return redirect("http://ec2-184-73-128-179.compute-1.amazonaws.com:3000", code=302)

    else:
        return render_template('add-update.html', show_result=False, not_valid=False)

if __name__== '__main__':
    init_login_db()
    app.run(host='0.0.0.0', port=80) 
