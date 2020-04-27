"""
Implements the FlakeDiscoverer by parsing xml, json or yaml files.
Infer the right parser to use based on file extension and an injected factory.
"""
from typing import List

from protoflake.descriptors import FileSourceDescriptor
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.flakediscoverer import FlakeDiscoverer
from protoflake.parsers import FlakeParser


class FileDiscoverer(FlakeDiscoverer):

    def __init__(self, parser_factory, file_paths):
        self.file_paths = file_paths
        self.parser_factory = parser_factory

    def discover(self) -> List[FlakeDescriptor]:
        flake_descriptors = []
        for file_path in self.file_paths:
            flake_descriptors.extend(self.parse_file(file_path))
        return flake_descriptors

    def parse_file(self, file_path: str) -> List[FlakeDescriptor]:
        source = FileSourceDescriptor(file_path)
        parser: FlakeParser = self.parser_factory.get_parser(source)
        return parser.from_file(file_path)
