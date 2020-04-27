from abc import ABC
from abc import abstractmethod

from protoflake.flakeprovider import FlakeProvider


class AttributeDescriptor(ABC):
    """Attributes used to create a flake"""
    name: str

    @abstractmethod
    def get_primitive_value(self, flake_provider: FlakeProvider):
        """Returns the real attribute as described by this descriptor
        Potentially creating new/retrieving existing flakes.
        """