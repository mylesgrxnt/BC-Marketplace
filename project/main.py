from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User, Product
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)

@main.route('/add_item', methods =["GET", "POST"])
@login_required
def add_item():
  # string is from name field of input elements in add_item.html, the dropdowns return the index (1-based) of the option selected
  print(request.form.get("payment")) 


  return render_template('add_item.html')