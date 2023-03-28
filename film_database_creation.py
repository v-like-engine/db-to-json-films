from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


# define the tables
class FilmTitles(Base):
    __tablename__ = 'FilmTitles'
    film_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)


class FilmRatings(Base):
    __tablename__ = 'FilmRatings'
    film_id = Column(Integer, ForeignKey('FilmTitles.film_id'), primary_key=True)
    rating = Column(Float)
    imbd_rating = Column(Float)
    kinopoisk_rating = Column(Float)


class FilmLinks(Base):
    __tablename__ = 'FilmLinks'
    film_id = Column(Integer, ForeignKey('FilmTitles.film_id'), primary_key=True)
    trailer_link = Column(String)
    poster_link = Column(String)
    stream_link = Column(String)


class Labels(Base):
    __tablename__ = 'Labels'
    label_id = Column(Integer, primary_key=True)
    label = Column(String)


class FilmLabels(Base):
    __tablename__ = 'FilmLabels'
    film_id = Column(Integer, ForeignKey('FilmTitles.film_id'), primary_key=True)
    label_id = Column(Integer, ForeignKey('Labels.label_id'), primary_key=True)
    film = relationship(FilmTitles, backref="labels")
    label = relationship(Labels)


class FilmDubbings(Base):
    __tablename__ = 'FilmDubbings'
    film_id = Column(Integer, ForeignKey('FilmTitles.film_id'), primary_key=True)
    dubbings_reference = Column(String)


def create_engine_instance():
    # create engine and connect to the database
    engine_instance = create_engine('sqlite:///films.db')
    return engine_instance


def create_tables(engine_entity, base):
    # create the tables
    base.metadata.create_all(engine_entity)


def create_session(engine_entity):
    # create a session
    session = (sessionmaker(bind=engine_entity))()
    return session


def add_data(session_instance):
    # add data to the tables
    film1 = FilmTitles(title='The Godfather', description='An organized crime movie')
    film2 = FilmTitles(title='The Shawshank Redemption', description='A drama movie')
    film3 = FilmTitles(title='The Dark Knight', description='A superhero movie')
    session_instance.add_all([film1, film2, film3])

    rating1 = FilmRatings(film_id=1, rating=4.5, imbd_rating=9.2, kinopoisk_rating=8.5)
    rating2 = FilmRatings(film_id=2, rating=4.2, imbd_rating=9.3, kinopoisk_rating=8.7)
    rating3 = FilmRatings(film_id=3, rating=4.8, imbd_rating=9.0, kinopoisk_rating=8.9)
    session_instance.add_all([rating1, rating2, rating3])

    link1 = FilmLinks(film_id=1, trailer_link='https://www.youtube.com/watch?v=sY1S34973zA', poster_link='https://www.imdb.com/title/tt0068646/mediaviewer/rm2124448769/', stream_link='rtmp://rtmp.klpkw.one/live/workstation')
    link2 = FilmLinks(film_id=2, trailer_link='https://www.youtube.com/watch?v=6hB3S9bIaco', poster_link='https://www.imdb.com/title/tt0111161/mediaviewer/rm1042539264/', stream_link='rtmp://rtmp.klpkw.one/live/workstation')
    link3 = FilmLinks(film_id=3, trailer_link='https://www.youtube.com/watch?v=EXeTwQWrcwY', poster_link='https://www.imdb.com/title/tt0468569/mediaviewer/rm1361131520/', stream_link='rtmp://rtmp.klpkw.one/live/workstation')
    session_instance.add_all([link1, link2, link3])

    label1 = Labels(label='Crime')
    label2 = Labels(label='Drama')
    label3 = Labels(label='Superhero')
    session_instance.add_all([label1, label2, label3])

    film_label1 = FilmLabels(film_id=1, label_id=1)
    film_label2 = FilmLabels(film_id=1, label_id=2)
    film_label3 = FilmLabels(film_id=2, label_id=2)
    film_label4 = FilmLabels(film_id=3, label_id=3)
    session_instance.add_all([film_label1, film_label2, film_label3, film_label4])

    dubbing1 = FilmDubbings(film_id=1, dubbings_reference='https://www.imdb.com/title/tt0068646/parentalguide')
    dubbing2 = FilmDubbings(film_id=2, dubbings_reference='https://www.imdb.com/title/tt0111161/parentalguide')
    dubbing3 = FilmDubbings(film_id=3, dubbings_reference='https://www.imdb.com/title/tt0468569/parentalguide')
    session_instance.add_all([dubbing1, dubbing2, dubbing3])

    # commit the session_instance
    session_instance.commit()


def test_query(session):

    # query the database
    print('All films:')
    for film in session.query(FilmTitles).all():
        print(film.title)

    print('\nAll crime movies:')
    for film in session.query(FilmTitles).join(FilmLabels).join(Labels).filter(Labels.label == 'Crime').all():
        print(film.title)

    print('\nThe rating of The Godfather:')
    for rating in session.query(FilmRatings).filter_by(film_id=1).all():
        print(rating.rating)

    print('\nThe dubbings reference of The Dark Knight:')
    for dubbing in session.query(FilmDubbings).filter_by(film_id=3).all():
        print(dubbing.dubbings_reference)


def close_session(session):
    # close the session
    session.close()


def basic_create(perform_test_query=False):
    engine = create_engine_instance()
    create_tables(engine, Base)
    session = create_session(engine)
    add_data(session)
    if perform_test_query:
        test_query(session)
    close_session(session)


def start_basic_session():
    engine = create_engine_instance()
    session = create_session(engine)
    return session
