"""
The flake container is the main interface to the proto flake service.
It acts as a facade between the outer world and the internals of proto flake.
Please note you can have as many FlakeContainer as you wish inside your application.
"""
from discoveryservice import DiscoveryService
from filediscoverer import FileDiscoverer
from flakebuilder import FlakeBuilder
from flakefactory import FlakeFactory
from flakeregistry import FlakeRegistry
from flakeservice import FlakeService
from listdiscoverer import ListDiscoverer
from protoregistry import ProtoRegistry


class FlakeContainer(DiscoveryService, FlakeService):

    def __init__(self):
        super().__init__()
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
