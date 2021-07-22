from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/Gallery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["IMAGE_UPLOADS"] = "static/uploads"


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET']) 
def get_index():
    return render_template('index.html')

@app.route("/signout")
def signout():
    return redirect('login')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
       name = request.json.get('name')
       password = request.json.get('pass')

       user = User.query.filter_by(name=name).first()
       session['name'] = user.name
       session['password'] = user.password
       session['email'] = user.email
       session['userid'] = user.user_id

       if user.password == password:
           return redirect(url_for('get_home'))
       else:
           flash('Incorrect password', category='error')
  
    return render_template("index.html")
    

@app.route('/home', methods=['GET']) 
def get_home():
    return render_template('home.html')

@app.route('/register', methods=['GET']) 
def get_register():
    return render_template('register.html')

@app.route('/register', methods=['POST']) 
def post_register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('pass')
    cpassword = request.form.get('cpass')
   
    if password != cpassword:
        flash('Passwords don\'t match.', category='error')
    else:
        create_user(name, password, email)
        flash('Account created!', category='success')
        return redirect(url_for('login'))

    return render_template("register.html")
    
@app.route('/users', methods=['GET']) 
def get_users():
    return render_template('users.html')

@app.route('/users', methods=['DELETE']) 
def delete_users():
    delete_user(session['userid'])
    return redirect('login')

@app.route('/users', methods=['PUT']) 
def put_users():
    updated_user = update_user(session['userid'])
    return redirect('login')

@app.route('/userinfo', methods=['GET']) 
def get_userinfo():
    sid = session['userid']
    sname = session['name']
    semail = session['email']
    spassword = session['password']
    data = {'id':sid, 'name':sname, 'email':semail, 'password':spassword}
    return jsonify(data)

@app.route('/images', methods=['GET']) 
def get_image():
    #print('display_image filename: ' + filename)\
    files = os.listdir('static/uploads')
    print(files)
    data = {'images': files}
    return jsonify(data)

@app.route('/image', methods=['POST'])
def upload_image():

    if request.files:

        image = request.files["image"]
        print(image)

        if image.filename == "":
            print("No filename")
            return redirect('home')

        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
        
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            create_image(session['userid'], filename)
            print("Image saved")

            return redirect("home")

        else:
            print("That file extension is not allowed")
            return redirect('home')

    return redirect("home")


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    images = db.relationship('Image')
    def __init__(self, name, password, email):
        self.name = name
        self.email = email
        self.password = password

class Image(db.Model):
    __tablename__ = 'images'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    description = db.Column(db.String(60), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

def get_user(id):
    user = User.query.get(id)
    if user is None:
        return {'error': 'user not found'}
    return {'id': user.user_id , 
            'name': user.name, 
            'email':user.email,
            'password': user.password}

def get_user_list():
    users = User.query.all()
    user_list=[]
    for user in users:
        user_data = {'id': user.user_id, 
                    'name': user.name, 
                    'email': user.email }
        user_list.append(user_data)

    return {'users': user_list}

def create_user(name, email, password):
    user = User( name,
                 email,
                 password)
    db.session.add(user)
    db.session.commit()
    return {'message': 'user created'}

def create_image(user_id, description):
    image = Image(user_id,
                 description)
    db.session.add(image)
    db.session.commit()
    return {'message': 'user created'}


def update_user(id):
    user = User.query.get(id) #con esto no se necesita un db.update, esto retorna 
    if user is None:
        return {'error': 'user not found'}
    
    name = request.json['name']
    if name != '':
        user.name = name

    email = request.json['email']
    if email != '':
        user.email = email

    password = request.json['pass']
    if password != '':
        user.password = password
    
    db.session.commit()

    return { 'message': 'user modified', 'user': {
        'id': user.user_id,
        'name': user.name,
        'email': user.email,
        'password': user.password
    }}

def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return {'error': 'user not found'}
    db.session.delete(user)
    db.session.commit()
    return {'message': 'user deleted'}


#new_user = User(first_name="jeje",email="email", password="hh")
#db.session.add(new_user)
#db.session.commit()
#login_user(new_user, remember=True)

if __name__ == "__main__":
    app.run(debug=False)
