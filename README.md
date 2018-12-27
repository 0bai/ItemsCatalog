# Items Catalog

A website that that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project uses the FSND-Virtual-Machine and python3 if you don't have that installed please refer back to the FSND lessons and follow the instructions.

### Installing

First we need to download and move the project folder to your FSND vagrant directory :

```
mv Dowloads/ItemsCatalog FSND-Virtual-Machine/vagrant/
```

After that we need to get the FSND Virtual Machine running :
```
cd FSND-Virtual-Machine/vagrant
vagrant up
vagrant ssh
```
Then we need to install Flask, sqlAlchemy & the rest of our requirements
```
pip3 install flask
pip3 install sqlalchemy
pip3 install flask-sqlalchemy
pip3 install requests
pip3 install httplib2
pip3 install request
pip3 install passlib
pip3 install oauth2client
pip3 install pycodestyle
```
And now we are ready to run and seed our database
```
cd FSND-Virtual-Machine/vagrant/ItemsCatalog
python3 itemsCatalogDB_setup.py
python3 seeder.py
```
Lastly we need to run our app
```
python3 app.py
```
## Running the tests

### Program correctness
To check the program for correctness access the [web page](http://localhost:8000) and sign in with your google account. 
### Python code style

To check if the program file conforms to Python code style run

```
pycodestyle app.py
```

## Built With
* [python3](https://www.python.org/download/releases/3.0/) Python is an open soure and easy to learn programming language. 
* [pip3](https://pip.pypa.io/en/stable/) - Dependency Management.
* [flask](http://flask.pocoo.org) - Flask is a microframework for Python based on Werkzeug and Jinja 2.
* [OAuth2](https://oauth.net/2/) - OAuth 2.0 is the industry-standard protocol for authorization. 
* [sqlalchemy](https://www.sqlalchemy.org) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

## Authors

* **Obai Alnajjar** - *Initial work* - [0bai](https://github.com/0bai)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Udacity Full Stack Nano Degree Team
