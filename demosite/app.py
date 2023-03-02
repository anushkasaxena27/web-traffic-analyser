from flask import Flask,render_template,request,redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
dbname = "demosite.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super secret key"
db = SQLAlchemy(app)
cors = CORS(app, supports_credentials=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f"{self.email} - {self.password}"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def __str__(self) -> str:
        return f"{self.name} - {self.email} - {self.phone} - {self.message}"


@app.route('/login',methods = ['GET','POST'] )
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user.password == password:
            flash("Login Successfully", "success")
            return jsonify({"message": "Login Successfully", "status": "success"})
        else:
            flash("Invalid Credentials", "error")
            return jsonify({"message": "Invalid Credentials", "status": "error"})

    return render_template('login.html')

@app.route('/signup',methods = ['GET','POST'] )
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        username = request.form['username']
        if len(email) < 4:
            
            flash("Email must be greater than 3 characters", "error")
            return jsonify({"message": "Email must be greater than 3 characters", "status": "error"})
        if len(password) < 4:
           
            flash("Password must be greater than 3 characters", "error")
            return jsonify({'message': 'Password must be greater than 3 characters', 'status': 'error'})
        if len(username) < 4:
            flash("Username must be greater than 3 characters", "error")
            return jsonify({'message': 'Username must be greater than 3 characters', 'status': 'error'})
        if password != cpassword:
            flash("Password and Confirm Password must be same", "error")
            return jsonify({'message': 'Password and Confirm Password must be same', 'status': 'error'})
        user = User.query.filter_by(email=email).first()
        if user:
            print(flash("Email already exists", "error"))
            return jsonify({'message': 'Email already exists', 'status': 'error'})
        user = User(email=email,password=password,username=username)
        db.session.add(user)
        db.session.commit()
        print("Signup Successfully")
        flash("Signup Successfully", "success")
        return jsonify({'message': 'Signup Successfully', 'status': 'success'})
    return render_template('signup.html')
 
@app.route('/')

def home():
        
        return render_template('index.html')

@app.route('/contact',methods = ['GET','POST'] )
#@cross_origin()
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        contact = Contact(name=name,email=email,phone=phone,message=message)
        db.session.add(contact)
        db.session.commit()
        print("Message Sent Successfully")
        return jsonify({'message': 'Message Sent Successfully', 'status': 'success'})
    return render_template('contact.html')



if __name__ == '__main__':
    if not os.path.exists(dbname):
        with app.app_context():
            db.create_all()
    app.run(debug=True,port=5000, host="0.0.0.0")
