from flask_login import UserMixin
from . import db

PAYMENT = {
  1: "Cash",
  2: "Venmo",
  3: "Paypal",
  4: "Zelle"
}

LOCATION = {
  1: "Upper",
  2: "Lower",
  3: "Newton"
}

CONDITION = {
  1: "New",
  2: "Used (like new)",
  3: "Used (good)",
  4: "Used (fair)",
  5: "Refurbished",
}

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  name = db.Column(db.String(1000))
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  products = db.relationship('Product', backref='owner', lazy=True)  
  rating = db.Column(db.Float, nullable=False, default=0.0)
  location = db.Column(db.String(100))
  isOfficial = db.Column(db.Boolean, nullable=True, default=False)
  isConfirmed = db.Column(db.Boolean, nullable=False, default=False)

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

  def getPayment(self):
    return PAYMENT.get(self.preferredPayment, "Unknown payment method")

  def getLocation(self):
    return LOCATION.get(self.meetup, "Unknown location")

  def getCondition(self):
    return CONDITION.get(self.condition, "Unspecified condition")