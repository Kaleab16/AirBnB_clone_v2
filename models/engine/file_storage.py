#!/usr/bin/python3
"""Module for FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to JSON file and deserializes back."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects, optionally filtered by cls."""
        if cls is not None:
            if isinstance(cls, str):
                cls_dict = {}
                for k, v in FileStorage.__objects.items():
                    if v.__class__.__name__ == cls:
                        cls_dict[k] = v
                return cls_dict
            else:
                cls_dict = {}
                for k, v in FileStorage.__objects.items():
                    if isinstance(v, cls):
                        cls_dict[k] = v
                return cls_dict
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                json_objects = json.load(f)
            for key, val in json_objects.items():
                class_name = val.get("__class__")
                if class_name in classes:
                    FileStorage.__objects[key] = classes[class_name](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Calls reload() method for deserializing JSON file to objects."""
        self.reload()
