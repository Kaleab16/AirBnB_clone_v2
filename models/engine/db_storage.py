#!/usr/bin/python3
"""Database storage engine"""
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
    """Manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine from environment variables"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dict of objects, optionally filtered by class"""
        classes = [State, City, User, Place, Review, Amenity]
        if cls is not None:
            if isinstance(cls, str):
                cls = {c.__name__: c for c in classes}.get(cls)
            classes = [cls] if cls else []
        result = {}
        for c in classes:
            for obj in self.__session.query(c).all():
                result["{}.{}".format(type(obj).__name__, obj.id)] = obj
        return result

    def new(self, obj):
        """Add an object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commit the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and a new thread-safe session"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Close the session"""
        self.__session.remove()
