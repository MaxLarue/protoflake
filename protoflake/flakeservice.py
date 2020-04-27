"""
The flake service is responsible for instantiating and retrieving flakes, it relies on some
discovery service to have been injected in order to get the flake definitions.
"""
from protoflake.discoveryservice import DiscoveryService
from protoflake.flakebuilder import FlakeBuilder


class FlakeService(object):

    def __init__(self,
                 discovery_service: DiscoveryService,
                 builder: FlakeBuilder):
        super().__init__()
        self.discovery = discovery_service
        self.builder = builder

    def get(self, flake_id):
        if self.builder.has(flake_id):
            return self.builder.get_ref(flake_id)
        else:
            return self.builder.get_new(self.discovery.get_definition(flake_id))
