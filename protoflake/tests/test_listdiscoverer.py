import unittest
from unittest.mock import patch
from unittest.mock import Mock

from protoflake.listdiscoverer import ListDiscoverer


class TestListDiscoverer(unittest.TestCase):

    @patch('protoflake.listdiscoverer.DescriptorBuilder')
    def test_it_delegates_to_descriptor_builder(self, builder_mock):
        instance_mock = Mock()
        builder_mock.return_value = instance_mock
        instance_mock.build_flake_descriptor.side_effect = [1, 2, 3]
        discoverer = ListDiscoverer(['a', 'b', 'c'])
        self.assertEqual(discoverer.discover(), [1, 2, 3])
