from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from wtforms import Form, TextAreaField, validators, StringField, SubmitField

import sqlite3
from flask import g
from werkzeug.utils import secure_filename

from flask import send_from_directory 

def show_files(username):
    return (os.listdir(path='F:\\File-sharing-site\\files'+username))
       
app = Flask(__name__)
app.secret_key = "OpenClassRoom" # Moved here

UPLOAD_FOLDER = "F:\\File-sharing-site\\uploads"

def get_user():
    lst=[]
    conn=sqlite3.connect("base.db")
    c=conn.cursor()
    for row in c.execute('SELECT * FROM data'):
        lst.append(row[0])
    conn.commit()
    return lst
l=get_user()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/',methods=['POST'])
def reg():
    return validate()

@app.route('/home',methods=['POST'])
def do_login():
    conn=sqlite3.connect("base.db")
    c=conn.cursor()
    error1=None
    session['username'] = request.form['username']
    password=request.form['password']
    for row in c.execute('SELECT * FROM data'):
        if row[0]== session['username'] and row[1]==password :
            error2="Welcome, "+ session['username']+"!"
            return render_template('home.html',error2=error2)
        elif row[0]!= session['username'] or row[1]!=password:
            error1="Wrong username or password!Please, try again."
            
        conn.commit()
    return render_template('login.html',error1=error1)

@app.route('/home',methods=['GET'])
def home_page():
    error2="Welcome, "+ session['username']+"!"
    return render_template('home.html',error2=error2)

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template('register.html')

def add_value(username,password,folder_password):
    conn=sqlite3.connect("base.db")
    c=conn.cursor()
    data1=[(username,password,folder_password)]
    c.executemany("INSERT INTO data VALUES (?,?,?)", data1)
    conn.commit()

def validate():
    error1=None
    error=None 
    user=request.form['user']
    password=request.form['pass']
    repeat_password=request.form['repeat_password']
    
    if user!="" and password!="" and repeat_password!="":
        if user in l:
            error= "This username is already used. Please, enter other username!"
        elif user not in l and (password!=repeat_password or len(password)<6):
            error="The password aren`t same or password is to short!"        
        else:
            add_value(user,password,None)
            path=r'F:\\File-sharing-site\\files'
            os.mkdir(path+user)
            error1="You are successfully registered :)"
            return render_template('login.html',error1=error1)
    else:
        error="The fields cannot be empty!"
    return render_template('register.html',error=error)
    
@app.route("/logout",methods=['POST'])
def logout():
    session.pop('users name')
    session.pop('username', None)
    return home()

@app.route("/home/directory",methods=['POST'])
def directory():
    files=show_files(session.get('username', None))
    return render_template("directory.html",files=files)
    
@app.route("/back",methods=['POST'])
def back():
    return redirect("http://127.0.0.1:5000/home",code=302)

    
@app.route("/delete",methods=['GET','POST'])

def delete():
    if request.method=='GET':
        lst=show_files(session.get('username'))
        return render_template("delete.html",lst=lst)
         
    elif request.method=='POST': 
        choose=str(request.form.get('choose'))
        print(choose)
        os.remove(path='F:\File-sharing-site\\files'+session.get('username', None)+'\\'+(choose))
        return redirect("http://127.0.0.1:5000/home",code=302)
        
@app.route("/remove",methods=['POST'])
def remove():
    os.remove(path='C:\\Users\\Дмитро\\Desktop\\project\\files\\'+session.get('username', None)+'\\'+(choose))
    return redirect("http://127.0.0.1:5000/home",code=302)
    
@app.route("/change",methods=['GET','POST'])
def change():
    if request.method == 'GET':
        return render_template("change.html")
    elif request.method == 'POST':
        conn=sqlite3.connect("base.db")
        c=conn.cursor()
        if request.form['new password']==request.form['repeat password']:
            c.execute("UPDATE data SET folder_password = ? WHERE username = ?", [request.form['new password'], session.get('username', None)])
            error1="Password refreshed successfully!"
        else:
            error1="Passwords aren`t same!"
        conn.commit()
    return render_template("change.html",error1=error1)
    
@app.route("/upload",methods=['GET','POST'])
def upload_file():
   return render_template('upload.html')
   
@app.route('/uploader', methods = ['GET', 'POST'])
def uploadd_file():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            flash("You must be logged in to upload files.", "error")
            return redirect(url_for('home')) # Assuming 'home' is your login page route

        if 'file' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(request.url) 

        f = request.files['file']
        if f.filename == '':
            flash('No selected file.', 'error')
            return redirect(request.url)

        if f:
            try:
                # Construct the user-specific upload directory path
                user_upload_dir = os.path.join(UPLOAD_FOLDER, username)
                
                # Create the directory if it doesn't exist
                os.makedirs(user_upload_dir, exist_ok=True)
                
                filename = secure_filename(f.filename)
                save_path = os.path.join(user_upload_dir, filename)
                
                f.save(save_path)
                flash(f"File '{filename}' uploaded successfully!", "success")
                return redirect(url_for('directory')) # Redirect to a page showing files
            except Exception as e:
                # Log the exception for debugging
                app.logger.error(f"File upload failed for user {username}: {e}")
                flash(f"An error occurred during file upload. Please try again.", "error")
                return redirect(url_for('upload_file')) # Redirect back to upload form
    # For GET request, or if POST conditions not met without specific error
    return render_template('upload.html') # Or redirect to where the upload form is
      
@app.route('/download', methods = ['GET', 'POST'])
def download():
    if request.method=='GET':
        return render_template("download.html")
    elif request.method=='POST':
        conn=sqlite3.connect("base.db")
        c=conn.cursor()
        for row in c.execute('SELECT * FROM data'):
            if request.form['users name']==row[0] and request.form['folder password']==row[2]:
                session['users name']=request.form['users name']
                spisok=show_files(request.form['users name'])
                return render_template("downloading.html",spisok=spisok)
            elif request.form['users name']!=row[0] or request.form['folder password']!=row[2]:
                error1="Invalid data!"
            
        return render_template("download.html",error1=error1) 
        
@app.route('/downloading',methods=['POST'])
def downloading():
    filename=request.form.get('todownload')
    return send_from_directory(UPLOAD_FOLDER+session.get('users name',None), filename)     
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
