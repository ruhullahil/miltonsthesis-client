import os,hashlib
from flask import Flask, render_template,session,redirect,request,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, relationship


tem_path=  os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
tem_path = os.path.join(tem_path,'milton')
tem_path = os.path.join(tem_path,'client')
tem_path =os.path.join(tem_path,'temptates')
print(tem_path)


app = Flask(__name__,template_folder = tem_path,static_folder= tem_path)
app.config['SECRET_KEY'] = 'secret!2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///efile.db'
db = SQLAlchemy(app)

class User(db.Model):
        '''
        '''
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String)
        email = db.Column(db.String)
        password = db.Column(db.String)
        authenticated = db.Column(db.Boolean, default=False)
        #friend = relationship('Friend')
        #messaages = relationship('Message')
        def is_active(self):
                 """True, as all users are active."""
                 return True

        def get_id(self):
                """Return the email address to satisfy Flask-Login's requirements."""
                return self.id

        def is_authenticated(self):
                return self.authenticated
                 
                

        def is_anonymous(self):
                 return False
        def __str__(self):
                return self.name
        def __repr__(self):
                return self.name

class Friends(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer ,db.ForeignKey(User.id))
        Friends = db.Column(db.Integer,db.ForeignKey(User.id))
        def __str__(self):
                return self.user_id
        def __repr__(self):
                return self.user_id




class Message(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        sender = db.Column(db.Integer,db.ForeignKey(User.id))
        reciver = db.Column(db.Integer,db.ForeignKey(User.id))
        message = db.Column(db.Text)
        def __repr__(self):
                return self.message
                
class Tokenlist(db.Model):
        token = db.Column(db.String ,primary_key=True)
        user_id =db.Column(db.Integer)
        user_name = db.Column(db.String)

#db.create_all()
#db.session.commit()
def token_validator(token):
        token = Tokenlist.query.filter_by(token=token).first()
        if token != None :
                return True
        return False

def token_grnerator(user):
        word = user.name+user.password
        token = hashlib.sha224(word.encode('ascii')).hexdigest()
        object_token= Tokenlist(token=token,user_id = user.id,user_name=user.name)
        db.session.add(object_token)
        db.session.commit()
        return token
def token_distroyer(token):
        token = Tokenlist.query.filter_by(token=token).first()
        if token != None :
                db.session.delete(token)
                db.session.commit()
                return True
        return False
def token_to_userid(token):
        token = Tokenlist.query.filter_by(token=token).first()
        return token.user_id
def friendid_to_friend(friends_id):
        friends =[]
        for friend in friends_id:
                user= User.query.filter_by(id=friend.Friends)
                friends.append(user)
        return friends
        


        

        




@app.route('/')
def home():
        user_token= request.cookies.get('token')
        if token_validator(user_token):
                return redirect('friends')
        else:
                return render_template('index.html')


                
@app.route('/login',methods=["POST"])
def user_login_post():
        user_name= request.form.get('uname')
        userpassword = request.form.get('psw')
        users = User.query.filter_by(name=user_name).all()
        for single in users:
                if single.password==userpassword:
                        responce = make_response(redirect('/friends'))
                        token = token_grnerator(single)
                        responce.set_cookie('token',token)
                        return responce
        return redirect('/')


@app.route('/friends')
def friends():
        token = request.cookies.get('token')
        if token_validator(token):
                id = token_to_userid(token)
                users_friends = Friends.query.filter_by(user_id=id)
                friend_list = friendid_to_friend(users_friends)
                return render_template('friend.html',friend_list =friend_list)

        else :
                return("not log in ")
@app.route('/logout')
def logout_get():
        token = request.cookies.get('token')
        if token_distroyer(token):
                return(" token vanished")
        return ("somthing wrong happend")
        




                
         



















if __name__ == '__main__':
    app.run(debug=True, port = 4000)