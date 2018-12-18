from flask import Flask, render_template, request, redirect, make_response, jsonify, url_for, flash, make_response, \
    session as login_session
import random, string, httplib2, json, requests
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from itemsCatalogDB_setup import Base, User, Item, Category
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Items Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///itemsCatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Landing page route
@app.route("/")
def show_landing_page():
    state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session["state"] = state
    categories = get_categories()
    latest = get_items(limit=10)
    return render_template("index.html", categories=categories, latest=latest, STATE=state)


# Show category page route
@app.route("/<string:category>")
def show_category(category):
    categories = get_categories()
    items = get_items(get_category_id(category))
    return render_template("category/show.html", category=category, items=items, categories=categories)


# Add new item page route
@app.route("/items/new", methods=["GET", "POST"])
def new_item():
    if request.method == "GET":
        return render_template("item/new.html")
    item = Item(title=request.form["title"], description=request.form["description"], image=request.form["image"],
                category=get_category_info(category_id=request.form["category"]),
                user=get_user_info(login_session["user_id"]),
                user_id=login_session["user_id"], category_id=request.form["category"])
    session.add(item)
    session.commit()
    return redirect(url_for("show_item", category=item.category.name, item=item.title))


# Edit item page route
@app.route("/<string:category>/<string:item>/edit", methods=["GET", "POST"])
def edit_item(category, item):
    category = get_category_info(category_name=category)
    item = get_item(item, category.id)
    categories = get_categories()
    # if the item exists
    if item:
        if request.method == "GET":
            return render_template("item/edit.html", item=item, category=category, categories=categories)
        # if the category is changed check if there's an item with the same name in that category
        if request.form["category"] != category.id:
            new_category = get_category_info(category_id=request.form["category"])
            if get_item(item, new_category):
                flash("An Item with this name already exist in the new category please select a new category !")
                return redirect(url_for("edit_item", item=item.title, category=category.name))
            category = new_category
        item.title = request.form["title"]
        item.description = request.form["description"]
        item.image = request.form["image"]
        item.category = category
        item.category_id = category.id
        session.add(item)
        session.commit()
        return redirect(url_for("show_item", item=item.title, category=category.name))
    flash("Item does not exist!")
    return redirect(url_for("show_landing_page"))


# Delete item page route
@app.route("/<string:category>/<string:item>/delete", methods=["GET", "POST"])
def delete_item(category, item):
    if request.method == "GET":
        return render_template("item/delete.html", category=category, item=item)
    category = get_category_info(category_name=category)
    item = get_item(item, category.id)
    if item:
        session.delete(item)
        session.commit()
        return redirect(url_for("show_category", category=category.name))
    flash("Item does not exist!")
    return redirect(url_for("show_landing_page"))


# Show item page route
@app.route("/<string:category>/<string:item>")
def show_item(category, item):
    category = get_category_info(category_name=category)
    item = get_item(item, category.id)
    return render_template("item/show.html", item=item, category=category)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        flash("Current user is already connected.")
        return redirect(url_for("show_landing_page"))

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    print(data)
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = get_user_id(login_session["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session["user_id"] = user_id
    flash("you are now logged in as %s" % login_session['username'])
    return redirect(url_for("show_landing_page"))


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def create_user(login_session):
    new_user = User(name=login_session["username"], email=login_session["email"], image=login_session["picture"])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session["email"]).one()
    return user.id


def get_user_info(user_id):
    return session.query(User).filter_by(id=user_id).one()


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_category_id(name):
    try:
        category = session.query(Category).filter_by(name=name).one()
        return category.id
    except:
        return None


def get_category_info(category_name=None, category_id=None):
    if category_id:
        return session.query(Category).filter_by(id=category_id).one()
    return session.query(Category).filter_by(name=category_name).one()


def get_items(category_id=None, limit=None):
    if limit:
        return session.query(Item).order_by(Item.timestamp.desc()).limit(10)
    return session.query(Item).filter_by(category_id=category_id).all()


def get_item(title, category_id):
    try:
        item = session.query(Item).filter_by(title=title, category_id=category_id)
        return item
    except:
        return None


def get_categories():
    return session.query(Category).all()


if __name__ == '__main__':
    app.secret_key = "5Jdkl892$21!*9dsfjljeiol"
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
