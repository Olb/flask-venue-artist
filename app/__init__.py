#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
import forms
from forms import ShowForm, ArtistForm, VenueForm

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('app.config')

moment = Moment(app)
import models
from models import Venue, Show, Artist, db

migrate = Migrate(app, models.db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    unique_city_states = Venue.query.with_entities(
        Venue.city, Venue.state).distinct().all()
    data = []
    for cs in unique_city_states:
        venues = Venue.query.filter_by(city=cs[0], state=cs[1]).all()
        data.append({'city': cs[0], 'state': cs[1], 'venues': venues})
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    venues = Venue.query.filter(func.lower(Venue.name).contains(
        request.form.get('search_term').lower())).all()
    response = {
        "count": len(venues),
        "data": venues
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    data = request.form
    venues = Venue.query.filter_by(name=data['name']).all()
    if len(venues) > 0:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' already exists!')
        return render_template('pages/home.html')

    try:
        venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'],
                      phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue was successfully deleted!')
    except:
        db.session.rollback()
        flash('Venue failed to delete!')
    finally:
        db.session.close()

    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    artists = Artist.query.filter(func.lower(Artist.name).contains(
        request.form.get('search_term').lower())).all()

    response = {
        "count": len(artists),
        "data": artists
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        data = request.form
        artist = Artist.query.get(artist_id)
        artist.name = data['name']
        artist.city = data['city']
        artist.state = data['state']
        artist.genres = [data['genres']]
        artist.phone = data['phone']
        artist.facebook_link = data['facebook_link']
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        data = request.form
        venue = Venue.query.get(venue_id)
        venue.name = data['name']
        venue.city = data['city']
        venue.state = data['state']
        venue.genres = [data['genres']]
        venue.phone = data['phone']
        venue.address = data['address']
        venue.facebook_link = data['facebook_link']
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    data = request.form
    artist = Artist.query.filter_by(name=data['name']).all()
    if len(artist) > 0:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' already exists!')
        return render_template('pages/home.html')

    try:
        data = request.form
        artist = Artist(name=data['name'], city=data['city'], state=data['state'],
                        phone=data['phone'], genres=[data['genres']], facebook_link=data['facebook_link'])
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        data = request.form
        show = Show(artist_id=data['artist_id'],
                    venue_id=data['venue_id'], start_time=data['start_time'])
        db.session.add(show)
        db.session.commit()
        flash('The show was successfully listed!')
    except:
        flash('An error occurred. The show could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
