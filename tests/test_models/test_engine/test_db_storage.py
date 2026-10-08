#!/usr/bin/python3
"""Unittests for DBStorage"""
import os
import unittest
from models import storage
from models.state import State

DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


@unittest.skipIf(not DB, "DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Validate DBStorage against the real database"""

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
        self.conn.commit()
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM states")
        n = cur.fetchone()[0]
        cur.close()
        return n

    def test_all_returns_dict(self):
        self.assertIsInstance(storage.all(), dict)

    def test_all_with_class(self):
        state = State(name="Texas")
        state.save()
        self.assertIn("State.{}".format(state.id), storage.all(State))

    def test_new_save_adds_row(self):
        before = self.count_states()
        state = State(name="Nevada")
        storage.new(state)
        storage.save()
        self.assertEqual(before + 1, self.count_states())

    def test_delete_removes_row(self):
        state = State(name="Utah")
        state.save()
        before = self.count_states()
        storage.delete(state)
        storage.save()
        self.assertEqual(before - 1, self.count_states())

    def test_reload_keeps_working(self):
        storage.reload()
        self.assertIsInstance(storage.all(), dict)
