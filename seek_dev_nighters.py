import requests
import datetime
import pytz


def load_attempts():
    page = 1
    while page <= int(requests.get(
        'https://devman.org/api/challenges/solution_attempts'
    ).json()['number_of_pages']):
        page_response = requests.get(
            'https://devman.org/api/challenges/solution_attempts',
            params={'page': page}
        ).json()
        page += 1
        for record in page_response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters():
    midnight = 0
    morning = 0
    midnighters = set()
    for attempt in load_attempts():
        hour_of_attempt = timestamp_to_timedate(attempt['timestamp'], attempt['timezone'])
        if midnight <= hour_of_attempt <= morning:
            midnighters.add(attempt['username'])
    return midnighters


def timestamp_to_timedate(timestamp, user_timezone):
    return datetime.datetime.fromtimestamp(
        timestamp,
        tz=pytz.timezone(user_timezone)
    ).astimezone(pytz.timezone('Europe/Moscow')).hour


if __name__ == '__main__':
    print('Midnighters:')
    for midnighter in get_midnighters():
        print(midnighter)
