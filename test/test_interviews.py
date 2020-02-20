import unittest
from datetime import datetime

from src.etl_processes.interviews import transform_interview, parse_date_list_str
from src.handshake_fields import InterviewFields


class TestTransformInterview(unittest.TestCase):

    def setUp(self) -> None:
        interview = {
            InterviewFields.EMPLOYER_ID: '38479',
            InterviewFields.ID: '2837824',
            InterviewFields.EMPLOYER_NAME: 'Google',
            InterviewFields.DATE_LIST: '2019-11-15, 2019-11-12'
        }
        self.cleaned_interview = transform_interview(interview)

    def test_changes_field_names_of_basic_str_fields(self):
        self.assertEqual('38479', self.cleaned_interview['employer_id'])
        self.assertEqual('2837824', self.cleaned_interview['handshake_id'])
        self.assertEqual('Google Interview Schedule (2019-11-12, 2019-11-15)', self.cleaned_interview['engagement_name'])

    def test_converts_datetime_field_to_datetime(self):
        self.assertEqual(datetime(2019, 11, 12), self.cleaned_interview['datetime'])

    def test_sets_correct_engagement_type(self):
        self.assertEqual('interview', self.cleaned_interview['engagement_type'])

    def test_makes_engagement_id(self):
        self.assertEqual('interview_38479_2837824', self.cleaned_interview['engagement_id'])


class TestDateListParser(unittest.TestCase):

    def test_single_item_list(self):
        self.assertEqual([datetime(2019, 12, 3)], parse_date_list_str('2019-12-03'))

    def test_multi_item_list_is_sorted(self):
        self.assertEqual([datetime(2019, 2, 14), datetime(2019, 7, 30), datetime(2019, 12, 3)],
                         parse_date_list_str('2019-12-03, 2019-02-14, 2019-07-30'))
