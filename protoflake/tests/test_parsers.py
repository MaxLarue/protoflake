import unittest
from typing import Any
from typing import cast

from protoflake.constants import XML_ROOT
from protoflake.constants import YAML_ROOT
from protoflake.descriptors import CodeSourceDescriptor
from protoflake.flakedescriptor import FlakeDescriptor
from protoflake.parsers import InvalidRootYaml
from protoflake.parsers import XmlFlakeParser
from protoflake.parsers import JsonFlakeParser
from protoflake.parsers import InvalidXmlRootException
from protoflake.parsers import InvalidRootJson
from protoflake.parsers import YamlFlakeParser


class TestXmlParser(unittest.TestCase):

    def test_root_needs_to_be_whats_in_constants_success(self):
        xml = '''
        <%s>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        parser.from_string(xml, TestXmlParser.test_root_needs_to_be_whats_in_constants_success.__qualname__)

    def test_root_needs_to_be_whats_in_constants_fail(self):
        xml = '''
        <%s>
        </%s>
        ''' % (XML_ROOT + 'a', XML_ROOT + 'a')
        parser = XmlFlakeParser()
        with self.assertRaises(InvalidXmlRootException):
            parser.from_string(xml, TestXmlParser.test_root_needs_to_be_whats_in_constants_fail.__qualname__)

    def test_parsing_a_simple_flake(self):
        func_name = TestXmlParser.test_parsing_a_simple_flake.__qualname__
        xml = '''
        <%s>
            <resource.body id='first flake' />
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, func_name)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0], FlakeDescriptor)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].proto_name, 'resource.body')
        self.assertEqual(cast(CodeSourceDescriptor, parser.get_source()).hint, func_name)

    def test_parsing_a_simple_flake_from_file(self):
        TestXmlParser.test_parsing_a_simple_flake.__qualname__
        parser = XmlFlakeParser()
        flakes: Any = parser.from_file('./protoflake/tests/test_data/simple_file.xml')
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0], FlakeDescriptor)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].proto_name, 'resource.body')

    def test_parsing_int(self):
        xml = '''
        <%s>
            <resource.body id='first flake' int-weight="85" />
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_int.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'int')

    def test_parsing_float(self):
        xml = '''
        <%s>
            <resource.body id='first flake' float-weight="85.5" />
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_float.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85.5)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'float')

    def test_parsing_bool(self):
        xml = '''
        <%s>
            <resource.body id='first flake' bool-heavy="True" bool-light="False" />
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_bool.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('heavy').value, True)
        self.assertEqual(flakes[0].attrs.get('heavy').type, 'bool')
        self.assertEqual(flakes[0].attrs.get('light').value, False)
        self.assertEqual(flakes[0].attrs.get('light').type, 'bool')

    def test_parsing_with_nested_primitives(self):
        xml = '''
        <%s>
            <resource.body>
                <id>first flake</id>
                <bool-heavy>True</bool-heavy>
                <bool-light>False</bool-light>
            </resource.body>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_with_nested_primitives.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].attrs.get('heavy').value, True)
        self.assertEqual(flakes[0].attrs.get('heavy').type, 'bool')
        self.assertEqual(flakes[0].attrs.get('light').value, False)
        self.assertEqual(flakes[0].attrs.get('light').type, 'bool')

    def test_parsing_lists_of_primitives(self):
        xml = '''
        <%s>
            <resource.body id='first flake'>
                <list-parts>
                    <int-0>3</int-0>
                    <int-1>2</int-1>
                    <int-2>1</int-2>
                </list-parts>
            </resource.body>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_lists_of_primitives.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[2].value, 1)

    def test_parsing_nested_lists(self):
        xml = '''
        <%s>
            <resource.body id='first flake'>
                <list-parts>
                    <list-sub-parts>
                        <int-0>3</int-0>
                        <int-1>2</int-1>
                        <int-2>1</int-2>
                    </list-sub-parts>
                </list-parts>
            </resource.body>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_nested_lists.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertIsInstance(flakes[0].attrs.get('parts').value[0].value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value[0].value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[2].value, 1)

    def test_parsing_ref(self):
        xml = '''
        <%s>
            <resource.body id='first flake'>
                <ref-color id="some id" />
            </resource.body>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_ref.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('color').reference_flake_id, 'some id')

    def test_parsing_nested_flakes(self):
        xml = '''
        <%s>
            <resource.body id='first flake'>
                <flake-color>
                    <resource.color id="some id" />
                </flake-color>
            </resource.body>
        </%s>
        ''' % (XML_ROOT, XML_ROOT)
        parser = XmlFlakeParser()
        flakes: Any = parser.from_string(xml, TestXmlParser.test_parsing_nested_flakes.__qualname__)
        self.assertEqual(len(flakes), 1)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.id, 'some id')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.proto_name, 'resource.color')


class TestJsonParser(unittest.TestCase):

    def test_we_need_a_root_list_element_success(self):
        json = '''
        []
        '''
        parser = JsonFlakeParser()
        parser.from_string(json, TestJsonParser.test_we_need_a_root_list_element_success.__qualname__)

    def test_we_need_a_root_list_element_fail(self):
        json = '''
        {}
        '''
        parser = JsonFlakeParser()
        with self.assertRaises(InvalidRootJson):
            parser.from_string(json, TestJsonParser.test_we_need_a_root_list_element_fail.__qualname__)

    def test_parsing_single_simple_flake(self):
        json = '''
        [
            {"proto": "resource.body", "id": "first flake"}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_single_simple_flake.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0], FlakeDescriptor)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].proto_name, 'resource.body')

    def test_parsing_int(self):
        json = '''
        [
            {"proto": "resource.body", "id": "first flake", "weight": 85}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_int.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'int')

    def test_parsing_float(self):
        json = '''
        [
            {"proto": "resource.body", "id": "first flake", "weight": 85.5}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_float.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85.5)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'float')

    def test_parsing_bool(self):
        json = '''
        [
            {"proto": "resource.body", "id": "first flake", "heavy": true, "light": false}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_bool.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('heavy').value, True)
        self.assertEqual(flakes[0].attrs.get('heavy').type, 'bool')
        self.assertEqual(flakes[0].attrs.get('light').value, False)
        self.assertEqual(flakes[0].attrs.get('light').type, 'bool')

    def test_parsing_lists_of_primitives(self):
        json = '''
        [
            {"proto": "my.body", "id": "one", "parts": [
                3,
                2,
                1
            ]}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_lists_of_primitives.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[2].value, 1)

    def test_parsing_nested_lists(self):
        json = '''
        [
            {"proto": "my.body", "id": "one", "parts": [
                [3, 2, 1]
            ]}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_nested_lists.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertIsInstance(flakes[0].attrs.get('parts').value[0].value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value[0].value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[2].value, 1)

    def test_parsing_ref(self):
        json = '''
        [
            {"proto": "my.body", "id": "some", "color": {
                "is_flake_ref": "True",
                "proto": "my.module.color",
                "id": "some id"
            }}
        ] 
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_ref.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('color').reference_flake_id, 'some id')

    def test_parsing_nested_flakes(self):
        json = '''
        [
            {"proto": "my.body", "id": "first flake", "color": {"proto": "resource.color", "id": "some id"}}
        ]
        '''
        parser = JsonFlakeParser()
        flakes: Any = parser.from_string(json, TestJsonParser.test_parsing_nested_flakes.__qualname__)
        self.assertEqual(len(flakes), 1)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.id, 'some id')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.proto_name, 'resource.color')


class TestYamlParser(unittest.TestCase):

    def test_we_need_a_root_list_element_success(self):
        yaml = '''
        %s:
            - something: someone
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        parser.from_string(yaml, TestYamlParser.test_we_need_a_root_list_element_success.__qualname__)

    def test_we_need_a_root_list_element_fail_bad_root(self):
        yaml = '''
        {}
        '''
        parser = YamlFlakeParser()
        with self.assertRaises(InvalidRootYaml):
            parser.from_string(yaml, TestYamlParser.test_we_need_a_root_list_element_fail_bad_root.__qualname__)

    def test_we_need_a_root_list_element_fail_first_elem_should_be_list(self):
        func_name = TestYamlParser.test_we_need_a_root_list_element_fail_first_elem_should_be_list.__qualname__
        yaml = '''
        %s:
            key: value
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        with self.assertRaises(InvalidRootYaml):
            parser.from_string(yaml, func_name)

    def test_parsing_single_simple_flake(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: first flake
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_single_simple_flake.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0], FlakeDescriptor)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].proto_name, 'resource.body')

    def test_parsing_int(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: body
              weight: 85
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_int.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'int')

    def test_parsing_float(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: body
              weight: 85.5
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_float.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('weight').value, 85.5)
        self.assertEqual(flakes[0].attrs.get('weight').type, 'float')

    def test_parsing_bool(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: body
              heavy: True
              light: False
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_bool.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('heavy').value, True)
        self.assertEqual(flakes[0].attrs.get('heavy').type, 'bool')
        self.assertEqual(flakes[0].attrs.get('light').value, False)
        self.assertEqual(flakes[0].attrs.get('light').type, 'bool')

    def test_parsing_lists_of_primitives(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: body
              parts:
                - 3
                - 2
                - 1
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_lists_of_primitives.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[2].value, 1)

    def test_parsing_nested_lists(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: body
              parts:
                  -
                    - 3
                    - 2
                    - 1
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_nested_lists.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertIsInstance(flakes[0].attrs.get('parts').value, list)
        self.assertIsInstance(flakes[0].attrs.get('parts').value[0].value, list)
        self.assertEqual(len(flakes[0].attrs.get('parts').value[0].value), 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[0].value, 3)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[1].value, 2)
        self.assertEqual(flakes[0].attrs.get('parts').value[0].value[2].value, 1)

    def test_parsing_ref(self):
        yaml = '''
        %s:
            - proto: body.resource
              id: body
              color:
                id: some id
                is_flake_ref: True
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_ref.__qualname__)
        self.assertEqual(1, len(flakes))
        self.assertEqual(flakes[0].attrs.get('color').reference_flake_id, 'some id')

    def test_parsing_nested_flakes(self):
        yaml = '''
        %s:
            - proto: resource.body
              id: first flake
              color:
                proto: resource.color
                id: some id
        ''' % YAML_ROOT
        parser = YamlFlakeParser()
        flakes: Any = parser.from_string(yaml, TestYamlParser.test_parsing_nested_flakes.__qualname__)
        self.assertEqual(len(flakes), 1)
        self.assertEqual(flakes[0].id, 'first flake')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.id, 'some id')
        self.assertEqual(flakes[0].attrs.get('color').nested_descriptor.proto_name, 'resource.color')
