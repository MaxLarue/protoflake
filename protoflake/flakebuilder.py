"""
The flake builder is responsible for building nested flakes, retrieving refs and transforming AttributeDescriptors
into primitive attributes. All this for building complex flakes.
Once flake attributes have been transformed to primitive types, the flake builder will save the new
flake instance inside the flake registry and return it.
"""
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.flakefactory import FlakeFactory
from protoflake.flakeregistry import FlakeRegistry
from protoflake.flakeprovider import FlakeProvider
from protoflake.protoregistry import ProtoRegistry


class FlakeBuilder(FlakeProvider):

    def __init__(self, factory: FlakeFactory, flake_registry: FlakeRegistry, proto_registry: ProtoRegistry):
        self.factory = factory
        self.flake_registry = flake_registry
        self.proto_registry = proto_registry

    def get_new(self, flake_descriptor: FlakeDescriptor):
        return self.build_from_descriptor(flake_descriptor)

    def get_ref(self, flake_id):
        return self.flake_registry.get(flake_id)

    def has(self, flake_id):
        return self.flake_registry.has(flake_id)

    def build_from_descriptor(self, descriptor: FlakeDescriptor):
        flake_id = descriptor.id
        if self.flake_registry.has(flake_id):
            return self.flake_registry.get(flake_id)
        flake_data = self.collect_data_from_descriptor(descriptor)
        proto = self.proto_registry.get(descriptor.proto_module, descriptor.proto_class)
        flake = self.factory.build_flake(proto, flake_data)
        self.flake_registry.set(flake_id, flake)
        return flake

    def collect_data_from_descriptor(self, flake_descriptor: FlakeDescriptor) -> dict:
        data = {}
        for attr_name, attr_descriptor in flake_descriptor.attrs.items():
            data[attr_name] = attr_descriptor.get_primitive_value(self)
        return data
