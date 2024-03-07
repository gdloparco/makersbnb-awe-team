import os
from flask import Flask, request, render_template, redirect
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

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# GET PROPERTY ROUTES
@app.route('/property_list', methods=['GET'])
def get_property_list():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
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
    # We use `render_template` to send the user the file `property_id.html`
    return render_template('property_id.html', property=property)

# BOOK PROPERTY ROUTES
# BOOK /PROPERTY_{ID}
@app.route('/property_request_sent', methods=['GET'])
def get_property_request_success():
    return render_template('property_request_sent.html')

@app.route('/make_booking', methods=['POST'])
def book_property():
    # Get the property_id from the webpage based on which
    # property was being viewed
    property_id = request.form.get('property_id')
    # Set up the database connection and repositories
    # to save the booking to the database and access
    # owner / user info
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    property_repository = PropertyRepository(connection)
    user_repository = UserRepository(connection)
    start_date = '2025-01-01'
    end_date = '2025-02-01'
    total_cost = '500'
    # Get the relevant information to make the booking
    # and send the confirmation
    property = property_repository.find(property_id)
    owner_id = property.user_id
    owner = user_repository.find_by_id(owner_id)
    # Create the booking in the bookings table
    new_booking = Booking(0, start_date, end_date, 1, property_id)
    booking_repository.create(new_booking)
    # Send email confirmations to the user who made the
    # booking and the owner, and then redirect the user
    # to the 'success' page
    emailer = EmailManager()
    emailer.send_email('series4000kryten@gmail.com', 'Your MakersBnB booking', f'Thank you for booking through MakersBnB. Your request has been sent to the property host, who will be in touch soon.\n\nYour booking details:\nStart date: {start_date}\nEnd date: {end_date}\nTotal cost: £{total_cost}')
    emailer.send_email(owner.email, 'Someone wants to book your MakersBnB property', f'Someone wants to book your MakersBnB property! See the details below, and then approve or deny the request.\n\nBooking details:\nStart date: {start_date}\nEnd date: {end_date}\nTotal cost: £{total_cost}')
    return redirect('/property_request_sent')

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
    return render_template('create_property.html', properties = properties)

@app.route('/create_property', methods=['POST'])
def post_create_property():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    name = request.form['name']
    description = request.form['description']
    cost_per_night = request.form['cost_per_night']
    username = request.form['username']
    user_repository = UserRepository(connection)
    user = user_repository.find(username)
    property = Property(0, name, description, cost_per_night, user.id)
    validator = PropertyParametersValidator(name, description, cost_per_night)
    if not validator.is_valid():
        return render_template('create_property.html', errors=validator.generate_errors()), 400
    else:
        property = repository.create(property)
    return redirect('/property_list')

#  Log In
@app.route('/log_in')
def get_log_in():
    return render_template('log_in.html')

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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
