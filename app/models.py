from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    products = db.relationship('Product', secondary='cart')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()
       

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    description = db.Column(db.String(500))
    users = db.relationship('User', secondary='cart')
    

    def __init__(self, name, price, image_url, description):
        self.name = name
        self.price = price
        self.image_url = image_url
        self.description = description
    
    def __repr__(self):
        return f'<Product: {self.name}>'



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

