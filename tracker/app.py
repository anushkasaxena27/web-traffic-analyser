from flask import Flask,render_template,redirect,request,flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
dbname = "tracker.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super secret key"
db = SQLAlchemy(app)
CORS(app, support_credentials=True)

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

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(12), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website = db.Column(db.String(200), nullable=False)
    visitor_count = db.Column(db.Integer, nullable=False, default=1)

    def __str__(self) -> str:
        return f"{self.ip} - {self.date}"

class TrackLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(12), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website = db.Column(db.String(200), nullable=False)
    login_count = db.Column(db.Integer, nullable=False, default=1)

    def __str__(self) -> str:
        return f"{self.ip} - {self.date}"

class TrackSignup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(12), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website = db.Column(db.String(200), nullable=False)
    register_count = db.Column(db.Integer, nullable=False, default=1)

    def __str__(self) -> str:
        return f"{self.ip} - {self.date}"

class TrackContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(12), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    website = db.Column(db.String(200), nullable=False)
    contact_count = db.Column(db.Integer, nullable=False, default=1)

    def __str__(self) -> str:
        return f"{self.ip} - {self.date}"

@app.route('/register',methods = ['GET','POST'] )
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        username = request.form['username']
        if len(email) < 4:
            
            flash("Email must be greater than 3 characters", "error")
            return redirect('/register')
        if len(password) < 4:
           
            flash("Password must be greater than 3 characters", "error")
            return redirect('/register')
        if len(username) < 4:
            flash("Username must be greater than 3 characters", "error")
            return redirect('/register')
        if password != cpassword:
            flash("Password and Confirm Password must be same", "error")
            return redirect('/register')
        user = User.query.filter_by(email=email).first()
        if user:
            print(flash("Email already exists", "error"))
            return redirect('/register')
        user = User(email=email,password=password,username=username)
        db.session.add(user)
        db.session.commit()
        print("Signup Successfully")
        flash("Signup Successfully", "success")
        return redirect('/login')
    return render_template('register.html')


@app.route('/login',methods = ['GET','POST'] )
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user.password == password:
            flash("Login Successfully", "success")
            return redirect('/')
        return redirect('/')

    return render_template('login.html')

@app.route('/')
def hello():
    login_data = TrackLogin.query.all()
    signup_data = TrackSignup.query.all()
    contact_data = TrackContact.query.all()
    pagevisit_data = PageVisit.query.all()
    return render_template('index.html',login_data=login_data,signup_data=signup_data,contact_data=contact_data,pagevisit_data=pagevisit_data)

@app.route('/contact',methods = ['GET','POST'] )
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
    return render_template('contact.html')


# reciever API
# recieve the ip address of the user and login submission
@app.route('/track/logins', methods = ['GET','POST'] )
@cross_origin()
def track_login():
    if request.method == 'POST':
        ip = request.form.get('ip')
        website = request.form.get('website')
        query = TrackLogin.query.filter_by(ip=ip).first()
        if query:
            query.date = datetime.utcnow()
            query.login_count += 1
            db.session.commit()
        else:
            track_login = TrackLogin(ip=ip,website=website)
            db.session.add(track_login)
            db.session.commit()
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route('/track/register', methods = ['GET','POST'] )
@cross_origin()
def track_registrations():
    if request.method == 'POST':
        ip = request.form.get('ip')
        website = request.form.get('website')
        query = TrackSignup.query.filter_by(ip=ip).first()
        if query:
            query.date = datetime.utcnow()
            query.register_count += 1
            db.session.commit()
        else:
            track_register = TrackSignup(ip=ip,website=website)
            db.session.add(track_register)
            db.session.commit()
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route('/track/contacts',methods = ['POST'])
@cross_origin()
def track_contact():
    if request.method == 'POST':
        ip = request.form.get('ip')
        website = request.form.get('website')
        query = TrackContact.query.filter_by(ip=ip).first()
        if query:
            query.date = datetime.utcnow()
            query.contact_count += 1
            db.session.commit()
        else:
            track_contact = TrackContact(ip=ip,website=website)
            db.session.add(track_contact)
            db.session.commit()
        return jsonify({'success':True})
    return jsonify({'success':False})

@app.route('/track/pagevists', methods = ['GET','POST'] )
@cross_origin()
def track_pagevists():
    if request.method == 'POST':
        ip = request.form.get('ip')
        website = request.form.get('website')
        query = TrackPageVisit.query.filter_by(ip=ip).first()
        if query:
            query.date = datetime.utcnow()
            query.page_visit_count += 1
            db.session.commit()
        else:
            track_pagevisit = TrackPageVisit(ip=ip,website=website)
            db.session.add(track_pagevisit)
            db.session.commit()
        return jsonify({'success':True})
    return jsonify({'success':False})


if __name__ == '__main__':
    if not os.path.exists(dbname):
        with app.app_context():
            db.create_all()
    app.run(debug=True,port=8000, host="0.0.0.0")