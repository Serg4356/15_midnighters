import requests
import datetime
import pytz


def load_attempts():
    for page in range(1, int(requests.get(
        'https://devman.org/api/challenges/solution_attempts'
    ).json()['number_of_pages']) + 1, 1):
        page_response = requests.get(
            'https://devman.org/api/challenges/solution_attempts',
            params={'page': page}
        ).json()
        for record in page_response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters():
    midnight = 0
    morning = 0
    midnighters = []
    for attempt in load_attempts():
        hour_of_attempt = timestamp_to_timedate(attempt['timestamp'])
        if midnight <= int(hour_of_attempt) <= morning:
            midnighters.append(attempt['username'])
    return midnighters


def timestamp_to_timedate(timestamp):
    return datetime.datetime.fromtimestamp(
        timestamp,
        tz=pytz.timezone('Europe/Moscow')
    ).hour


if __name__ == '__main__':
    print('Midnighters:')
    for midnighter in set(get_midnighters()):
        print(midnighter)
