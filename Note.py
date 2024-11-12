from datetime import datetime
from flask_login import current_user

from config import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, nullable=False)

    def edit(self, title, text):
        self.title = title
        self.text = text
        self.date = datetime.utcnow()

    def __repr__(self):
        return '<Note %r>' % self.id