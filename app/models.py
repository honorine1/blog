from . import db
from sqlalchemy.sql import func
from . import login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    blog = db.relationship('Blog', backref='users', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    comment = db.relationship('Comment', backref = 'users', lazy = 'dynamic')
    # upvotes = db.relationship('Upvote', backref = 'users', lazy = 'dynamic')
    # downvotes = db.relationship('Downvote', backref = 'users', lazy = 'dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'{self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}' 


class Blog(db.Model):
    '''
    '''
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    # category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment',backref='pitch',lazy='dynamic')
    # upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
    # downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')

    @classmethod
    def get_blogs(cls, id):
        blogs = Blog.query.order_by(blog_id=id).desc().all()
        return blogs

    def __repr__(self):
        return f'Blog {self.description}'

    

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)


    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

class Quotes:
    def __init__(self,author,quote):

        self.author = author
        self.quote = quote


# class Pitch(db.Model):
#     '''
#     '''
#     __tablename__ = 'pitches'

#     id = db.Column(db.Integer, primary_key = True)
#     owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
#     description = db.Column(db.String(), index = True)
#     title = db.Column(db.String())
#     category = db.Column(db.String(255), nullable=False)
#     comments = db.relationship('Comment',backref='pitch',lazy='dynamic')
#     upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
#     downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')

    
   


# class Upvote(db.Model):
#     __tablename__ = 'upvotes'

#     id = db.Column(db.Integer,primary_key=True)
#     upvote = db.Column(db.Integer,default=1)
#     blog_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

#     def save_upvotes(self):
#         db.session.add(self)
#         db.session.commit()


#     def add_upvotes(cls,id):
#         upvote_pitch = Upvote(user = current_user, pitch_id=id)
#         upvote_pitch.save_upvotes()

    
#     @classmethod
#     def get_upvotes(cls,id):
#         upvote = Upvote.query.filter_by(pitch_id=id).all()
#         return upvote

#     @classmethod
#     def get_all_upvotes(cls,pitch_id):
#         upvotes = Upvote.query.order_by('id').all()
#         return upvotes

#     def __repr__(self):
#         return f'{self.user_id}:{self.pitch_id}'



# class Downvote(db.Model):
#     __tablename__ = 'downvotes'

#     id = db.Column(db.Integer,primary_key=True)
#     downvote = db.Column(db.Integer,default=1)
#     pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

#     def save_downvotes(self):
#         db.session.add(self)
#         db.session.commit()


#     def add_downvotes(cls,id):
#         downvote_pitch = Downvote(user = current_user, pitch_id=id)
#         downvote_pitch.save_downvotes()

    
#     @classmethod
#     def get_downvotes(cls,id):
#         downvote = Downvote.query.filter_by(pitch_id=id).all()
#         return downvote

#     @classmethod
#     def get_all_downvotes(cls,pitch_id):
#         downvote = Downvote.query.order_by('id').all()
#         return downvote

#     def __repr__(self):
#         return f'{self.user_id}:{self.pitch_id}'






    