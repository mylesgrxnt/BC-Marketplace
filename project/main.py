from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Product
from . import db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, DecimalField,
                     RadioField)
from wtforms.validators import InputRequired, Length
from flask_optional_routes import OptionalRoutes
from base64 import b64encode
import base64
from io import BytesIO

class ProductForm(FlaskForm):
    image = FileField("image", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    name = StringField('name', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])
    meetup = IntegerField('meetup', validators=[InputRequired()])
    payment = IntegerField('payment', validators=[InputRequired()])
    condition = IntegerField('condition', validators=[InputRequired()])
    type = IntegerField('type', validators=[InputRequired()])

main = Blueprint('main', __name__)

optional = OptionalRoutes(main)

@optional.routes('/<int:category>?/')
def index(category=None, priceMin=None, priceMax=None, location=None, condition=None):
  products = Product.query.all()
  for p in products:
    if p.types != category:
      products.remove(p)
      
  return render_template('index.html', products=products)

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', 
    name=current_user.name,
    email=current_user.email,
    location=current_user.location,
    rating=current_user.rating,
    owned_products=current_user.products)

@main.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in Product.query.all() if p.id == product_id), None)
    if product:
      seller = next((s for s in User.query.all() if s.id == product.user_id), None)
      return render_template('product.html', product=product, seller=seller)
    else:
      return "Product not found"

@main.route('/add_item', methods =["GET", "POST"])
@login_required
def add_item():
  form = ProductForm()
  if request.method == "POST":
    if form.validate_on_submit():
      testFile = form.image.data
      data = testFile.read()
      renderedTestFile = base64.b64encode(data).decode('utf-8')
      new_product = Product(name=form.name.data, desc=form.description.data, price=form.price.data, meetup=form.meetup.data, preferredPayment=form.payment.data, condition=form.condition.data, types=form.type.data, user_id=current_user.id, image_data=data, image_rendered_data=renderedTestFile)
      db.session.add(new_product)
      db.session.commit()
    else:
      flash("All fields must be filled before submitting")


  return render_template('add_item.html', form=form)