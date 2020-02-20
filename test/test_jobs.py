import unittest
from datetime import datetime

from src.etl_processes.jobs import transform_job
from src.handshake_fields import JobFields


class TestTransformJob(unittest.TestCase):

    def setUp(self) -> None:
        job = {
            JobFields.EMPLOYER_ID: '6235',
            JobFields.ID: '847734',
            JobFields.TITLE: 'SWE 1',
            JobFields.POSTING_CREATED_AT_TIME: '2019-12-01 11:45:15',
            JobFields.TYPE: 'Job'
        }
        self.cleaned_job = transform_job(job)

    def test_changes_field_names_of_basic_str_fields(self):
        self.assertEqual('6235', self.cleaned_job['employer_id'])
        self.assertEqual('847734', self.cleaned_job['handshake_id'])
        self.assertEqual('SWE 1', self.cleaned_job['engagement_name'])

    def test_converts_datetime_field_to_datetime(self):
        self.assertEqual(datetime(2019, 12, 1, 11, 45, 15), self.cleaned_job['datetime'])

    def test_sets_correct_engagement_type(self):
        self.assertEqual('job', self.cleaned_job['engagement_type'])

    def test_makes_engagement_id(self):
        self.assertEqual('job_847734', self.cleaned_job['engagement_id'])

    def test_sets_correct_engagement_type_for_internship(self):
        cleaned_internship = transform_job({
            JobFields.EMPLOYER_ID: '6235',
            JobFields.ID: '847734',
            JobFields.TITLE: 'SWE 1',
            JobFields.POSTING_CREATED_AT_TIME: '2019-12-01 11:45:15',
            JobFields.TYPE: 'Internship'
        })
        self.assertEqual('internship', cleaned_internship['engagement_type'])
