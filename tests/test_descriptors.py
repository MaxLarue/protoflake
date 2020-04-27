import unittest

from descriptors import FileSourceDescriptor
from descriptors import CodeSourceDescriptor
from descriptors import PrimitiveAttributeDescriptor
from descriptors import ReferenceAttributeDescriptor
from flakedescriptor import FlakeDescriptor


class TestDescriptors(unittest.TestCase):

    def test_building_a_file_source_descriptor(self):
        path = '/some/where/file.yaml'
        descriptor = FileSourceDescriptor(path)
        self.assertEqual(descriptor.full_path, path)
        self.assertEqual(descriptor.file_name, 'file.yaml')
        self.assertEqual(descriptor.dir_name, '/some/where')

    def test_building_a_code_source_descriptor(self):
        hint = 'created in bla-bla-bla'
        descriptor = CodeSourceDescriptor(hint)
        self.assertEqual(descriptor.hint, hint)

    def test_building_a_primitive_attribute_descriptor(self):
        descriptor = PrimitiveAttributeDescriptor('int', 3)
        self.assertEqual(descriptor.type, 'int')
        self.assertEqual(descriptor.value, 3)

    def test_building_a_reference_attribute_descriptor(self):
        proto = 'my.module.class'
        flake_id = 'where-12345'
        descriptor = ReferenceAttributeDescriptor(proto, flake_id)
        self.assertEqual(descriptor.reference_proto_name, proto)
        self.assertEqual(descriptor.reference_flake_id, flake_id)

    def test_building_a_flake_descriptor(self):
        proto = 'my.module.class'
        flake_id = 'where-12345'
        attrs = {
            'hello': 'world'
        }
        source = None
        descriptor = FlakeDescriptor(proto, flake_id, attrs, source)
        self.assertEqual(descriptor.id, flake_id)
        self.assertEqual(descriptor.proto_name, proto)
        self.assertEqual(descriptor.attrs, attrs)
        self.assertEqual(descriptor.source, source)
