import unittest
from datetime import datetime

from src.etl_processes.events import transform_event
from src.handshake_fields import EventFields


class TestTransformEvent(unittest.TestCase):

    def setUp(self) -> None:
        event = {
            EventFields.EMPLOYER_ID: '2892',
            EventFields.ID: '938093',
            EventFields.NAME: 'An Event',
            EventFields.START_DATE_TIME: '2018-09-25 18:30:00'
        }
        self.cleaned_event = transform_event(event)

    def test_changes_field_names_of_basic_str_fields(self):
        self.assertEqual('2892', self.cleaned_event['employer_id'])
        self.assertEqual('938093', self.cleaned_event['handshake_id'])
        self.assertEqual('An Event', self.cleaned_event['engagement_name'])

    def test_converts_datetime_field_to_datetime(self):
        self.assertEqual(datetime(2018, 9, 25, 18, 30), self.cleaned_event['datetime'])

    def test_sets_correct_engagement_type(self):
        self.assertEqual('event', self.cleaned_event['engagement_type'])

    def test_makes_engagement_id(self):
        self.assertEqual('event_938093', self.cleaned_event['engagement_id'])
