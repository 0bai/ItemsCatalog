from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from itemsCatalogDB_setup import Base, User, Item, Category
import random, string, httplib2, json, requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///itemsCatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Landing page route
@app.route("/")
def show_landing_page():
    categories = session.query(Category).all()
    latest = session.query(Item).order_by(Item.timestamp.desc()).limit(10)
    return render_template("index.html", categories=categories, latest=latest)


@app.route("/<string:category>")
def show_category(category):
    category_id = session.query(Category).filter_by(name=category).one().id
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template("category/show.html", category=category, items=items, categories=categories)


@app.route("/items/new", methods=["GET", "POST"])
def new_item():
    if request.method == "GET":
        return render_template("item/new.html")
    category = session.query(Category).filter_by(id=request.form["category"]).one()
    #take the user from the login session
    user = session.query(User).filter_by(id=1).one()
    item = Item(title=request.form["title"],  description=request.form["description"], image=request.form["image"], category=category, user=user)
    session.add(item)
    session.commit()
    return redirect(url_for("show_category", category=category.name))

@app.route("/<string:category>/<string:item>")
def show_item(category, item):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(Item).filter_by(title=item, category=category).one()
    return render_template("item/show.html", item=item, category=category)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
