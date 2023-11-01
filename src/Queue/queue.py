""" File containing the Queue class """

import queue

class Queue:
    """ The Queue class that acts as a wrapper around the queue library
    Exposes three methods:
    get: for getting the next item in the queue
    add: adding a item to the back of the queue
    is_empty: for getting whether the queue is empty or not
    done: for letting the queue know that a task is finished
    """
    def __init__(self):
        self.queue = queue.Queue()

    def get(self) -> any:
        """ Gets the next element of the queue """
        return self.queue.get()

    def add(self, item) -> None:
        """ Adds a item to the queue """
        self.queue.put(item)

    def is_empty(self) -> bool:
        """ Returns true if the queue is empty, otherwise false """
        return self.queue.empty()

    def done(self) -> None:
        """ Lets the Queue know that a task is finished """
        self.queue.task_done()
