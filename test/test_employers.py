import unittest

from src.etl_processes.employers import transform_employer
from src.handshake_fields import EmployerFields


class TestTransformEvent(unittest.TestCase):

    def setUp(self) -> None:
        employer = {
            EmployerFields.ID: '8475',
            EmployerFields.NAME: 'Deloitte',
            EmployerFields.INDUSTRY: 'Consulting'
        }
        self.cleaned_employer = transform_employer(employer)

    def test_changes_field_names_of_basic_str_fields(self):
        self.assertEqual('8475', self.cleaned_employer['id'])
        self.assertEqual('Deloitte', self.cleaned_employer['name'])
        self.assertEqual('Consulting', self.cleaned_employer['industry'])
