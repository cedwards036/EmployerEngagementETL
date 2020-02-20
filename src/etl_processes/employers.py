from src.common import InsightsReport, NoInsightsDateField, make_etl_func
from src.handshake_fields import EmployerFields

EVENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZW1wbG95ZXJzP3FpZD1mdlAxOUViRzRkN096Z3RoRDFvcjJDJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field=NoInsightsDateField()
)


def transform_employer(employer: dict):
    return {
        'id': employer[EmployerFields.ID],
        'name': employer[EmployerFields.NAME],
        'industry': employer[EmployerFields.INDUSTRY]
    }


run_employers_etl = make_etl_func(EVENTS_INSIGHTS_REPORT, transform_employer)
