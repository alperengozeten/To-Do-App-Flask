
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
  
mysql = MySQL(app)  

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'
  
        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)

@app.route('/tasks', methods =['GET', 'POST'])
def tasks():
    if not session['loggedin']:
        return redirect(url_for('login'))
    result = None
    userid = session['userid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM TaskType')
    task_types = cursor.fetchall()
    
    if request.method == 'POST' and 'task_id' in request.form:
        taskid = int(request.form['task_id'])
        cursor.execute('DELETE FROM Task WHERE id = % s', (taskid, ))
        mysql.connection.commit()
    
    if request.method == 'POST' and 'finish_task_id' in request.form:
        taskid = int(request.form['finish_task_id'])
        cursor.execute('UPDATE Task SET status = \'Done\', done_time = % s WHERE id = % s', (datetime.now(), taskid,  ))
        mysql.connection.commit()

    if request.method == 'POST' and 'create_task_title' in request.form:
        title = request.form['create_task_title']
        description = request.form['create_task_description']
        type = request.form['task_type_input']
        deadline = request.form['create_deadline_date']
        cursor.execute('INSERT INTO Task(title, description, status, deadline, creation_time, done_time, user_id, task_type) VALUES (% s, % s, \'Todo\', % s, % s, NULL, % s, % s)', (title, description, deadline, datetime.now(), userid, type, ))
        mysql.connection.commit()
    
    if request.method == 'POST' and 'edit_task_title' in request.form:
        taskid = int(request.form['edit_task_id'])
        title = request.form['edit_task_title']
        description = request.form['edit_task_description']
        type = request.form['edit_type_input']
        deadline = request.form['edit_deadline_date']
        cursor.execute('UPDATE Task SET title = % s, description = % s, deadline = % s, task_type = % s WHERE id = % s', (title, description, deadline, type, taskid, ))
        mysql.connection.commit()
    
    cursor.execute('SELECT * FROM Task WHERE user_id = % s AND status = \'Todo\' ORDER BY deadline', (userid, ))
    result = cursor.fetchall()

    cursor.execute('SELECT * FROM Task WHERE user_id = % s AND status = \'Done\' ORDER BY deadline', (userid, ))
    completedTasks = cursor.fetchall()

    return render_template('tasks.html', table=result, task_types=task_types, completedTasks=completedTasks)

@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    if not session['loggedin']:
        return redirect(url_for('login'))
    return render_template('analysis.html')

@app.route("/logout")
def logout():
    session["username"] = None
    session['loggedin'] = False
    session['userid'] = None
    session['email'] = None
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
