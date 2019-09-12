from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import Flask
from app import app
from datetime import datetime

db = SQLAlchemy(app)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.Column(db.ARRAY(db.String()))

    @property
    def past_shows(self):
        now = datetime.now()
        past_shows = [x for x in self.shows if datetime.strptime(
            x.start_time, '%Y-%m-%d %H:%M:%S') < now]
        return past_shows

    @property
    def upcoming_shows(self):
        now = datetime.now()
        future_shows = [x for x in self.shows if datetime.strptime(
            x.start_time, '%Y-%m-%d %H:%M:%S') > now]
        return future_shows

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.Column(db.ARRAY(db.String()))

    @property
    def past_shows(self):
        now = datetime.now()
        past_shows = [x for x in self.shows if datetime.strptime(
            x.start_time, '%Y-%m-%d %H:%M:%S') < now]
        return past_shows

    @property
    def upcoming_shows(self):
        now = datetime.now()
        future_shows = [x for x in self.shows if datetime.strptime(
            x.start_time, '%Y-%m-%d %H:%M:%S') > now]
        return future_shows

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    start_time = db.Column(db.String(), nullable=False)

    @property
    def artist_name(self):
        return Artist.query.get(self.artist_id).name

    @property
    def artist_image_link(self):
        return Artist.query.get(self.artist_id).image_link

    @property
    def venue_name(self):
        return Venue.query.get(self.venue_id).name

    @property
    def venue_image_link(self):
        return Venue.query.get(self.venue_id).image_link
