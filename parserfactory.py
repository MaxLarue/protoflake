"""
Parser factory, which returns the right parser depending on the source
"""
from descriptors import FileSourceDescriptor
from parsers import JsonFlakeParser
from parsers import XmlFlakeParser
from parsers import YamlFlakeParser


class NoSuitableParserFound(Exception):
    def __init__(self, extension, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = 'No suitable parsers were found for extension %s' % extension


class ParserFactory(object):

    @staticmethod
    def get_parser(source_descriptor: FileSourceDescriptor):
        extension = source_descriptor.file_extension
        if extension == 'xml':
            return XmlFlakeParser()
        elif extension == 'yaml' or extension == 'yml':
            return YamlFlakeParser()
        elif extension == 'json':
            return JsonFlakeParser()
        else:
            raise NoSuitableParserFound(extension)
