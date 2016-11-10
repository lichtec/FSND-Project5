# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, \
    session as login_session, redirect, url_for, jsonify

from functools import wraps

from sqlalchemy import create_engine, asc, update
from sqlalchemy.orm import sessionmaker

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# json for jsonify
import json

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.records.record_model import Genre, Artist, Record

# Define the blueprint: 'add', set its url prefix: app.url
modificationBase = Blueprint('add', __name__, url_prefix='')

'''
login required decorator
'''


def login_required(f):
    """
    login_required: declorator for requiring a user to be logged in

    Args:

    Returns:
        return a redirect or just returns
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

'''
    set record modification methods
'''


@modificationBase.route('/records/add', methods=['GET', 'POST'])
@login_required
def addRecords():
    """

        addRecords: Add records method. Uses form to create a new record.

        Args: none

        Returns:
            return a redirect when successful
    """
    if request.method == 'POST':
        # Pull the artist id and genre id based on the name to create the
        # record
        artist_id = db.session.query(Artist.id).filter_by(
            artist_name=request.form['artist_Sel']).one()
        genre_id = db.session.query(Genre.id).filter_by(
            genre_name=request.form['genre_Sel']).one()
        if(len(request.form['record_image']) > 0):
            record_image = request.form['record_image']
        else:
            record_image = 'http://placehold.it/800x500'
        if(len(request.form['year']) > 0):
            year = int(request.form['year'])
        else:
            year = 0
        newRecord = Record(
            title=request.form['title'], artist_id=int(artist_id[0]),
            genre_id=genre_id[0], year=year,
            description=request.form['description'],
            record_image=record_image)
        db.session.add(newRecord)
        flash('New Record Successfully Created')
        db.session.commit()
        return redirect('/records')

    # Pull all artists and genres to pass to the add artists html
    artists = db.session.query(Artist).all()
    genres = db.session.query(Genre).all()
    if 'username' not in login_session:
        return render_template("records/add_records.html", artists=artists,
                               genres=genres, loggedIn=False)
    else:
        return render_template("records/add_records.html", artists=artists,
                               genres=genres, loggedIn=True)


@modificationBase.route('/records/<int:record_id>/edit', methods=['GET',
                                                                  'POST']
                        )
@login_required
def editRecords(record_id):
    """

    editRecords: Updates record method. Uses form to update a specified
    record with info from the form.

    Args: record_id

    Returns:
        return a redirect when successful
    """
    # Get the record that needs edited
    record = db.session.query(Record.id, Record.title, Record.year,
                              Record.description, Record.artist_id,
                              Record.record_image, Artist.artist_name,
                              Genre.genre_name).filter_by(id=record_id).\
    outerjoin(Artist).outerjoin(Genre).one()

    if request.method == 'POST':
        editRecord = db.session.query(Record).filter_by(id=record_id).one()
        # test for new values from the form
        if request.form['title']:
            editRecord.title = request.form['title']
        if request.form['artist_Sel']:
            artist_id = db.session.query(Artist.id).filter_by(
                artist_name=request.form['artist_Sel']).one()
            print int(artist_id[0])
            editRecord.artist_id = int(artist_id[0])
        if request.form['genre_Sel']:
            genre_id = db.session.query(Genre.id).filter_by(
                genre_name=request.form['genre_Sel']).one()
            editRecord.genre_id = int(genre_id[0])
        if request.form['year']:
            editRecord.year = int(request.form['year'])
        if request.form['description']:
            editRecord.description = request.form['description']
        if request.form['record_image']:
            editRecord.record_image = request.form['record_image']
        db.session.add(editRecord)
        flash('Updated Record Successfully')
        db.session.commit()
        return redirect('/records')

    # Pull all artists and genres for the edit page
    artists = db.session.query(Artist).all()
    genres = db.session.query(Genre).all()
    if 'username' not in login_session:
        return render_template("/records/edit_record.html",
                               artists=artists, genres=genres, record=record,
                               loggedIn=False)
    else:
        return render_template("/records/edit_record.html", artists=artists,
                               genres=genres, record=record, loggedIn=True)


@modificationBase.route('/records/<int:record_id>/delete', methods=['GET',
                                                                    'POST'])
@login_required
def deleteRecords(record_id):
    """

    delete: Delete record method. Deletes the record.

    Args: record_id

    Returns:
        return a redirect when successful
    """
    # Get the record to delete
    recordToDelete = db.session.query(Record).filter_by(id=record_id).one()
    if request.method == 'POST':
        db.session.delete(recordToDelete)
        flash('Record Successfully Deleted')
        db.session.commit()
        return redirect('/records')

    if 'username' not in login_session:
        return render_template("records/delete_record.html",
                               record=recordToDelete, loggedIn=False)
    else:
        return render_template("records/delete_record.html",
                               record=recordToDelete, loggedIn=True)

'''
    set artist methods
'''


@modificationBase.route('/artists/add', methods=['GET', 'POST'])
@login_required
def addArtist():
    """

    addArtist: Add artist method. Creates new artist

    Args:

    Returns:
        return a redirect when successful
    """
    if request.method == 'POST':
        genre_id = db.session.query(Genre.id).filter_by(
            genre_name=request.form['genre_Sel']).one()
        if(len(request.form['artist_image']) > 0):
            artist_image = request.form['artist_image']
        else:
            artist_image = 'http://placehold.it/800x500'
        newArtist = Artist(artist_name=request.form['artist_name'],
                           genre_id=genre_id[0], artist_image=artist_image)
        db.session.add(newArtist)
        flash('New Artist Successfully Created')
        db.session.commit()
        return redirect('/artists')

    artists = db.session.query(Artist).all()
    genres = db.session.query(Genre).all()
    if 'username' not in login_session:
        return render_template("artists/add_artists.html", artists=artists,
                               genres=genres, loggedIn=False)
    else:
        return render_template("artists/add_artists.html", artists=artists,
                               genres=genres, loggedIn=True)


@modificationBase.route('/artists/<int:artist_id>/edit', methods=['GET',
                                                                  'POST'])
@login_required
def editArtists(artist_id):
    """

        editArtist: Edit artist method. Updates an artist based on info from
        the form

        Args: artist_id

        Returns:
            return a redirect when successful
    """
    editArtist = db.session.query(Artist).filter_by(id=artist_id).one()

    if request.method == 'POST':
        if request.form['artist_name']:
            editArtist.artist_name = request.form['artist_name']
        if request.form['genre_Sel']:
            genre_id = db.session.query(Genre.id).filter_by(
                genre_name=request.form['genre_Sel']).one()
            editArtist.genre_id = genre_id[0]
        if request.form['artist_image']:
            editArtist.artist_image = request.form['artist_image']
        db.session.add(editArtist)
        flash('Updated Artist Successfully')
        db.session.commit()
        return redirect('/artists')

    # Pull genres for edit html
    genres = db.session.query(Genre).all()
    if 'username' not in login_session:
        return render_template("/artists/edit_artist.html", artist=editArtist,
                               genres=genres, loggedIn=False)
    else:
        return render_template("/artists/edit_artist.html", artist=editArtist,
                               genres=genres, loggedIn=True)


@modificationBase.route('/artists/<int:artist_id>/delete', methods=['GET',
                                                                    'POST'])
@login_required
def deleteArtist(artist_id):
    """

        deleteArtist: Delete artist method. Deletes an artist

        Args: artist_id

        Returns:
            return a redirect when successful

    """
    artistToDelete = db.session.query(Artist).filter_by(id=artist_id).one()
    # pull the records of that has this artist to delete as the artist
    relatedRecords = db.session.query(
        Record).filter_by(artist_id=artist_id).all()

    if request.method == 'POST':
        # remove the artist id from the related records
        for record in relatedRecords:
            record.artist_id = None
            db.session.add(record)
        db.session.delete(artistToDelete)
        flash('Artist Successfully Deleted')
        db.session.commit()
        return redirect('/artists')

    if 'username' not in login_session:
        return render_template("/artists/delete_artist.html",
                               artist=artistToDelete, records=relatedRecords,
                               loggedIn=False)
    else:
        return render_template("/artists/delete_artist.html",
                               artist=artistToDelete, records=relatedRecords,
                               loggedIn=True)

'''
    set genre methods
'''


@modificationBase.route('/genres/add', methods=['GET', 'POST'])
@login_required
def addGenre():
    """

        addGenre: Add genre method. Creates new genre

        Args:

        Returns:
            return a redirect when successful
    """
    if request.method == 'POST':
        if(len(request.form['genre_image']) > 0):
            genre_image = request.form['genre_image']
        else:
            genre_image = 'http://placehold.it/800x500'
        newGenre = Genre(genre_name=request.form['genre_name'],
                         description=request.form[
                         'genre_description'], genre_image=genre_image)
        db.session.add(newGenre)
        flash('New Genre Successfully Created')
        db.session.commit()
        return redirect('/genres')

    if 'username' not in login_session:
        return render_template("genres/add_genres.html", loggedIn=False)
    else:
        return render_template("genres/add_genres.html", loggedIn=True)


@modificationBase.route('/genres/<int:genre_id>/edit', methods=['GET', 'POST'])
@login_required
def editGenre(genre_id):
    """

        editGenre: Edit genre method. Updates genre from form info

        Args: genre_id

        Returns:
            return a redirect when successful
    """
    editGenre = db.session.query(Genre).filter_by(id=genre_id).one()

    if request.method == 'POST':
        if(request.form['genre_name']):
            editGenre.genre_name = request.form['genre_name']
        if(request.form['genre_description']):
            editGenre.description = request.form['genre_description']
        if(request.form['genre_image']):
            editGenre.genre_image = request.form['genre_image']
        db.session.add(editGenre)
        flash('Genre Successfully Updated')
        db.session.commit()
        return redirect('/genres')

    if 'username' not in login_session:
        return render_template("genres/edit_genres.html", genre=editGenre,
                               loggedIn=False)
    else:
        return render_template("genres/edit_genres.html", genre=editGenre,
                               loggedIn=True)


@modificationBase.route('/genres/<int:genre_id>/delete', methods=['GET',
                                                                  'POST'])
@login_required
def deleteGenre(genre_id):
    """

        deleteGenre: Delete genre method. Deletes a genre

        Args: genre_id

        Returns:
            return a redirect when successful
    """
    genreToDelete = db.session.query(Genre).filter_by(id=genre_id).one()

    # pull related artists for this genre
    relatedArtists = db.session.query(Artist).filter_by(genre_id=genre_id
                                                       ).all()

    # pull related records for this genre
    relatedRecords = db.session.query(
        Record).filter_by(genre_id=genre_id).all()

    if request.method == 'POST':
        db.session.delete(genreToDelete)
        for artist in relatedArtists:
            artist.genre_id = None
            db.session.add(artist)
        for record in relatedRecords:
            record.genre_id = None
            db.session.add(record)
        flash('Genre Successfully Deleted')
        db.session.commit()
        return redirect('/genres')

    if 'username' not in login_session:
        return render_template("/genres/delete_genres.html",
                               genre=genreToDelete, artists=relatedArtists,
                               records=relatedRecords, loggedIn=False)
    else:
        return render_template("/genres/delete_genres.html",
                               genre=genreToDelete, artists=relatedArtists,
                               records=relatedRecords, loggedIn=True)
