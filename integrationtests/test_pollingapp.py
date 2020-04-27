import unittest

from protoflake import FlakeContainer


class PollService(object):
    def __init__(self):
        self.questions = []


class UiService(object):
    def __init__(self):
        self.poll_service = None


class Question(object):
    def __init__(self):
        self.question_text = None


class Choice(object):
    def __init__(self):
        self.question = None


class IntegrationTestPollingApp(unittest.TestCase):

    def setUp(self) -> None:
        self.container = FlakeContainer()
        self.container.from_files(['integrationtests/test_data/polling/resources.xml'])

    def test_it_created_a_container(self):
        self.assertIsNotNone(self.container)

    def test_it_wires_poll_service_to_ui_service(self):
        poll_service = self.container.get('poll_service')
        ui_service = self.container.get('ui_service')
        self.assertEqual(ui_service.poll_service, poll_service)
