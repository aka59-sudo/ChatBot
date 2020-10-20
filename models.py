# models.py
import flask_sqlalchemy
from app import db


class newChats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Text)
    message = db.Column(db.Text)
    profilePic = db.Column(db.Text)
    
    
    def __init__(self, a, b, c):
        self.userID = a
        self.message = b
        self.profilePic = c
        
    def __repr__(self):
        return '<The message is: %s>' % self.message

