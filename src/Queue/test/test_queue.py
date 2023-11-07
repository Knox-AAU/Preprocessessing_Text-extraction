""" Module providing unit tests for the Queue class """
import unittest

from Queue.queue import Queue

class TestCase(unittest.TestCase):
    """ Testing the Queue"""

    def test_can_add(self):
        """ Test if the adding of items to the queue works """
        # Arrange
        q = Queue()
        # Act
        q.add('shouldGetThis')
        # Assert
        self.assertEqual(q.get(), 'shouldGetThis')

    def test_can_get(self):
        """ Testing if the retrieval of items from the queue works """
        # Arrange
        q = Queue()
        # Act
        q.add('removeThis')
        item = q.get()
        # Assert
        self.assertEqual(item, 'removeThis')

    def test_is_empty(self):
        """ Testing that the queue is actually empty when the bool shows it """
        # Arrange
        q = Queue()
        # Act
        q.add('remove')
        q.get()
        # Assert
        self.assertTrue(q.is_empty())