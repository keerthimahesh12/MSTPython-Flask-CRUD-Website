from flask import Flask, render_template, request, session
import mysql.connector
import secrets

conn=mysql.connector.connect(host='localhost',user='root',password='root',database='tms')
mycursor=conn.cursor()

# create the flask application

app=Flask(__name__)

app.secret_key = secrets.token_hex(16)  


global_user_id = None

# define root and corresponding view

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/welcome', methods=['POST'])
def welcome():

    global global_user_id
    username=request.form['username']
    pwd=request.form['password']

    query = "SELECT * FROM users WHERE username LIKE %s AND password LIKE %s"
    mycursor.execute(query, (username, pwd))
    data = mycursor.fetchone()
    if data:
        global_user_id=data[0]

        return render_template('welcome.html',user=username)
    else:
        return render_template('login.html', msg='Invalid Username/Password')
    

@app.route('/viewalltasks', methods=['GET','POST'])
def viewalltasks():
    global global_user_id

    if global_user_id:

        if request.method == 'POST':
            return render_template('welcome.html', user="Back!!")

        category_filter = request.args.get('category')
        if category_filter:
            tasks_query = "SELECT * FROM tasks WHERE user_id = %s AND category = %s"
            mycursor.execute(tasks_query, (global_user_id, category_filter))
        else:
            tasks_query = "SELECT * FROM tasks WHERE user_id = %s"
            mycursor.execute(tasks_query, (global_user_id,))

        tasks_data = mycursor.fetchall()

        return render_template('viewalltasks.html', sqldata=tasks_data)
    else:
        return render_template('login.html', msg='No data')
    


@app.route('/addtask', methods=['POST','GET'])

def addtask():
    if request.method=='POST':
        
        # get data from the form
        task_id=int(request.form['task_id'])
        user_id = int(request.form['user_id'])
        title = request.form['title']
        description = request.form['description']
        category=request.form['category']
        due_date = request.form['due_date']
        status = int(request.form['status'])

        # insert task into the database
        task_query = "INSERT INTO tasks (task_id,user_id, title, description, category, due_date, status) VALUES (%s,%s, %s, %s, %s, %s, %s)"
        task_values = (task_id,user_id, title, description, category, due_date, status)

        mycursor.execute(task_query, task_values)
        conn.commit()
        return render_template('welcome.html',user='back!')
    
    else:
            return render_template('addtask.html')


@app.route('/deletetask',methods=['POST','GET'])
def deletetask():
    global global_user_id
        
    if request.method == 'POST':
        task_ids = request.form.getlist('task_ids[]')
        print("Task IDs to delete:", task_ids)
        for task_id in task_ids:
            task_id = int(task_id)
            task_query = "DELETE FROM tasks WHERE task_id=%s"
            mycursor.execute(task_query, (task_id,))
            conn.commit()
        return render_template('welcome.html', user='back!')
    else:
        tasks_query = "SELECT * FROM tasks WHERE user_id = %s"
        mycursor.execute(tasks_query, (global_user_id,))
        tasks_data = mycursor.fetchall()

        return render_template('deletetask.html', sqldata=tasks_data)


@app.route('/updatestatus', methods=['POST', 'GET'])
def updatestatus():
    
    global global_user_id

    if request.method == 'POST':
        task_ids = request.form.getlist('task_ids[]')

        if not task_ids:
            # if no tasks selected for status update
            return render_template('updatestatus.html', sqldata=[], message='No tasks selected for status update')

        try:
            # loop through the selected task IDs
            for task_id in task_ids:
                task_id = int(task_id)
                
                status = request.form.get(f'status_{task_id}')
                
                status = True if status.lower() == 'complete' else False


                status_query = "UPDATE tasks SET status = %s WHERE task_id = %s AND user_id = %s"
                mycursor.execute(status_query, (status, task_id, global_user_id))
                conn.commit()

            return render_template('welcome.html', user='Status updated successfully!')
        
        except Exception as e:
            
            return render_template('welcome.html', user='Status update unsuccessful')

    else:
        # fetch all tasks for the current user
        tasks_query = "SELECT * FROM tasks WHERE user_id = %s"
        mycursor.execute(tasks_query, (global_user_id,))
        tasks_data = mycursor.fetchall()

        return render_template('updatestatus.html', sqldata=tasks_data, message=None)

@app.route('/logout')
def logout():

    global global_user_id
    session.pop('user_id', None)
    global_user_id = None
    # redirect to the home page after logout
    return render_template('/home.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        
        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        query = "INSERT INTO users (user_id, username, password, email) VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, (user_id, username, password, email))
        conn.commit()

        return render_template('/login.html')
    else: return render_template('/register.html')

@app.route('/deleteaccount')
def deleteaccount():
    global global_user_id

    if global_user_id:
        # Delete tasks associated with the user
        delete_tasks_query = "DELETE FROM tasks WHERE user_id = %s"
        mycursor.execute(delete_tasks_query, (global_user_id,))

        # Delete the user
        delete_user_query = "DELETE FROM users WHERE user_id = %s"
        mycursor.execute(delete_user_query, (global_user_id,))

        conn.commit()
        session.clear()

        return render_template('home.html')
    else:
        return render_template('login')



# run flask application


if __name__=='__main__':
    app.run(debug=True)