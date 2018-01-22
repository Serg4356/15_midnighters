import requests
import datetime
import pytz


def load_attempts():
    proceed_loading = True
    page = 1
    while proceed_loading:
        api_response = requests.get(
            'https://devman.org/api/challenges/solution_attempts',
            params={'page': page}
        ).json()
        if page >= api_response['number_of_pages']:
            proceed_loading = False
        page += 1
        for record in api_response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters(attempts):
    midnight = 0
    morning = 5
    midnighters = set()
    for attempt in attempts:
        hour_of_attempt = timestamp_to_timedate(attempt['timestamp'], attempt['timezone'])
        if midnight <= hour_of_attempt <= morning:
            midnighters.add(attempt['username'])
    return midnighters


def timestamp_to_timedate(timestamp, user_timezone):
    return datetime.datetime.fromtimestamp(
        timestamp,
        tz=pytz.timezone(user_timezone)
    ).hour


if __name__ == '__main__':
    print('Midnighters:')
    for midnighter in get_midnighters(load_attempts()):
        print(midnighter)
