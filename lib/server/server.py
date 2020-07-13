import hashlib
from flask import Flask, render_template,session,redirect,request
from flask_socketio import SocketIO,Namespace,emit,join_room,leave_room,close_room,rooms,disconnect
from threading import Lock
from chaines import Block,Blockchain
from flask_cors import CORS
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#CORS(app)
#cors = CORS(app,resources={r"/*":{"origin":"*"}})
io = SocketIO(app,cors_allowed_origins="*")
thread = None

thread_lock=Lock()

user_info={}
Block_chain = Blockchain()

def dic_block(message):
    data = hashlib.sha224(message['data'].encode('ascii')).hexdigest()
    return Block(data,message['my_time'],message['previous_hash'],message['sender'],message['reciver'])

def dictionary_to_block(message):
    return Block(message['data'],message['my_time'],message['previous_hash'],message['sender'],message['reciver'])



def background_thread():
    print("-----------come background---------")
    last= Block_chain.last_block
    dic={
        'sender':last.sender,
        'reciver':last.reciver,
        'hash' : last.compute_hash()   
    }
    print(dic)
    io.emit('store_block',dic,namespace='/test')

    
'''
@app.route('/')
@app.route('/test')
def test_route():
   return render_template('test.html')
'''
#count1 =0


class Collect:
    def __init__(self):
        self.count=0
    def incrise(self):
        self.count+=1
    def decrise(self):
        self.count-=1
    def nuterl(self):
        self.count=0
    def get_val(self):
        return self.count
            

co = Collect()

def  collect_chain(sumitted_block):


    #user_info=user_info
    #global count1
    
    for single_user in user_info.keys():
        single_user+='_chain'
        @io.on(single_user, namespace='/test')
        def collect_chain(last_block):
            #last_block= dictionary_to_block(last_block)
            if last_block['hash']==sumitted_block.previous_hash:
               co.incrise()
               print("_______in count_____",co.get_val())
               
            else:
               co.decrise()
               print('_________de count____',co.get_val)
    print("-------get count :",co.get_val())
    
    if co.get_val()<0 :
        print("-------get count befor :",co.get_val())
        co.nuterl()
        print("-------get count after:",co.get_val())
        return False 
    else:
        print("-------get count befor:",co.get_val())
        co.nuterl()
        print("-------get count after :",co.get_val())

        return True



          





@io.on('connect', namespace='/test')
def test_connect():
    #print ('---------connected-----------')
    background_thread()
    '''
    global thread
    with thread_lock:
        if thread is None:
            print('________________work_______________')
            thread = io.start_background_task(background_thread)
    #emit('my_response', {'data': 'Connected'})
    '''


@io.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@io.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
    #{k:v for k, v in user_info if v!=request.sid}


@io.on('user_id',namespace='/test')
def user_id(user):
    usr= str(user['data'])
    #print('________________________user:',type(usr))
    user_info[usr]=request.sid
    emit('just')

@io.on('private_message',namespace='/test')
def private_message(message):
    #usr = message['reciver']
    #print('------user id -------',usr)
    #print()
    #emit('private_message',message,room=user_info[usr])
    
    emit('send_lastblock',broadcast=True)
    block = dic_block(message)
    #print("work")
    
    if collect_chain(block):
        #global count1
        #print('infunction count--------------------',count1)
        prof,block=Block_chain.proof_of_work(block)
       # print('seeproof-------------:',prof,block)
        res = Block_chain.add_block(block,prof)

        #print("find res ---------------:",res)

        if res :

            usr= str(block.reciver)
            dic={
                'sender':block.sender,
                'reciver':block.reciver,
                'hash':block.compute_hash()

            }
            emit('add_in_blockchain',dic,broadcast=True)
            #print('-------work-----------',message)
            usr = message['reciver']
            #print('------user id -------',type(usr))
            #print('------------------user info ',user_info)
            emit('private_message',message,room=user_info[usr])
    

        
       

    



    



    
    






















if __name__ == '__main__':
    io.run(app,debug =True)