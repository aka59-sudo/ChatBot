# models.py
import flask_sqlalchemy
from app import db


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Text)
    message = db.Column(db.Text)
    
    
    def __init__(self, a, b):
        self.userID = a
        self.message = b
        
    def __repr__(self):
        return '<The message is: %s>' % self.message

