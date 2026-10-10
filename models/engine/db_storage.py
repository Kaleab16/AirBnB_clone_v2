#!/usr/bin/python3
"""Database storage engine for HBNB."""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Manages HBNB objects in a MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the MySQL database engine."""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        url = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database
        )

        self.__engine = create_engine(url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all objects, optionally filtered by class."""
        classes = [State, City, User, Place, Review, Amenity]

        if cls is not None:
            if isinstance(cls, str):
                cls = {
                    model.__name__: model for model in classes
                }.get(cls)

            classes = [cls] if cls in classes else []

        objects = {}

        for model in classes:
            for obj in self.__session.query(model).all():
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """Add an object to the current session."""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create database tables and initialize a scoped session."""
        Base.metadata.create_all(self.__engine)

        factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(factory)

    def close(self):
        """Remove the current scoped session."""
        if self.__session is not None:
            self.__session.remove()
