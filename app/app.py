
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
    message = ''

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
        if not title or not description or not type or not deadline:
            message = 'Please fill in all the required details!'
        else:
            cursor.execute('INSERT INTO Task(title, description, status, deadline, creation_time, done_time, user_id, task_type) VALUES (% s, % s, \'Todo\', % s, % s, NULL, % s, % s)', (title, description, deadline, datetime.now(), userid, type, ))
            mysql.connection.commit()
    
    if request.method == 'POST' and 'edit_task_title' in request.form:
        taskid = int(request.form['edit_task_id'])
        title = request.form['edit_task_title']
        description = request.form['edit_task_description']
        type = request.form['edit_type_input']
        deadline = request.form['edit_deadline_date']
        if not title or not description or not type or not deadline:
            message = 'Please fill in all the required details!'
        else:
            cursor.execute('UPDATE Task SET title = % s, description = % s, deadline = % s, task_type = % s WHERE id = % s', (title, description, deadline, type, taskid, ))
            mysql.connection.commit()
    
    cursor.execute('SELECT * FROM Task WHERE user_id = % s AND status = \'Todo\' ORDER BY deadline', (userid, ))
    result = cursor.fetchall()

    cursor.execute('SELECT * FROM Task WHERE user_id = % s AND status = \'Done\' ORDER BY deadline', (userid, ))
    completedTasks = cursor.fetchall()

    return render_template('tasks.html', table=result, task_types=task_types, completedTasks=completedTasks, message=message)

@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    if not session['loggedin']:
        return redirect(url_for('login'))
    
    averageTime = None
    lateTasks = None
    nonCompletedTasks = None
    mostTimeTasks = None
    typeTaskCounts = None
    userid = int(session['userid'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    analysisType = None

    if request.method == 'POST' and 'analysis_type' in request.form:
        analysisType = request.form['analysis_type']
        if request.form['analysis_type'] == "Average Task Completion":
            cursor.execute('SELECT HOUR(SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(done_time, creation_time))))) DIV 24 as avg_day, HOUR(SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(done_time, creation_time))))) MOD 24 as avg_hour, MINUTE(SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(done_time, creation_time))))) as avg_minute FROM Task WHERE user_id = % s AND status=\'Done\'', (userid, ))
            averageTime = cursor.fetchall()
        if request.form['analysis_type'] == "Tasks Completed After The Deadline":
            cursor.execute('SELECT title, HOUR(TIMEDIFF(done_time, deadline)) DIV 24 as day, HOUR(TIMEDIFF(done_time, deadline)) MOD 24 as hour_diff, MINUTE(TIMEDIFF(done_time, deadline)) as minute_diff FROM Task WHERE user_id = % s AND done_time > deadline', (userid, ))
            #cursor.execute('WITH difference_in_seconds AS (SELECT title, TIMESTAMPDIFF(SECOND, creation_time, done_time) AS seconds FROM Task WHERE user_id = % s), differences AS (SELECT title, MOD(seconds, 60) AS seconds_part, MOD(seconds, 3600) AS minutes_part, MOD(seconds, 3600 * 24) AS hours_part FROM difference_in_seconds) SELECT title, CONCAT(FLOOR(seconds / 3600 / 24), \' days \', FLOOR(hours_part / 3600), \' hours \', FLOOR(minutes_part / 60), \' minutes \', seconds_part, \' seconds\') AS difference FROM differences;', (userid, ))
            lateTasks = cursor.fetchall()

        if request.form['analysis_type'] == "Uncompleted Tasks Sorted By Deadline":
            cursor.execute('SELECT * FROM Task WHERE user_id = % s AND status = \'Todo\' ORDER BY deadline', (userid, ))
            nonCompletedTasks = cursor.fetchall()


        if request.form['analysis_type'] == "Most Time Consuming Two Tasks":
            cursor.execute('SELECT title, TIMEDIFF(done_time, creation_time) as task_time FROM Task WHERE user_id = % s ORDER BY task_time DESC LIMIT 2', (userid, ))
            mostTimeTasks = cursor.fetchall()
        
        if request.form['analysis_type'] == "Number Of Tasks Completed For Each Task Type":
            cursor.execute('SELECT Y.type as type, COUNT(*) as task_count FROM Task T, TaskType Y WHERE T.user_id = % s AND status = \'Done\' AND T.task_type = Y.type GROUP BY Y.type', (userid, ))
            typeTaskCounts = cursor.fetchall()
    
    return render_template('analysis.html', analysisType=analysisType, lateTasks=lateTasks, nonCompletedTasks=nonCompletedTasks, typeTaskCounts=typeTaskCounts, averageTime=averageTime, mostTimeTasks=mostTimeTasks)

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
