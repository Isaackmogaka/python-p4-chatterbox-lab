from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import DateTime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(20), default=str(datetime.utcnow()))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, body, username):
        self.body = body
        self.username = username

