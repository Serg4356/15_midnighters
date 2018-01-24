import requests
import datetime
import pytz
import collections


def load_attempts():
    response = requests.get(
        'https://devman.org/api/challenges/solution_attempts')
    pages = int(response.json()['number_of_pages'])
    for page in range(pages):
        page_response = requests.get(
            'https://devman.org/api/challenges/solution_attempts',
            params={'page': int(page)+1}
        ).json()
        for record in page_response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters():
    timezone_stamp = pytz.timezone('Europe/Moscow')
    midnighters = []
    for attempt in load_attempts():
        hour_of_attempt = to_hours_in_one_tz(
            timestamp_to_timedate(attempt['timestamp']),
            timezone_stamp,
            pytz.timezone(attempt['timezone']))
        if 0 <= int(hour_of_attempt) <= 5:
            midnighters.append(attempt['username'])
    return midnighters


def timestamp_to_timedate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def to_hours_in_one_tz(time, timezone_stamp, timezone_sample):
    return timezone_sample.localize(
        time
    ).astimezone(
        timezone_stamp
    ).strftime('%H')


if __name__ == '__main__':
    print('Midnighters:')
    for midnighter in collections.Counter(get_midnighters()):
        print(midnighter)
