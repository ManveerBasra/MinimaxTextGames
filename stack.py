""" implement stack ADT

Taken from lecture examples
"""
from typing import Any


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def __str__(self) -> str:
        """ Return a string representation of self

        >>> s = Stack()
        >>> s.add(5)
        >>> print(s)
        [5]
        """
        return str(self._contains)

    def __eq__(self, other: Any) -> bool:
        """ Return whether self is equivalent to other

        >>> s1 = Stack()
        >>> s2 = Stack()
        >>> s2.add(5)
        >>> s1 == s1
        True
        >>> s1 == s2
        False
        >>> s2 == 5
        False
        """
        return type(self) == type(other) and self._contains == other._contains

    def add(self, obj: object) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0
