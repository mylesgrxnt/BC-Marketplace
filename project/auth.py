from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Product
from . import db
import re
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from .__init__ import create_app

load_dotenv()

def generate_token(email):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
        return email
    except Exception:
        return False



def send_email(to, subject, template):
    app = current_app
    app.config.update(dict(
    DEBUG = False,
    TESTING = False,
    CSRF_ENABLED = True,
    SECRET_KEY = os.getenv("SECRET_KEY"),
    BCRYPT_LOG_ROUNDS = 13,
    WTF_CSRF_ENABLED = True,
    DEBUG_TB_ENABLED = False,
    DEBUG_TB_INTERCEPT_REDIRECTS = False,
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT"),
    MAIL_DEFAULT_SENDER = "noreply@flask.com",
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_DEBUG = False,
    MAIL_USERNAME = os.getenv("EMAIL_USER"),
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    ))
    mail = Mail(app)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="noreply@flask.com",
    )
    mail.send(msg)


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
  # login code goes here
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  user = User.query.filter_by(email=email).first()

  # check if the user actually exists
  # take the user-supplied password, hash it, and compare it to the hashed password in the database
  if not user or not check_password_hash(user.password, password):
    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

  # if the above check passes, then we know the user has the right credentials
  login_user(user, remember=remember)
  return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
  return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
  # code to validate and add user to database goes here
  email = request.form.get('email')
  name = request.form.get('name')
  password = request.form.get('password')

  user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

  if user: # if a user is found, we want to redirect back to signup page so user can try again
    flash('Email address already exists')
    return redirect(url_for('auth.signup'))

  EMAIL_REGEX = re.compile(r"[A-Za-z]+@bc\.edu")

  if not EMAIL_REGEX.match(email):
    flash('Please use a BC email')
    return redirect(url_for('auth.signup'))

  # create a new user with the form data. Hash the password so the plaintext version isn't saved.
  new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

  # add the new user to the database
  db.session.add(new_user)
  db.session.commit()

  token = generate_token(new_user.email)

  confirm_url = url_for("auth.confirm_email", token=token, _external=True)
  html = render_template("confirm_email.html", confirm_url=confirm_url)
  subject = "Please confirm your email"
  send_email(new_user.email, subject, html)

  login_user(new_user)

  flash("A confirmation email has been sent via email.", "success")

  return redirect(url_for("main.inactive"))

  #return render_template("accounts/register.html", form=form)

  #return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.isConfirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("main.profile"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.isConfirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("main.profile"))