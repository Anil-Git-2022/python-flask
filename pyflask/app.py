from flask import Flask,flash,render_template,request,redirect,session
from flask_mysqldb import MySQL
from datetime import datetime
import bcrypt
import os
import json
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pydata'
app.config['UPLOAD_FOLDER'] = './upload'
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ""
app.config['MAIL_PASSWORD'] = ""
mail = Mail(app)
app.secret_key='asdsdfsdfs13sdf_df%&' 
db = MySQL(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     content = db.Column(db.String(255),nullable=False)
#     completed = db.Column(db.String(255),nullable=False)
#     date_created = db.Column(db.DateTime,default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':

        # UPLOAD_FOLDER = './upload'

        file1 = request.files['upload']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        msg = Message('Hello', sender = 'Anil Harjani', recipients = ['anilharjani51@gmail.com'])
        msg.body = "Test mail."
        mail.send(msg)

        name = request.form['name']
        age = request.form['age']

        cursor = db.connection.cursor()
        cursor.execute(''' INSERT INTO info_table (name,age) VALUES(%s,%s)''',(name,age))
        db.connection.commit()
        cursor.close()
        return redirect('/list')
@app.route('/list')
def getList():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM info_table")
    #db.connection.commit()
    #cursor.close()
    data = cursor.fetchall()
    return render_template('demo.html',data=data)
@app.route('/delete/<int:id>')
def delete(id):

    cursor = db.connection.cursor()
    cursor.execute("DELETE from info_table where id = %s",(str(id)))
    db.connection.commit()
    cursor.close()
    return redirect('/list')
@app.route('/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):
    if request.method == 'GET':
        cursor = db.connection.cursor()
        cursor.execute("SELECT name,age,id FROM info_table where id = %s",(str(id)))
        #db.connection.commit()
        #cursor.close()
        data = cursor.fetchone()
        return render_template('edit.html',data=data)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = db.connection.cursor()
        cursor.execute("UPDATE info_table set name = %s, age = %s where id = %s",(name,str(age),str(id)))
        db.connection.commit()
        cursor.close()
        return redirect('/list')
@app.route('/log', methods = ['POST', 'GET'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # passwd = b's$cret12'

        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(passwd, salt)

       
        cursor = db.connection.cursor()
        data = cursor.execute("SELECT * from users where username = %s ",[username])
        db.connection.commit()
        user = cursor.fetchone()
        # print(user[2])
        #cursor.close()
        if data > 0:
            
            checkpass = bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8'))
            if checkpass:
             session['name'] = request.form['username']
             flash('You have been authenticated successfully.')
             return redirect('/list')
            else: 
             return "Invalid Login Credentials"
            
        else:
            return 'User does not exsist'
@app.route('/logout', methods = ['GET'])
def logout():
    session.pop('name')
    return redirect('/list')

@app.route('/register',methods = ['POST','GET'])
def register():
   if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    bytePwd = password.encode('utf-8')
    # Generate salt
    mySalt = bcrypt.gensalt()
    # Hash password
    hash = bcrypt.hashpw(bytePwd, mySalt)
    cursor = db.connection.cursor()
    cursor.execute('''INSERT INTO users (username,password) VALUES (%s,%s)''',(username,hash))
    db.connection.commit()
    cursor.close()
    return redirect('/log')
   if request.method == 'GET':
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)