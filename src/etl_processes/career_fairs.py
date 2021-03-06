from src.common import InsightsReport, NoInsightsDateField, parse_handshake_datetime_str, make_etl_func
from src.handshake_fields import CareerFairFields

CAREER_FAIRS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX2ZhaXJzP2VtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mcWlkPVpRYThDdXFpaldPT3FncVlrQnhkRHAmdG9nZ2xlPWZpbA==',
    date_field=NoInsightsDateField()
)

ENGAGEMENT_TYPE = 'career_fair'


def transform_career_fair(career_fair: dict):
    return {
        'employer_id': career_fair[CareerFairFields.EMPLOYER_ID],
        'engagement_type': ENGAGEMENT_TYPE,
        'handshake_id': career_fair[CareerFairFields.ID],
        'engagement_id': make_engagement_id(career_fair),
        'engagement_name': career_fair[CareerFairFields.NAME],
        'datetime': parse_handshake_datetime_str(career_fair[CareerFairFields.START_DATE_TIME])
    }


def make_engagement_id(career_fair: dict) -> str:
    return f'{ENGAGEMENT_TYPE}_{career_fair[CareerFairFields.EMPLOYER_ID]}_{career_fair[CareerFairFields.ID]}'

run_career_fairs_etl = make_etl_func(CAREER_FAIRS_INSIGHTS_REPORT, transform_career_fair)
