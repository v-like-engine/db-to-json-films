import json
from sqlalchemy.orm.exc import NoResultFound
from film_database_creation import FilmTitles, FilmRatings, FilmLinks, FilmLabels, start_basic_session, close_session


def get_film_details(title):
    session = start_basic_session()
    try:
        film = session.query(FilmTitles).filter(FilmTitles.title == title).one()
        rating = session.query(FilmRatings).filter(FilmRatings.film_id == film.film_id).one()
        links = session.query(FilmLinks).filter(FilmLinks.film_id == film.film_id).one()
        labels = session.query(FilmLabels.label).join(FilmLabels.label).filter(FilmLabels.film_id == film.film_id).all()

        # create a dictionary containing the film details
        film_details = {
            'filmTitle': film.title,
            'filmDescription': film.description,
            'filmRating': rating.rating,
            'filmIMBdRating': rating.imbd_rating,
            'filmKinopoiskRating': rating.kinopoisk_rating,
            'filmLabels': [label[0] for label in labels],
            'filmTrailerLink': links.trailer_link,
            'filmPosterLink': links.poster_link,
            'filmStreamLink': links.stream_link
        }
        return film_details
    except NoResultFound:
        return None
    finally:
        close_session(session)


def get_film_titles():
    session = start_basic_session()
    film_list = []
    for film in session.query(FilmTitles).all():
        film_list.append(film)
    return film_list


def get_json(title):
    film_details = get_film_details('The Godfather')
    if film_details:
        # do something with the film details, such as print them as JSON
        return json.dumps(film_details)
    else:
        return None

