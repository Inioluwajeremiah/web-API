import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    useremail = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, onupdate=datetime.now())

    scholarshipPost = db.relationship('ScholarshipPost', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class ScholarshipPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ga = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #  ra = db.Column(db.Text, nullable = True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    institution = db.Column(db.Text, nullable=False)
    faculty = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=True)
    course = db.Column(db.Text, nullable=True)
    level = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Text, nullable=False)
    appfee = db.Column(db.Text, nullable=False)
    fund_type = db.Column(db.Text, nullable=False)
    app_url = db.Column(db.Text, nullable=False)
    app_short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, onupdate=datetime.now())

    #  waived = db.Column(db.Text, nullable = True)

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))

        link = self.query.filter_by(app_short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return 'ScholarshipPost>>> {self.url}'
