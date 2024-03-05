import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from lib.user_repo import userRepository
from lib.user import User
from lib.property_repository import PropertyRepository
from lib.property import Property
# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/property_list', methods=['GET'])
def get_property_list():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    return render_template('property_list.html', properties = properties)

@app.route('/create_user')
def get_create_user():
    return render_template('create_user.html')

@app.route('/create_user', methods=['POST'])
def post_create_user():
    connection = get_flask_database_connection(app)
    repository = userRepository(connection)
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    user = User(None, username, email, password, phone)
    user = repository.create(user)
    return redirect('/index')

@app.route('/create_property')
def get_create_property():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    return render_template('create_property.html', properties = properties)

@app.route('/create_property', methods=['POST'])
def post_create_property():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    name = request.form['name']
    description = request.form['description']
    cost_per_night = request.form['cost_per_night']
    user_id = request.form['username']
    property = Property(name, description, cost_per_night, user_id)
    property = repository.create(property)
    return redirect('/property_list')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
