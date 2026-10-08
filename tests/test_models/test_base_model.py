#!/usr/bin/python3
"""Unittest for BaseModel class."""
import os
import unittest
from datetime import datetime
from models.base_model import BaseModel


class test_basemodel(unittest.TestCase):
    """Test BaseModel class."""

    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.value = BaseModel

    @classmethod
    def tearDownClass(cls):
        """Tear down test class."""
        try:
            os.remove('file.json')
        except OSError:
            pass

    def test_default(self):
        """Test default instance."""
        i = self.value()
        self.assertEqual(type(i), self.value)
        self.assertIsNotNone(i.id)
        self.assertIsNotNone(i.created_at)
        self.assertIsNotNone(i.updated_at)

    def test_kwargs(self):
        """Test instance creation with kwargs."""
        i = self.value()
        copy = i.to_dict()
        new = self.value(**copy)
        self.assertFalse(i is new)

    def test_kwargs_int(self):
        """Test invalid integer key."""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            self.value(**copy)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        'FileStorage-specific test'
    )
    def test_save(self):
        """Test save."""
        i = self.value()
        i.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_str(self):
        """Test string representation."""
        i = self.value()
        string = '[{}] ({}) {}'.format(
            type(i).__name__, i.id, i.__dict__
        )
        self.assertEqual(str(i), string)

    def test_todict(self):
        """Test to_dict."""
        i = self.value()
        new = i.to_dict()
        self.assertEqual(new['__class__'], type(i).__name__)
        self.assertEqual(new['id'], i.id)
        self.assertEqual(new['created_at'], i.created_at.isoformat())
        self.assertEqual(new['updated_at'], i.updated_at.isoformat())

    def test_kwargs_none(self):
        """Test None as key."""
        i = self.value()
        copy = i.to_dict()
        copy.update({None: 2})
        with self.assertRaises(TypeError):
            self.value(**copy)

    def test_kwargs_one(self):
        """Test invalid keyword."""
        with self.assertRaises(KeyError):
            self.value(Name='test')

    def test_id_type(self):
        """Test id type."""
        i = self.value()
        self.assertEqual(type(i.id), str)

    def test_created_at_type(self):
        """Test created_at type."""
        i = self.value()
        self.assertEqual(type(i.created_at), datetime)

    def test_updated_at_type(self):
        """Test updated_at type."""
        i = self.value()
        self.assertEqual(type(i.updated_at), datetime)

    def test_updated_at(self):
        """Test updated_at differs from created_at."""
        i = self.value()
        new = self.value(**i.to_dict())
        self.assertNotEqual(new.created_at, new.updated_at)
