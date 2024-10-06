from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Product
from . import db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, DecimalField,
                     RadioField, FloatField)
from wtforms.validators import InputRequired, Length
from flask_optional_routes import OptionalRoutes
from base64 import b64encode
import base64
from io import BytesIO



def isUserConfirmed(func):
    if current_user.isConfirmed is False:
        flash("Please confirm your account!", "warning")
        return redirect(url_for("main.inactive"))
    return func


class ProductForm(FlaskForm):
    image = FileField("image", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    name = StringField('name', validators=[InputRequired()])
    description = TextAreaField('description', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])
    meetup = IntegerField('meetup', validators=[InputRequired()])
    payment = IntegerField('payment', validators=[InputRequired()])
    condition = IntegerField('condition', validators=[InputRequired()])
    type = IntegerField('type', validators=[InputRequired()])

class FilterForm(FlaskForm):
  category = IntegerField('category')
  priceMin = FloatField('priceMin')
  priceMax = FloatField('priceMax')
  location = IntegerField('location')
  condition = IntegerField('condition')

main = Blueprint('main', __name__)

optional = OptionalRoutes(main)

@main.route('/', methods =["GET", "POST"])
def index():
  form = FilterForm()
  products = Product.query.all()
  featured = Product.query.filter_by(user_id=1)
  featured_products = featured.all()
  scroll=None
  remove_list = []

  if request.method == "POST":
    scroll = "page-break"

    search_query = request.form.get('search')
    type_list = request.form.getlist('type')
    priceMin = request.form.get('priceMin')
    priceMax = request.form.get('priceMax')
    location_list = request.form.getlist('location')
    condition_list = request.form.getlist('condition')

    for p in products:
      if not (search_query.lower() in p.name.lower() or search_query.lower() in p.desc.lower()):
        remove_list.append(p)
      if str(p.types) not in type_list and type_list != []:
        remove_list.append(p)
      if priceMin != "":
        if p.price < float(priceMin):
          remove_list.append(p)
      if priceMax != "":
        if p.price > float(priceMax):
          remove_list.append(p)
      if str(p.meetup) not in location_list and location_list != []:
        remove_list.append(p)
      if str(p.condition) not in condition_list and condition_list != []:
        remove_list.append(p)

  new_product_list = [x for x in products if x not in remove_list]
  print(new_product_list)

  return render_template('index.html', products=new_product_list, featured_products=featured_products, form=form, scroll=scroll)

@optional.routes('/profile/<int:user_id>?/')
@login_required
def profile(user_id=None):
  
  if user_id is not None:
    user = User.query.get(user_id)
    ret = render_template('profile.html', 
      id=user.id,
      name=user.name,
      email=user.email,
      location=user.location,
      rating=user.rating,
      owned_products=user.products)
    return isUserConfirmed(ret)
  ret = render_template('profile.html', 
      id=current_user.id,
      name=current_user.name,
      email=current_user.email,
      location=current_user.location,
      rating=current_user.rating,
      owned_products=current_user.products)
  return isUserConfirmed(ret)

@main.route('/product/<int:product_id>')
@login_required
def product(product_id):
    product = next((p for p in Product.query.all() if p.id == product_id), None)
    if product:
      seller = next((s for s in User.query.all() if s.id == product.user_id), None)
      return render_template('product.html', product=product, seller=seller)
    else:
      return "Product not found"
    
@optional.routes('/allproducts/', methods =["GET", "POST"])
@login_required
def allproducts():
  form = FilterForm()
  products = Product.query.all()
  remove_list = []

  if request.method == "POST":
    search_query = request.form.get('search')
    type_list = request.form.getlist('type')
    priceMin = request.form.get('priceMin')
    priceMax = request.form.get('priceMax')
    location_list = request.form.getlist('location')
    condition_list = request.form.getlist('condition')

    for p in products:
      if not (search_query.lower() in p.name.lower() or search_query.lower() in p.desc.lower()):
        remove_list.append(p)
      if str(p.types) not in type_list and type_list != []:
        remove_list.append(p)
      if priceMin != "":
        if p.price < float(priceMin):
          remove_list.append(p)
      if priceMax != "":
        if p.price > float(priceMax):
          remove_list.append(p)
      if str(p.meetup) not in location_list and location_list != []:
        remove_list.append(p)
      if str(p.condition) not in condition_list and condition_list != []:
        remove_list.append(p)

  new_product_list = [x for x in products if x not in remove_list]
  print(new_product_list)
      
  return render_template('allproducts.html', products=new_product_list, remove_list=remove_list, form=form)


@main.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
  Product.query.filter(Product.id == id).delete()
  db.session.commit()
  return redirect('/')


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
      return redirect('/')
    else:
      flash("All fields must be filled before submitting")
      return render_template('add_item.html', form=form)
  else:
    ret = render_template('add_item.html', form=form)
    return isUserConfirmed(ret)
  
@main.route("/inactive")
@login_required
def inactive():
    if current_user.isConfirmed:
        return redirect(url_for("main.profile"))
    return render_template("inactive.html")