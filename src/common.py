import csv
import itertools
import json
import os
from datetime import datetime
from typing import List, Callable

from autohandshake import HandshakeSession, HandshakeBrowser, InsightsPage, FileType

CONFIG_FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}/../config.json'


def load_config(config_filepath: str):
    """
    Load the configuration file
    :param config_filepath: the filepath to the config file
    :return: a dict of config values
    """
    with open(config_filepath, 'r') as file:
        return json.load(file)


CONFIG = load_config(CONFIG_FILEPATH)


class BrowsingSession(HandshakeSession):
    """
    A wrapper class around HandshakeSession that always logs into the same account.
    """

    def __init__(self, max_wait_time=300):
        super().__init__(CONFIG['handshake_url'], CONFIG['handshake_email'],
                         download_dir=CONFIG['download_dir'], chromedriver_path=CONFIG['chromedriver_path'], max_wait_time=max_wait_time)


class InsightsDateField:

    def set_report_date_range(self, insights_page: InsightsPage):
        pass


class RangeInsightsDateField(InsightsDateField):

    def __init__(self, date_field_category: str, date_field_title: str):
        self.date_field_category = date_field_category
        self.date_field_title = date_field_title

    def set_report_date_range(self, insights_page: InsightsPage):
        START_DATE = self._first_date_of_current_academic_year()
        END_DATE = datetime.today()
        insights_page.set_date_range_filter(field_category=self.date_field_category,
                                            field_title=self.date_field_title,
                                            start_date=START_DATE, end_date=END_DATE)
        return insights_page

    @staticmethod
    def _first_date_of_current_academic_year():
        JULY = 7
        if datetime.today().month < JULY:
            return datetime(datetime.today().year - 1, JULY, 1)
        else:
            return datetime(datetime.today().year, JULY, 1)


class NoInsightsDateField(InsightsDateField):

    def set_report_date_range(self, insights_page: InsightsPage):
        return insights_page


class InsightsReport:
    """
    A specification of an Inisghts report and its filterable date field.
    """

    def __init__(self, url: str, date_field: InsightsDateField = NoInsightsDateField()):
        self.url = url
        self._date_field = date_field

    def extract_data(self, browser: HandshakeBrowser) -> List[dict]:
        """
        Extract data from a Handshake insights page for the engagement report.

        :param browser: a logged-in HandshakeBrowser
        :param insights_url: a valid Insights report page url from which to get the data
        :return: the raw, extracted data in list-of-dict format
        """
        insights_page = InsightsPage(self.url, browser)
        insights_page = self._date_field.set_report_date_range(insights_page)
        downloaded_filepath = insights_page.download_file(CONFIG['download_dir'], file_type=FileType.JSON)
        return read_and_delete_json(downloaded_filepath)


def make_etl_func(insights_report: InsightsReport, transform_func: Callable[[dict], dict]) -> Callable[[HandshakeBrowser], List[dict]]:
    def etl_func(browser: HandshakeBrowser) -> List[dict]:
        raw_data = insights_report.extract_data(browser)
        return [transform_func(row) for row in raw_data]

    return etl_func

def read_and_delete_json(filepath: str) -> List[dict]:
    """
    Read the given json file into a list of dicts, then delete the file

    :param filepath: the filepath of the json file to read
    :return: a list of dicts representing the json data
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    os.remove(filepath)
    return data


def parse_handshake_datetime_str(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def write_lists_of_dicts_to_csv(filepath, lists: List[List[dict]]):
    combined_lists = list(itertools.chain.from_iterable(lists))
    write_to_csv(filepath, combined_lists)


def write_to_csv(filepath: str, data: List[dict]):
    header = data[0].keys()
    with open(filepath, 'w', encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, header, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return filepath
