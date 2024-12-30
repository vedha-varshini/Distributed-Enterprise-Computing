from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://dbuser:dbuser@stageeventscluster.f77s0.mongodb.net/?retryWrites=true&w=majority&appName=StageEventsCluster'
mongo = PyMongo(app)

@app.route('/test_connection')
def test_connection():
    try:
        # Check MongoDB connection
        db = mongo.db
        if db is None:
            return "MongoDB connection is not established. Please check the connection string."

        # Try to access collections
        stage_event_exists = db.stage_event.find_one()
        stage_event_show_exists = db.stage_event_show.find_one()
        ticket_booking_exists = db.ticket_booking.find_one()

        if stage_event_exists and stage_event_show_exists and ticket_booking_exists:
            return "Connection successful and accessed all collections!"
        else:
            return "Connection successful, but one or more collections are empty or missing!"
    except Exception as e:
        return f"An error occurred while testing connection: {e}"

@app.route('/')
def index():
    try:
        events = db.stage_event.find()
        return render_template('index.html', events=events)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/event/<event_id>')
def event_detail(event_id):
    try:
        event = db.stage_event.find_one({'_id': ObjectId(event_id)})
        shows = db.stage_event_show.find({'stage_event_id': ObjectId(event_id)})
        return render_template('event_detail.html', event=event, shows=shows)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/show/<show_id>')
def show_detail(show_id):
    try:
        show = db.stage_event_show.find_one({'_id': ObjectId(show_id)})
        bookings = db.ticket_booking.find({'stage_event_show_id': ObjectId(show_id)})
        total_tickets = sum([booking['no_of_seats'] for booking in bookings])
        return render_template('show_detail.html', show=show, total_tickets=total_tickets)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/book/<show_id>', methods=['POST'])
def book_ticket(show_id):
    try:
        customer = request.form['customer']
        price = float(request.form['price'])
        no_of_seats = int(request.form['no_of_seats'])
        booking = {
            'stage_event_show_id': ObjectId(show_id),
            'customer': customer,
            'price': price,
            'no_of_seats': no_of_seats
        }
        db.ticket_booking.insert_one(booking)
        return redirect(url_for('show_detail', show_id=show_id))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
