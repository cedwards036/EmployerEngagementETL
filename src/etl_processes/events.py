from src.common import InsightsReport, NoInsightsDateField, parse_handshake_datetime_str, make_etl_func
from src.handshake_fields import EventFields

EVENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1nOWdKOTJTRzBIdjVtVHlCWHRTOFBMJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field=NoInsightsDateField()
)

ENGAGEMENT_TYPE = 'event'


def transform_event(event: dict):
    return {
        'employer_id': event[EventFields.EMPLOYER_ID],
        'engagement_type': ENGAGEMENT_TYPE,
        'handshake_id': event[EventFields.ID],
        'engagement_id': make_engagement_id(event),
        'engagement_name': event[EventFields.NAME],
        'datetime': parse_handshake_datetime_str(event[EventFields.START_DATE_TIME])
    }


def make_engagement_id(event: dict) -> str:
    return f'{ENGAGEMENT_TYPE}_{event[EventFields.EMPLOYER_ID]}_{event[EventFields.ID]}'


run_events_etl = make_etl_func(EVENTS_INSIGHTS_REPORT, transform_event)
