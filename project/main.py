from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User, Product
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  products = [1,2,3,4,5,6,7,8,9,10,11,12]
  return render_template('index.html', products=products)

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)

@main.route('/add_item', methods =["GET", "POST"])
@login_required
def add_item():
  # string is from name field of input elements in add_item.html, the dropdowns return the index (1-based) of the option selected
  # print(request.form.get("payment"))
  if request.form.get("name") != None:
    new_product = Product(name=request.form.get("name"), desc=request.form.get("description"), price=request.form.get("price"), meetup=request.form.get("meetup"), preferredPayment=request.form.get("payment"), condition=request.form.get("condition"), types=request.form.get("type"), user_id=current_user.id)
    db.session.add(new_product)
    db.session.commit()
  # current_user.id for user id
  # look at models.py
  # auth.py line 50


  return render_template('add_item.html')