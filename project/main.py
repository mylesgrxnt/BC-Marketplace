from flask import Blueprint, render_template
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

@main.route('/add_item')
@login_required
def add_item():
  return render_template('add_item.html')