from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

from urllib.parse import urlparse

import psycopg2
import os


app = Flask(__name__)

try:
	app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
except:
	app.config['SECRET_KEY'] = 'apparently_i_need_this'
socket = SocketIO(app)

# Database setup
try:
	url = urlparse(os.environ["DATABASE_URL"])

	database_connection = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)

	database = SQLAlchemy(app)

except:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/flask_chat'
	database = SQLAlchemy(app)

class History(database.Model):
	id = database.Column('id', database.Integer, primary_key=True)
	message = database.Column('message', database.String(500))

@socket.on('message')
def handleMessage(message_to_post):
	message = History(message=message_to_post)
	database.session.add(message)
	database.session.commit()

	send(message_to_post, broadcast=True)

@app.route('/')
def index():
    messages = History.query.all()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
	socket.run(app)
