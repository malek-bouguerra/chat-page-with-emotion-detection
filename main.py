from flask import Flask
from flask_socketio import SocketIO, send, emit
from aylienapiclient import textapi


USER_NAMES={}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app,cors_allowed_origins='*')

client = textapi.Client("be8862f5", "873f2bb1ab151d51d050114c84018841")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



@socketio.on('my event message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	if str(json['message'])!='':
		msg=json['message']
		sentiment = client.Sentiment({'text': json['message']})['polarity']
		if sentiment=='positive':
			emoji=":)"
		elif sentiment=='negative':
			emoji=":("
		else:
			emoji=":|"
		print('Message: ' + msg)
		msg_emoji= msg+ " "+emoji
		json['message']=msg_emoji
		json['user_name']=USER_NAMES[json['user_id']]
		socketio.emit('my response', json, callback=messageReceived)
	print('received my event: ' + str(json))

@socketio.on('my event connection')
def handle_my_connection(json, methods=['GET', 'POST']):
	USER_NAMES[json['user_id']]=json['user_name']
	print('user_names dict',USER_NAMES)
	socketio.emit('my response connection',USER_NAMES, callback=messageReceived)
	print('received my event: ' + str(json))

@socketio.on('disconnection event')
def handleDisconnection(id,methods=['GET', 'POST']):
	socketio.emit('response disconnection',USER_NAMES[id], callback=messageReceived)
	del USER_NAMES[id]
	print(USER_NAMES, 'deleted')


if __name__ == '__main__':
	# print('helloWorld')
	socketio.run(app)



# sentiment = client.Sentiment({'text': msg})['polarity']
# 	if sentiment=='positive':
# 		emoji=":)"
# 	elif sentiment=='negative':
# 		emoji=":("
# 	else:
# 		emoji=":|"
# 	print('Message: ' + msg)
# 	msg_emoji= msg+ " "+emoji
# 	send(msg_emoji, broadcast=True)