"""
This discoverer is meant to discover flakes from primitive objects such as lists and dict and the most basic ones
"""
from typing import List

from protoflake.descriptorbuilder import DescriptorBuilder
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.flakediscoverer import FlakeDiscoverer


class ListDiscoverer(FlakeDiscoverer):

    def __init__(self, data):
        self.data = data

    def discover(self) -> List[FlakeDescriptor]:
        builder = DescriptorBuilder()
        return [builder.build_flake_descriptor(data) for data in self.data]
