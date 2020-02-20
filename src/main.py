from src.common import BrowsingSession, run_etl, write_to_csv, CONFIG
from src.events import EVENTS_INSIGHTS_REPORT, transform_event

if __name__ == '__main__':
    with BrowsingSession() as browser:
        print('Pulling event data...')
        clean_event_data = run_etl(browser, EVENTS_INSIGHTS_REPORT, transform_event)

        print('Writing engagement data...')
        engagement_data = clean_event_data
        write_to_csv(CONFIG['engagement_data_filepath'], engagement_data)

    print('Complete!')
