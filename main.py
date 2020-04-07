from flask import Flask
from flask_socketio import SocketIO, send, emit
from aylienapiclient import textapi
from flask_login import current_user



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app,cors_allowed_origins='*')

client = textapi.Client("be8862f5", "873f2bb1ab151d51d050114c84018841")

@socketio.on('message')
def handleMessage(msg):
	sentiment = client.Sentiment({'text': msg})['polarity']
	if sentiment=='positive':
		emoji=":)"
	elif sentiment=='negative':
		emoji=":("
	else:
		emoji=":|"
	print('Message: ' + msg)
	msg_emoji= msg+ " "+emoji
	send(msg_emoji, broadcast=True)

@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
        emit('my response',
             {'message': '{0} has joined'.format(current_user.name)},
             broadcast=True)
    else:
        return False  # not allowed here

if __name__ == '__main__':
	# print('helloWorld')
	socketio.run(app)