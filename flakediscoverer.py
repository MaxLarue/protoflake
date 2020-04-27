"""
Interface implemented by objects which are able to retrieve flake descriptors through various means
"""
from abc import ABC
from abc import abstractmethod
from typing import List

from flakedescriptor import FlakeDescriptor


class FlakeDiscoverer(ABC):

    @abstractmethod
    def discover(self) -> List[FlakeDescriptor]:
        """Runs the discoverer and return the list of flake descriptor which where found"""
