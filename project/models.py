from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  name = db.Column(db.String(1000))
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  products = db.relationship('Product', backref='owner', lazy=True)  
  rating = db.Column(db.Float, nullable=False, default=0.0)
  location = db.Column(db.String(100))
  isOfficial = db.Column(db.Boolean, nullable=True, default=False)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  desc = db.Column(db.String(2000), nullable=False)
  price = db.Column(db.Numeric(5, 2), nullable=False)
  meetup = db.Column(db.Integer, nullable=False)
  preferredPayment = db.Column(db.Integer, nullable=False)
  condition = db.Column(db.Integer, nullable=False)
  types = db.Column(db.Integer, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  image_data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
  image_rendered_data = db.Column(db.Text, nullable=False) #Data to render the pic in browser