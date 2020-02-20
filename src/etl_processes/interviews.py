from datetime import datetime
from typing import List

from src.common import InsightsReport, NoInsightsDateField, make_etl_func
from src.handshake_fields import InterviewFields

INTERVIEWS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vaW50ZXJ2aWV3X3NjaGVkdWxlcz9xaWQ9ODJhWDdWWHp0VUJVaHh1OFpYclplayZlbWJlZF9kb21haW49aHR0cHM6JTJGJTJGYXBwLmpvaW5oYW5kc2hha2UuY29tJnRvZ2dsZT1maWw=',
    date_field=NoInsightsDateField()
)

ENGAGEMENT_TYPE = 'interview'


def transform_interview(interview: dict) -> dict:
    dates = parse_date_list_str(interview[InterviewFields.DATE_LIST])
    return {
        'employer_id': interview[InterviewFields.EMPLOYER_ID],
        'engagement_type': ENGAGEMENT_TYPE,
        'handshake_id': interview[InterviewFields.ID],
        'engagement_id': make_engagement_id(interview),
        'engagement_name': make_engagement_name(interview[InterviewFields.EMPLOYER_NAME], dates),
        'datetime': dates[0]
    }


def make_engagement_id(interview: dict) -> str:
    return f'{ENGAGEMENT_TYPE}_{interview[InterviewFields.EMPLOYER_ID]}_{interview[InterviewFields.ID]}'


def make_engagement_name(employer: str, interview_dates: List[datetime]) -> str:
    return f'{employer} Interview Schedule ({list_of_dates_to_str(interview_dates)})'


def parse_date_list_str(date_list: str) -> List[datetime]:
    return sorted([datetime.strptime(date, '%Y-%m-%d') for date in date_list.split(', ')])


def list_of_dates_to_str(dates: List[datetime]) -> str:
    return ', '.join([date.strftime('%Y-%m-%d') for date in dates])


run_interviews_etl = make_etl_func(INTERVIEWS_INSIGHTS_REPORT, transform_interview)
