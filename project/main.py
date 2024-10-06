from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User, Product
from . import db
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, DecimalField,
                     RadioField)
from wtforms.validators import InputRequired, Length

class ProductForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])
    meetup = IntegerField('meetup', validators=[InputRequired()])
    payment = IntegerField('payment', validators=[InputRequired()])
    condition = IntegerField('condition', validators=[InputRequired()])
    type = IntegerField('type', validators=[InputRequired()])



main = Blueprint('main', __name__)

@main.route('/')
def index():
  products = [1,2,3,4,5,6,7,8,9,10,11,12]
  return render_template('index.html', products=products)

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)

@main.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in Product.query.all() if p.id == product_id), None)
    if product:
      return render_template('product.html', product=product)
    else:
      return "Product not found"

@main.route('/add_item', methods =["GET", "POST"])
@login_required
def add_item():
  form = ProductForm()
  if request.method == "POST":
    if form.validate_on_submit():
      new_product = Product(name=form.name.data, desc=form.description.data, price=form.price.data, meetup=form.meetup.data, preferredPayment=form.payment.data, condition=form.condition.data, types=form.type.data, user_id=current_user.id)
      db.session.add(new_product)
      db.session.commit()
    else:
      flash("All fields must be filled before submitting")


  return render_template('add_item.html', form=form)