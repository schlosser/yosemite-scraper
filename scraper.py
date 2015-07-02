import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict

BASE_URL = 'http://www.recreation.gov'
REQUEST_URL = BASE_URL + '/campsiteCalendar.do'

config = None
with open('config.json') as config_file:
    config = json.loads(config_file.read())

for trip in config['trips']:

    start_date = datetime.strptime(trip['start_date'], '%m/%d/%Y')
    days = [start_date + timedelta(days=i) for i in range(trip['length'])]
    day_strs = [day.strftime('%m/%d/%Y') for day in days]

    avail_camps = dict((day_str, defaultdict(list)) for day_str in day_strs)
    unavail_camps = dict((day_str, defaultdict(list)) for day_str in day_strs)

    for park_id in config['park_ids']:
        response = requests.get(REQUEST_URL, params={
            'page': 'matrix',
            'contractCode': 'NRSO',
            'calarvdate': trip['start_date'],
            'parkId': park_id
        })
        if not response.ok:
            print "Request failed for park {} on {}".format(park_id,
                                                            trip['start_date'])
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        camp_name = soup.find(id='cgroundName').string
        calendar_body = soup.select('#calendar tbody')[0]
        camps = calendar_body.find_all('tr', attrs={'class': None})

        for camp in camps:
            site_number_tag = camp.select('.siteListLabel a')[0]
            site_number = site_number_tag.string
            site_url = site_number_tag['href']
            call = '(call) {}'.format(site_url)

            status_tags = camp.select('.status')
            for day_str, status_tag in zip(day_strs, status_tags):
                if status_tag.string in ('R', 'X'):  # reserved, unavailable
                    unavail_camps[day_str][camp_name].append(site_number)
                elif status_tag.string == 'C':
                    avail_camps[day_str][camp_name].append((site_number,
                                                            call))

                else:
                    reservation_url = BASE_URL + status_tag.find('a')['href']
                    avail_camps[day_str][camp_name].append((site_number,
                                                            reservation_url))

    for day_str, camps in avail_camps.iteritems():
        print day_str
        print '--------------------'
        for camp_name, sites in camps.iteritems():
            print "{}:".format(camp_name)
            for site_number, action in sites:
                print ' - {}: {}'.format(site_number, action)
