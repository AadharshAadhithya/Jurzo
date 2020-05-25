from Jurzo import db,login_manager
from datetime import datetime
from flask_login import UserMixin




@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))



class User(db.Model,UserMixin):
    email=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(),nullable=False,unique=True)

    id=db.Column(db.Integer,primary_key=True)
    password=db.Column(db.String(60),nullable=False)
    page=db.relationship('Page',backref= 'owner' , lazy=True)



    def __repr__(self):
        return "user_id : {} , username : {} ,email : {}".format(self.id,self.username,self.email)






class Page(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default= datetime.utcnow)
    name=db.Column(db.Text)
    pet_name= db.Column(db.Text)
    phone_num= db.Column(db.Text)
    address= db.Column(db.Text)
    mail = db.Column(db.Text)
    birthday = db.Column(db.Text)
    nick_name= db.Column(db.Text)
    Quote = db.Column(db.Text)
    Songs = db.Column(db.Text)
    likes = db.Column(db.Text)
    hates = db.Column(db.Text)
    what_us = db.Column(db.Text)
    lastd = db.Column(db.Text)

    def __repr(self):
        return "user_id: {}".format(self.user_id , self.owner)

