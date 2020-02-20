import unittest
from datetime import datetime

from src.etl_processes.career_fairs import transform_career_fair
from src.handshake_fields import CareerFairFields


class TestTransformCareerFair(unittest.TestCase):

    def setUp(self) -> None:
        career_fair = {
            CareerFairFields.EMPLOYER_ID: '5364',
            CareerFairFields.ID: '63463452',
            CareerFairFields.NAME: 'An Fair',
            CareerFairFields.START_DATE_TIME: '2018-09-25 18:30:00'
        }
        self.cleaned_career_fair = transform_career_fair(career_fair)

    def test_changes_field_names_of_basic_str_fields(self):
        self.assertEqual('5364', self.cleaned_career_fair['employer_id'])
        self.assertEqual('63463452', self.cleaned_career_fair['handshake_id'])
        self.assertEqual('An Fair', self.cleaned_career_fair['engagement_name'])

    def test_converts_datetime_field_to_datetime(self):
        self.assertEqual(datetime(2018, 9, 25, 18, 30), self.cleaned_career_fair['datetime'])

    def test_sets_correct_engagement_type(self):
        self.assertEqual('career_fair', self.cleaned_career_fair['engagement_type'])

    def test_makes_engagement_id(self):
        self.assertEqual('career_fair_5364_63463452', self.cleaned_career_fair['engagement_id'])
