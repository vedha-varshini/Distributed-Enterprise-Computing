from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb+srv://dbuser:dbuser@stageeventscluster.f77s0.mongodb.net/?retryWrites=true&w=majority&appName=StageEventsCluster')
db = client.stage_events_db

# Insert stage events
event1_id = db.stage_event.insert_one({
    'name': 'Music Concert',
    'detail': 'A spectacular evening of live music performances.',
    'organizer': 'Concerts Inc.'
}).inserted_id

event2_id = db.stage_event.insert_one({
    'name': 'Drama Festival',
    'detail': 'A collection of plays performed by local theater groups.',
    'organizer': 'Drama Club'
}).inserted_id

# Insert stage event shows
show1_id = db.stage_event_show.insert_one({
    'start_time': '2024-01-01 18:00',
    'end_time': '2024-01-01 21:00',
    'stage_event_id': event1_id
}).inserted_id

show2_id = db.stage_event_show.insert_one({
    'start_time': '2024-01-02 18:00',
    'end_time': '2024-01-02 21:00',
    'stage_event_id': event1_id
}).inserted_id

show3_id = db.stage_event_show.insert_one({
    'start_time': '2024-01-03 17:00',
    'end_time': '2024-01-03 20:00',
    'stage_event_id': event2_id
}).inserted_id

show4_id = db.stage_event_show.insert_one({
    'start_time': '2024-01-04 17:00',
    'end_time': '2024-01-04 20:00',
    'stage_event_id': event2_id
}).inserted_id

# Insert ticket bookings
db.ticket_booking.insert_one({
    'customer': 'Alice',
    'price': 50.00,
    'no_of_seats': 2,
    'stage_event_show_id': show1_id
})

db.ticket_booking.insert_one({
    'customer': 'Bob',
    'price': 45.00,
    'no_of_seats': 3,
    'stage_event_show_id': show1_id
})

db.ticket_booking.insert_one({
    'customer': 'Charlie',
    'price': 60.00,
    'no_of_seats': 1,
    'stage_event_show_id': show2_id
})

db.ticket_booking.insert_one({
    'customer': 'Dave',
    'price': 55.00,
    'no_of_seats': 4,
    'stage_event_show_id': show3_id
})

db.ticket_booking.insert_one({
    'customer': 'Eve',
    'price': 70.00,
    'no_of_seats': 2,
    'stage_event_show_id': show4_id
})

print("Sample data inserted into MongoDB!")
