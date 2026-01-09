from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required
from pyrfc3339 import generate
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db

pages = Blueprint('account',__name__,template_folder='templates',
    static_folder='static',)
    
#Actual Auth pages(working)  
#Actual Auth pages(working)  
@pages.route('/login')  
def login():
    return render_template('account/login.html')

@pages.route('/login',methods=['POST'])  
def login_post():
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password,password):
            flash("Invalid Credentials")
            return redirect(url_for('pages.login'))

        login_user(user, remember=remember)
        return redirect(url_for('dashboards.index'))

@pages.route('/signup')  
def signup(): 
    return render_template('account/signup.html')

@pages.route('/signup',methods=['POST'])  
def signup_post():
    email = request.form.get('email') 
    username = request.form.get('username')
    password = request.form.get('password')

    user_email = User.query.filter_by(email=email).first()
    user_username = User.query.filter_by(username=username).first()    
    
    if user_email:
        flash("User email already Exists")
        return redirect(url_for('pages.signup'))
    if user_username:    
        flash("Username already Exists")
        return redirect(url_for('pages.signup'))

    new_user = User(email=email,username=username,password=generate_password_hash(password,method="sha256"))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('pages.login'))

@pages.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.login'))