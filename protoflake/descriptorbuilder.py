"""
Given a dict of python primitives, builds a FlakeDescriptor
"""
from typing import Any
from typing import Tuple
from typing import Union
from typing import cast

from protoflake.attributedescriptor import AttributeDescriptor
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.descriptors import ListAttributeDescriptor
from protoflake.descriptors import NestedFlakeDescriptor
from protoflake.descriptors import PrimitiveAttributeDescriptor
from protoflake.descriptors import ReferenceAttributeDescriptor


class DescriptorBuilder(object):

    def __init__(self):
        self.source = None

    def set_source(self, source):
        self.source = source

    def build_flake_descriptor(self, data):
        return self.process_flake_node(data)

    def process_flake_node(self, node) -> FlakeDescriptor:
        attrs = cast(Any, dict(list(map(self.process_attr, node.items()))))
        return FlakeDescriptor(attrs.get('proto').value, attrs.get('id').value, attrs, self.source)

    @staticmethod
    def process_ref(value: Any) -> AttributeDescriptor:
        flake_id = value.get('id')
        return ReferenceAttributeDescriptor(flake_id)

    def process_node(self, node, root=False) -> Union[FlakeDescriptor, AttributeDescriptor]:
        if node.get('proto'):
            if root:
                return self.process_flake_node(node)
            else:
                return NestedFlakeDescriptor(self.process_flake_node(node))

    def process_attr(self, key_value: Any) -> Tuple[str, AttributeDescriptor]:
        key, value = key_value
        if isinstance(value, dict):
            if value.get('is_flake_ref'):
                return key, self.process_ref(value)
            else:
                return key, self.process_node(value)
        elif isinstance(value, list):
            return key, ListAttributeDescriptor(list(map(
                lambda k_v: k_v[1],
                map(lambda a: self.process_attr(('', a)), value))))
        elif isinstance(value, bool):
            return key, PrimitiveAttributeDescriptor('bool', value)
        elif isinstance(value, int):
            return key, PrimitiveAttributeDescriptor('int', value)
        elif isinstance(value, float):
            return key, PrimitiveAttributeDescriptor('float', value)
        elif isinstance(value, str):
            return key, PrimitiveAttributeDescriptor('str', value)