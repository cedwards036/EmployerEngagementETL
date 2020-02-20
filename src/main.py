from src.common import BrowsingSession, write_lists_of_dicts_to_csv, CONFIG
from src.etl_processes import run_events_etl, run_jobs_etl, run_career_fairs_etl, run_interviews_etl

if __name__ == '__main__':
    engagement_data = []
    with BrowsingSession() as browser:
        print('Pulling event data...')
        engagement_data.append(run_events_etl(browser))
        print('Pulling career fair data...')
        engagement_data.append(run_career_fairs_etl(browser))
        print('Pulling interview data...')
        engagement_data.append(run_interviews_etl(browser))
        print('Pulling job data...')
        engagement_data.append(run_jobs_etl(browser))

        print('Writing engagement data...')
        write_lists_of_dicts_to_csv(CONFIG['engagement_data_filepath'], engagement_data)

    print('Complete!')
