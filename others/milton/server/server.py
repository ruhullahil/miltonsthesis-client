from flask import Flask, render_template,session,redirect,request
from flask_socketio import SocketIO,Namespace,emit,join_room,leave_room,close_room,rooms,disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
















if __name__ == '__main__':
    socketio.run(app)