from datetime import datetime

from dietapp import db
from dietapp import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carbohydrate = db.Column(db.Integer)
    calorie = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    used_in = db.relationship('Ingredient', backref='product', lazy=True)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carbohydrate = db.Column(db.Integer)
    calorie = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    ingredients = db.relationship('Ingredient', backref='meal', lazy=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(256))
    role = db.Column(db.String(50), nullable=False, default='user')

    diet_id = db.Column(db.Integer, db.ForeignKey('diets.id'), nullable=False)

    meals = db.relationship('Meal', backref='author', lazy=True)
    products = db.relationship('Product', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.email}'"


class Diet(db.Model):
    __tablename__ = 'diets'
    id = db.Column(db.Integer, primary_key=True)
    limit_protein = db.Column(db.Integer)
    limit_fat = db.Column(db.Integer)
    limit_carbohydrate = db.Column(db.Integer)
    limit_calorie = db.Column(db.Integer)

    users = db.relationship('User', backref='current_diet', lazy=True)
