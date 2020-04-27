"""
Service responsible for gathering and storing FlakeDescriptors
"""
from typing import List

from protoflake.filediscoverer import FileDiscoverer
from protoflake.listdiscoverer import ListDiscoverer
from protoflake.parserfactory import ParserFactory


class DiscoveryService(object):

    def __init__(self,
                 file_discoverer_class: FileDiscoverer,
                 list_discoverer_class: ListDiscoverer):
        self.file_discoverer_class = file_discoverer_class
        self.list_discoverer_class = list_discoverer_class
        self.flake_definitions = {}

    def get_definition(self, flake_id):
        return self.definitions[flake_id]

    @property
    def definitions(self):
        return self.flake_definitions

    @staticmethod
    def get_discoverer(klass, *args, **kwargs):
        """Used internally to retrieve the right discoverer implementation
        This is more of a hook point really.
        :param klass: the class of this discoverer
        :param args: the positional arguments to provide to the constructor
        :param kwargs: the keywords arguments to provide to the constructor
        :return: an implementation of the FlakeDiscoverer
        """
        return klass(*args, **kwargs)

    def discover(self, klass, *args, **kwargs):
        discoverer = self.get_discoverer(klass, *args, **kwargs)
        flake_descriptors = discoverer.discover()
        for flake_descriptor in flake_descriptors:
            self.definitions[flake_descriptor.id] = flake_descriptor

    def from_files(self, file_paths: List[str]):
        """
        Given a list of paths, load each one of them as a flake file.
        Path can be relative, but then resolves to the current working directory.
        Files MUST have an extension.
        Supported extensions are .json, .yml, .yaml, .xml
        Refer to the appropriate parser for the expected syntax
        :param file_paths: list of file paths to load (in the same order they are specified)
        :return: Nothing, but stores the discovered flake descriptors internally.
        """
        self.discover(self.file_discoverer_class, ParserFactory, file_paths)

    def from_list(self, definitions):
        """
        Given a list of dict compatible with flakes description (matching the structure of json or yaml),
        parse and store all the flake descriptors in our definitions
        :param definitions:
        :return:
        """
        self.discover(self.list_discoverer_class, definitions)
