"""
The flake container is the main interface to the proto flake service.
It acts as a facade between the outer world and the internals of proto flake.
Please note you can have as many FlakeContainer as you wish inside your application.
"""
from .discoveryservice import DiscoveryService
from .filediscoverer import FileDiscoverer
from .flakebuilder import FlakeBuilder
from .flakefactory import FlakeFactory
from .flakeregistry import FlakeRegistry
from .flakeservice import FlakeService
from .listdiscoverer import ListDiscoverer
from .protoregistry import ProtoRegistry


class FlakeContainer(object):

    def __init__(self):
        self.proto_registry = ProtoRegistry()
        self.flake_registry = FlakeRegistry()
        self.flake_factory = FlakeFactory()
        self.builder = FlakeBuilder(
            self.flake_factory,
            self.flake_registry,
            self.proto_registry
        )
        self.file_discoverer_class = FileDiscoverer
        self.list_discoverer_class = ListDiscoverer
        self.discovery_service = DiscoveryService(self.file_discoverer_class, self.list_discoverer_class)
        self.flake_service = FlakeService(self.discovery_service, self.builder)

    def from_list(self, *args, **kwargs):
        return self.discovery_service.from_list(*args, **kwargs)

    def from_files(self, *args, **kwargs):
        return self.discovery_service.from_files(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.flake_service.get(*args, **kwargs)
