import os
from flask import Flask, request, render_template, redirect, session, url_for, jsonify
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User
from lib.property_repository import PropertyRepository
from lib.property import Property
from lib.user_parameters_validator import UserParametersValidator
from lib.property_parameters_validator import PropertyParametersValidator
from lib.comms import EmailManager
from lib.booking_repository import BookingRepository
from lib.booking import Booking

# Create a new Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'teamvenerarulestheworld!@£$%'


# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username = username)
    return render_template('index.html')

# GET PROPERTY ROUTES
@app.route('/property_list', methods=['GET'])
def get_property_list():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    if 'username' in session:
        username = session['username']
        return render_template('property_list.html', username = username, properties = properties)
    return render_template('property_list.html', properties = properties)

# GET /property
# Returns the property with the supplied name as HTML
# Try it:
#   ; open http://localhost:5001/property_{{id}}
@app.route('/property_<int:id>', methods=['GET'])
def get_property(id):
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    property = repository.find(id)
    if 'username' in session:
        username = session['username']
        return render_template('property_id.html', username = username, property = property)
    # We use `render_template` to send the user the file `property_id.html`
    return render_template('property_id.html', property=property)

# BOOK PROPERTY ROUTES
# BOOK /PROPERTY_{ID}
@app.route('/property_request_sent', methods=['GET'])
def get_property_request_success():
    return render_template('property_request_sent.html')

from flask import request, redirect, render_template, session
from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.property_repository import PropertyRepository
from lib.user_repository import UserRepository

@app.route('/make_booking', methods=['POST'])
def book_property():
    # Check if the user is logged in
    if 'username' in session:
        # Set up the database connection and repositories
        # to save the booking to the database and access
        # owner / user info
        connection = get_flask_database_connection(app)
        booking_repository = BookingRepository(connection)
        property_repository = PropertyRepository(connection)
        user_repository = UserRepository(connection)
        
        # Get the property_id from the webpage based on which
        # property was being viewed
        property_id = request.form.get('property_id')
        
        # Get the start and end dates from the form inputs
        start_date = request.form.get('start_day')
        end_date = request.form.get('end_day')
        
        # Get the logged-in user's id
        username = session['username']
        booker = user_repository.find(username)
        
        # Create the booking instance
        new_booking = Booking(id=0, start_date=start_date, end_date=end_date,
                                user_id=booker.id, property_id=property_id)
        
        # Save the booking to the database
        try:
            booking_repository.create(new_booking)
        except Exception as e:
            return render_template('error.html', error_message=str(e))
        
        # Redirect the user to the booking confirmation page
        return render_template('property_request_sent.html', new_booking=new_booking)
    
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect('/log_in')


# CREATE USER
@app.route('/create_user')
def get_create_user():
    return render_template('create_user.html')

@app.route('/create_user', methods=['POST'])
def post_create_user():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    user = User(None, username, email, password, phone)
    validator = UserParametersValidator(username, email, password, phone)
    if not validator.is_valid() or not validator.is_password_valid():
        return render_template('create_user.html', errors=validator.generate_errors(), password_errors=validator.generate_password_errors()), 400
    else:
        user = repository.create(user)
    return redirect('/index')

# CREATE PROPERTY ROUTES
@app.route('/create_property')
def get_create_property():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    if 'username' in session:
        username = session['username']
        return render_template('create_property.html', username = username, properties = properties)    
    return render_template('create_property.html', properties = properties)

@app.route('/create_property', methods=['POST'])
def post_create_property():
    # Check if the user is logged in
    if 'username' in session:
        connection = get_flask_database_connection(app)
        repository = PropertyRepository(connection)
        name = request.form['name']
        description = request.form['description']
        cost_per_night = request.form['cost_per_night']
        username = session['username']
        user_repository = UserRepository(connection)
        user = user_repository.find(username)
        property = Property(0, name, description, cost_per_night, user.id)
        validator = PropertyParametersValidator(name, description, cost_per_night)
        if not validator.is_valid():
            return render_template('create_property.html', errors=validator.generate_errors()), 400
        else:
            property = repository.create(property)
        return redirect('/property_list')
    else:
        return redirect('/log_in')

#  Log In
@app.route('/log_in')
def get_log_in():
    return render_template('log_in.html')

"""
@app.route('/log_in', methods=['POST'])
def post_log_in():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    email = request.form['email']
    password = request.form['password']
    user = User(email=email, password=password)
    validator = UserParametersValidator(email, password)
    if not validator.is_valid():
        return render_template('create_user.html', errors=validator.generate_errors()), 400
    else:
        user = repository.create(user)
    return redirect('/index')
"""

# Log In - ANDRE VERSION
@app.route('/log_in', methods=['POST'])
def post_log_in():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    email = request.form['email']
    password = request.form['password']

    # Validate user input
    validator = UserParametersValidator(username=None, email=email, password=password, phone=None)

    if not validator.login_is_valid():
        # Handle invalid input
        return render_template('log_in.html', errors=[validator.generate_errors()])

    # Validate credentials and retrieve the user
    user = repository.find_by_email(email)

    if user and user.password == password:  # Check password here
        # Set the user's ID in the session
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/index')
    else:
        # Handle invalid credentials
        return render_template('log_in.html', errors=['Invalid email or password'])

# Log out
@app.route('/logout', methods=['GET'])
def logout():
    # Clear the user session
    session.clear()

    # Redirect to the login page (or any other desired page)
    return redirect(url_for('get_index'))

























































# get page user details
@app.route('/user_<username>', methods=['GET'])
def get_user_details(username):
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    properties = user_repo.find_properties_by_username(username)
    if 'username' in session:
        username = session['username']
        return render_template('user_profile.html', username = username, properties = properties)
    return render_template('user_profile.html', username = username)


# GET /property
# Returns the property with the supplied name as HTML
# Try it:
#   ; open http://localhost:5001/property_{{id}}
# @app.route('/property_<int:id>', methods=['GET'])
# def get_property(id):
#     connection = get_flask_database_connection(app)
#     repository = PropertyRepository(connection)
#     property = repository.find(id)
#     if 'username' in session:
#         username = session['username']
#         return render_template('property_id.html', username = username, property = property)
#     # We use `render_template` to send the user the file `property_id.html`
#     return render_template('property_id.html', property=property)






# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
