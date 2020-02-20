from src.career_fairs import run_career_fairs_etl
from src.common import BrowsingSession, write_lists_of_dicts_to_csv, CONFIG
from src.events import run_events_etl
from src.jobs import run_jobs_etl

if __name__ == '__main__':
    with BrowsingSession() as browser:
        print('Pulling event data...')
        clean_event_data = run_events_etl(browser)
        print('Pulling career_fair data...')
        clean_career_fair_data = run_career_fairs_etl(browser)
        print('Pulling job data...')
        clean_job_data = run_jobs_etl(browser)

        print('Writing engagement data...')
        write_lists_of_dicts_to_csv(CONFIG['engagement_data_filepath'],
                                    clean_career_fair_data,
                                    clean_job_data,
                                    clean_event_data)

    print('Complete!')
