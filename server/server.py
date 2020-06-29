from flask import Flask, render_template,session,redirect,request
from flask_socketio import SocketIO,Namespace,emit,join_room,leave_room,close_room,rooms,disconnect
from threading import Lock
from chaines import Block,Blockchain
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#CORS(app)
#cors = CORS(app,resources={r"/*":{"origin":"*"}})
io = SocketIO(app,cors_allowed_origins="*")
thread = None

thread_lock=Lock()

user_info={}
t_message={}
Block_chain = Blockchain()


def background_thread():

    pass
'''
@app.route('/')
@app.route('/test')
def test_route():
   return render_template('test.html')
'''


def collect_chain(sumitted_block):
    
    for single_user in user_info.key:
        single_user+='_chain'

        count=0
        @io.on(single_user, namespace='/test')
        def collect_chain(last_block):
            if last_block.compute_hash()!=sumitted_block.previous_hash:
                count+=1
            else:
                count-=1
    if count<0 : return False
    return True


          

def dic_block(message):
    return Block(message['data'],message['timestamp'],message['previous_hash'],message['sender'],message['reciver'])



@io.on('connect', namespace='/test')
def test_connect():
    print ('connected')
    '''
    global thread
    with thread_lock:
        if thread is None:
            thread = io.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected'})
    '''

@io.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@io.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@io.on('user_name',namespace='/test')
def user_name(user):
    user_info[user]=request.sid

@io.on('private_message',namespace='test')
def private_message(message):
    
    block = dic_block(message)
    if collect_chain(block):
       res = Block_chain.add_block(block)
       usr= block.reciver
       emit('add_in_blockchain',{'block':block},broadcast=True)
       emit('private_message',message,room=user_info[usr])

        
       

    



    



    
    






















if __name__ == '__main__':
    io.run(app)