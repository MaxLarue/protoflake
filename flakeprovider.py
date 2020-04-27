"""
Interface implemented by classes which provide for flakes
either return a ref to them, or create them
"""
from abc import ABC
from abc import abstractmethod


class FlakeProvider(ABC):

    @abstractmethod
    def get_ref(self, flake_id):
        """Given a flake id, return the already existing flake"""

    @abstractmethod
    def get_new(self, flake_descriptor):
        """Given a flake descriptor, build then return it"""
