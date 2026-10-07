#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

CLASSES = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone project."""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn't execute anything."""
        pass

    def do_create(self, arg):
        """Creates a new instance of a class, saves it and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in CLASSES:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)
            if not key or not value:
                continue
            if (value.startswith('"') and value.endswith('"')
                    and len(value) >= 2):
                val_str = value[1:-1]
                val_str = val_str.replace('\\"', '"').replace('_', ' ')
                kwargs[key] = val_str
            elif "." in value:
                try:
                    kwargs[key] = float(value)
                except ValueError:
                    continue
            else:
                try:
                    kwargs[key] = int(value)
                except ValueError:
                    continue

        new_instance = CLASSES[class_name](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints string representation of an instance based on class/id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        all_objects = storage.all()
        if key not in all_objects:
            print("** no instance found **")
        else:
            print(all_objects[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        all_objects = storage.all()
        if key not in all_objects:
            print("** no instance found **")
        else:
            del all_objects[key]
            storage.save()

    def do_all(self, arg):
        """Prints string representations of all instances or of a class."""
        args = shlex.split(arg)
        all_objects = storage.all()
        obj_list = []

        if len(args) > 0:
            if args[0] not in CLASSES:
                print("** class doesn't exist **")
                return
            for key, obj in all_objects.items():
                if key.startswith(args[0] + "."):
                    obj_list.append(str(obj))
        else:
            for obj in all_objects.values():
                obj_list.append(str(obj))

        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on class name and id."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        all_objects = storage.all()
        if key not in all_objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_val = args[3]

        if attr_name in ["id", "created_at", "updated_at"]:
            return

        obj = all_objects[key]

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                cast_val = attr_type(attr_val)
            except (ValueError, TypeError):
                cast_val = attr_val
        else:
            if attr_val.isdigit():
                cast_val = int(attr_val)
            else:
                try:
                    cast_val = float(attr_val)
                except ValueError:
                    cast_val = attr_val

        setattr(obj, attr_name, cast_val)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
