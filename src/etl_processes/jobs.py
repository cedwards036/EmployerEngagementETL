from src.common import InsightsReport, NoInsightsDateField, parse_handshake_datetime_str, make_etl_func
from src.handshake_fields import JobFields

JOBS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vam9icz9xaWQ9VTFpUEpDQ04yZ3FkODdubkFycWFiYSZlbWJlZF9kb21haW49aHR0cHM6JTJGJTJGYXBwLmpvaW5oYW5kc2hha2UuY29tJnRvZ2dsZT1maWw=',
    date_field=NoInsightsDateField()
)


def transform_job(job: dict):
    return {
        'employer_id': job[JobFields.EMPLOYER_ID],
        'engagement_type': get_engagement_type(job),
        'handshake_id': job[JobFields.ID],
        'engagement_id': make_engagement_id(job),
        'engagement_name': job[JobFields.TITLE],
        'datetime': parse_handshake_datetime_str(job[JobFields.POSTING_CREATED_AT_TIME])
    }


def make_engagement_id(job: dict) -> str:
    return f'{get_engagement_type(job)}_{job[JobFields.EMPLOYER_ID]}_{job[JobFields.ID]}'


def get_engagement_type(job: dict):
    if job[JobFields.TYPE] == 'Internship':
        return 'internship'
    else:
        return 'job'


run_jobs_etl = make_etl_func(JOBS_INSIGHTS_REPORT, transform_job)
