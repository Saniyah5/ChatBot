# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False)

# # class Message(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# #     role = db.Column(db.String(10), nullable=False)  # "user" or "assistant"
# #     content = db.Column(db.Text, nullable=False)

# class Message(db.Model):
#     __tablename__ = 'message'
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     role = db.Column(db.String(10))
#     content = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

class Message(db.Model):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}  # 🔧 This line fixes the error

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
