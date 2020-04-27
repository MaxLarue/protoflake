from dataclasses import dataclass
from typing import Dict

from sourcedescriptor import SourceDescriptor
from attributedescriptor import AttributeDescriptor


@dataclass
class FlakeDescriptor(object):
    """Describes the data that should be used to create a flake"""
    proto_name: str
    id: str
    attrs: Dict[str, AttributeDescriptor]
    source: SourceDescriptor

    @property
    def proto_class(self):
        return self.proto_name.rsplit('.', 1)[1]

    @property
    def proto_module(self):
        return self.proto_name.rsplit('.', 1)[1]