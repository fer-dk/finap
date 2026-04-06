from app import db
from datetime import datetime

class LogModel(db.Model):
    __tablename__="logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)