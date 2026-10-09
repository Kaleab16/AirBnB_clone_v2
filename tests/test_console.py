#!/usr/bin/python3
"""Unittests for the HBNB console"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage

DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


def run(line):
    """Run a console command and return what it printed"""
    with patch("sys.stdout", new=StringIO()) as out:
        HBNBCommand().onecmd(line)
    return out.getvalue().strip()


class TestConsoleBasics(unittest.TestCase):
    """Commands that behave the same with both storage engines"""

    def test_prompt(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        self.assertEqual("", run(""))

    def test_quit(self):
        with patch("sys.stdout", new=StringIO()):
            self.assertRaises(SystemExit, HBNBCommand().onecmd, "quit")

    def test_EOF(self):
        with patch("sys.stdout", new=StringIO()):
            self.assertRaises(SystemExit, HBNBCommand().onecmd, "EOF")

    def test_create_missing_class(self):
        self.assertEqual("** class name missing **", run("create"))

    def test_create_invalid_class(self):
        self.assertEqual("** class doesn't exist **", run("create MyModel"))

    def test_show_missing_class(self):
        self.assertEqual("** class name missing **", run("show"))

    def test_show_invalid_class(self):
        self.assertEqual("** class doesn't exist **", run("show MyModel"))

    def test_show_missing_id(self):
        self.assertEqual("** instance id missing **", run("show User"))

    def test_destroy_missing_class(self):
        self.assertEqual("** class name missing **", run("destroy"))

    def test_destroy_invalid_class(self):
        self.assertEqual("** class doesn't exist **", run("destroy MyModel"))

    def test_all_invalid_class(self):
        self.assertEqual("** class doesn't exist **", run("all MyModel"))

    def test_update_missing_class(self):
        self.assertEqual("** class name missing **", run("update"))


@unittest.skipIf(DB, "FileStorage only")
class TestConsoleFileStorage(unittest.TestCase):
    """create/show/destroy checked against FileStorage"""

    def test_create_state_with_param(self):
        new_id = run('create State name="California"')
        key = "State.{}".format(new_id)
        self.assertIn(key, storage.all())
        self.assertEqual("California", storage.all()[key].name)

    def test_create_underscore_param(self):
        new_id = run('create State name="New_York"')
        self.assertEqual("New York",
                         storage.all()["State." + new_id].name)

    def test_show_after_create(self):
        new_id = run("create User")
        self.assertIn(new_id, run("show User {}".format(new_id)))

    def test_destroy_after_create(self):
        new_id = run("create User")
        run("destroy User {}".format(new_id))
        self.assertNotIn("User." + new_id, storage.all())


    def test_create_place_numeric_edge_values(self):
        """Test quoted values, zero, negative integers, and floats."""
        command = (
            'create Place city_id="test_city" user_id="test_user" '
            'name="My_Little_House" description="A small test house" '
            'number_rooms=2 number_bathrooms=0 max_guest=-3 '
            'price_by_night=100 latitude=-120.12 longitude=0.41921928'
        )
        new_id = run(command)
        obj = storage.all()["Place." + new_id]

        self.assertEqual("test city", obj.city_id)
        self.assertEqual("test user", obj.user_id)
        self.assertEqual("My Little House", obj.name)
        self.assertEqual("A small test house", obj.description)
        self.assertEqual(2, obj.number_rooms)
        self.assertEqual(0, obj.number_bathrooms)
        self.assertEqual(-3, obj.max_guest)
        self.assertEqual(100, obj.price_by_night)
        self.assertEqual(-120.12, obj.latitude)
        self.assertEqual(0.41921928, obj.longitude)


@unittest.skipIf(not DB, "DBStorage only")
class TestConsoleDBStorage(unittest.TestCase):
    """create checked directly against MySQL (not through SQLAlchemy)"""

    def setUp(self):
        storage.reload()
        import MySQLdb
        self.conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB"))

    def tearDown(self):
        self.conn.close()

    def count_states(self):
        self.conn.commit()  # end the snapshot so we see fresh rows
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM states")
        n = cur.fetchone()[0]
        cur.close()
        return n

    def test_create_state_adds_row(self):
        before = self.count_states()
        run('create State name="California"')
        self.assertEqual(before + 1, self.count_states())
