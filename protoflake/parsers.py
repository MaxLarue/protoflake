import xml.etree.ElementTree as ElementTree
from abc import ABC
from abc import abstractmethod
from json import loads as json_load
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from yaml import safe_load as yaml_load

from protoflake.constants import XML_BOOL
from protoflake.constants import XML_FLOAT
from protoflake.constants import XML_INT
from protoflake.constants import XML_LIST
from protoflake.constants import XML_NESTED_FLAKE
from protoflake.constants import XML_REF
from protoflake.constants import XML_ROOT
from protoflake.constants import YAML_ROOT
from protoflake.attributedescriptor import AttributeDescriptor
from protoflake.descriptors import CodeSourceDescriptor
from protoflake.descriptors import FileSourceDescriptor
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.descriptors import ListAttributeDescriptor
from protoflake.descriptors import NestedFlakeDescriptor
from protoflake.descriptors import PrimitiveAttributeDescriptor
from protoflake.descriptors import ReferenceAttributeDescriptor
from protoflake.sourcedescriptor import SourceDescriptor
from protoflake.descriptorbuilder import DescriptorBuilder


class ParserException(Exception):
    def __init__(self, msg: str, source: SourceDescriptor):
        super().__init__(msg)
        self.source = source


class FlakeParser(ABC):
    source: SourceDescriptor

    def from_file(self, full_path: str) -> List[FlakeDescriptor]:
        self.source = FileSourceDescriptor(full_path)
        with open(full_path, 'r') as file:
            return self.parse(file.read())

    def from_string(self, text: str, source_hint: str) -> List[FlakeDescriptor]:
        self.source = CodeSourceDescriptor(source_hint)
        return self.parse(text)

    def get_source(self) -> SourceDescriptor:
        return self.source

    @abstractmethod
    def parse(self, text: str) -> List[FlakeDescriptor]:
        """Given some string (text), process it and return a list of flake descriptor that were encountered
        while parsing.
        """


class InvalidXmlRootException(ParserException):
    def __init__(self, source):
        super().__init__(
            'Invalid root element, it should be %s' % XML_ROOT, source)


class XmlFlakeParser(FlakeParser):
    """Parser for flakes which expects xml input. The rules for defining flakes in xml are:
        - Every file should have one root node, which tag should match the XML_ROOT constant
        - Under that root node only root flakes are allowed
        - Root flakes' tag should be their proto path
        - attributes should be prefixed with their types + '-' (int-, float-, bool-), or nothing for strings
        - children are either: list, flake-* or ref-* or primitives
        - primitives' tag are to be defined like their attribute names (same result)
        - primitives' attributes will be ignored, their values are taken from the node's text
        - list children, follow the format list-{attr-name}, other attributes will be ignored, their own children \
          are processed just like any other flake, list or primitive children
        - flake children's attributes will be ignored, they must have one and only one child, which follows the root \
          flake's definition. they follow the format flake-{attr-name}
        - ref children cannot have children and must have exactly 1 attribute: id, their tags serves as the proto, \
          just like for other flakes.

    See the tests for some example.
    """

    def parse(self, text: str) -> List[FlakeDescriptor]:
        root = ElementTree.fromstring(text)
        if root.tag != XML_ROOT:
            raise InvalidXmlRootException(self.source)
        return list(map(self.process_flake, root))

    def process_flake(self, node) -> FlakeDescriptor:
        proto = node.tag
        attrs = {**self.process_attrib(node), **self.process_sub_nodes(node)}
        flake_id = attrs.get('id').value
        source = self.source
        return FlakeDescriptor(proto, flake_id, attrs, source)

    def process_attrib(self, node) -> Dict[str, AttributeDescriptor]:
        return dict(list(map(self.process_single_attr, node.attrib.items())))

    def process_sub_nodes(self, node) -> Dict[str, AttributeDescriptor]:
        return dict(map(self.process_single_attr, [(child.tag, child) for child in node]))

    def process_nested_flake(self, key: str, node) -> Tuple[str, NestedFlakeDescriptor]:
        return key, NestedFlakeDescriptor(self.process_flake(node[0]))

    @staticmethod
    def process_ref(key: str, node) -> Tuple[str, ReferenceAttributeDescriptor]:
        flake_id = node.attrib['id']
        attr = ReferenceAttributeDescriptor(flake_id)
        return key, attr

    def process_list(self, key: str, node) -> Tuple[str, ListAttributeDescriptor]:
        attrs = list(self.process_sub_nodes(node).values())
        return key, ListAttributeDescriptor(attrs)

    def process_single_attr(self, key_value: Tuple[str, Any]) -> Tuple[str, AttributeDescriptor]:
        key, value = key_value
        if key.startswith(XML_LIST):
            return self.process_list(key[5:], value)
        elif key.startswith(XML_REF):
            return self.process_ref(key[4:], value)
        elif key.startswith(XML_NESTED_FLAKE):
            return self.process_nested_flake(key[6:], value)

        if not isinstance(value, str):
            value = value.text

        if key.startswith(XML_INT):
            return key[4:], PrimitiveAttributeDescriptor('int', int(value))
        elif key.startswith(XML_BOOL):
            return key[5:], PrimitiveAttributeDescriptor('bool', value == 'True')
        elif key.startswith(XML_FLOAT):
            return key[6:], PrimitiveAttributeDescriptor('float', float(value))
        else:
            return key, PrimitiveAttributeDescriptor('str', value)


class InvalidRootJson(Exception):
    def __init__(self, source):
        super().__init__(
            'Invalid root element, it should be an array', source)


class JsonFlakeParser(FlakeParser):
    """A parser for flakes which expect json input.
    The format rules are as follow:
        - the root node of json must be a list.
        - List and primitives are natively supported by json, so these will work as expected.
        - ref members should have a is_flake_ref property which is truth-y (not null, not missing, not 0, not empty)
        - flakes members must have a proto property set to a string, and an id set to a string as well.

    """

    def __init__(self):
        super().__init__()
        self.builder = DescriptorBuilder()

    def parse(self, text: str) -> List[FlakeDescriptor]:
        self.builder.set_source(self.source)
        tree = json_load(text)
        if not isinstance(tree, list):
            raise InvalidRootJson(self.source)
        return list(map(lambda n: self.builder.process_node(n, True), tree))


class InvalidRootYaml(ParserException):
    def __init__(self, source):
        super().__init__(
            'Invalid root for yaml file, should be %s key, then list as value' % YAML_ROOT, source)


class YamlFlakeParser(JsonFlakeParser):
    """Parser able to process yaml files/string and build flake descriptors out of it.
    It follows almost the same rules as the json parser.
    Only exception being:
        - The root node must be a mapping with the YAML_ROOT key
        - The root node's value must be a list (and probably cannot be empty)
    """

    def parse(self, text: str) -> List[FlakeDescriptor]:
        self.builder.set_source(self.source)
        as_root = yaml_load(text)
        if not isinstance(as_root, dict) or not as_root.get(YAML_ROOT):
            raise InvalidRootYaml(self.source)
        as_list = as_root.get(YAML_ROOT)
        if not isinstance(as_list, list):
            raise InvalidRootYaml(self.source)
        return list(map(lambda n: self.builder.process_node(n, True), as_list))
