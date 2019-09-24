from blog import db, login_manager
# from flask_mongoengien import BaseQueryQuerySetSet
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_email): 
    return User.objects.get(email=user_email)

class User(db.Document, UserMixin):
    # query_class = UserModel
    email = db.StringField(max_length=30,required=True, primary_key=True)
    username = db.StringField(max_length=20,required=True)
    image_file = db.StringField(max_length=50,required=True,default='avata.jpg')
    password = db.StringField(max_length=100,required=True)
    
    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.objects.get(email=user_id)


    def __repr__(self):
        return f"User('{self.username}','{self.password}','{self.image_file}')"

    # def get_email(self, email):
    #     return self.filter(self.get.email == email).first()

 
class Post(db.Document):
    title = db.StringField(max_length=150,required=True)
    date_posted = db.DateTimeField(default = datetime.utcnow())
    content = db.StringField()  
    image_file = db.StringField(max_length=50,required=True,default='post.jpg')
    author = db.ReferenceField(User,required=True)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}','{self.content}')"

class Comment(db.Document):
    post = db.ReferenceField(Post,required=True)
    author = db.ReferenceField(User,required=True)
    content = db.StringField(max_length=150,required=True)
    date_posted = db.DateTimeField(default = datetime.utcnow())