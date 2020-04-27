"""
Descriptors hold the data used to build flakes from proto

proto are classes / blueprints
flakes are instances / data holder

descriptors hold the data used to create a flake
"""
from typing import List
from typing import Any
from dataclasses import dataclass
import os

from flakedescriptor import FlakeDescriptor
from attributedescriptor import AttributeDescriptor

from flakeprovider import FlakeProvider
from sourcedescriptor import SourceDescriptor


@dataclass
class FileSourceDescriptor(SourceDescriptor):
    """A source descriptor that indicates the source is a file"""
    full_path: str

    @property
    def file_name(self):
        return os.path.basename(self.full_path)

    @property
    def dir_name(self):
        return os.path.dirname(self.full_path)

    @property
    def file_extension(self):
        return self.file_name.rsplit('.', 1)[1]


@dataclass
class CodeSourceDescriptor(SourceDescriptor):
    """A source descriptor which is meant to be coming from a direct call from the code
    For example: during tests
    """
    hint: str


@dataclass
class PrimitiveAttributeDescriptor(AttributeDescriptor):
    """An attribute which is of primitive type, such as string, int, float, etc..."""

    def get_primitive_value(self, flake_provider: FlakeProvider):
        return self.value

    type: str
    _value: Any

    @property
    def value(self):
        return self._value


@dataclass
class ReferenceAttributeDescriptor(AttributeDescriptor):
    """An attribute which is a reference to another flake."""

    def get_primitive_value(self, flake_provider: FlakeProvider):
        return flake_provider.get_ref(self.reference_flake_id)

    reference_proto_name: str
    reference_flake_id: str


@dataclass
class ListAttributeDescriptor(AttributeDescriptor):
    """An attribute that holds a list of other attributes"""

    def get_primitive_value(self, flake_provider: FlakeProvider):
        return list(map(lambda descriptor: descriptor.get_primitive_value(flake_provider), self.value))

    value: List[AttributeDescriptor]


@dataclass
class NestedFlakeDescriptor(AttributeDescriptor):
    """An attribute which states we should create a new flake and use it as a reference in this object"""

    def get_primitive_value(self, flake_provider: FlakeProvider):
        return flake_provider.get_new(self.nested_descriptor)

    nested_descriptor: FlakeDescriptor
