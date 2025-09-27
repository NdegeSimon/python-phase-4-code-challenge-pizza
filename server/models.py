from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship("RestaurantPizza", backref="restaurant", cascade="all, delete")

    def to_dict(self, include_relationships=False):
        data = {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }
        if include_relationships:
            data["restaurant_pizzas"] = [rp.to_dict() for rp in self.restaurant_pizzas]
        return data


class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship("RestaurantPizza", backref="pizza", cascade="all, delete")

    def to_dict(self, include_relationships=False):
        data = {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }
        if include_relationships:
            data["restaurant_pizzas"] = [rp.to_dict() for rp in self.restaurant_pizzas]
        return data


class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    @validates("price")
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("validation errors")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza_id": self.pizza_id,
            "restaurant_id": self.restaurant_id,
            "pizza": self.pizza.to_dict(),
            "restaurant": self.restaurant.to_dict()
        }
