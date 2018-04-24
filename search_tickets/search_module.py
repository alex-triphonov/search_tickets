import json
import logging

import re
from calendar import monthrange
from datetime import datetime
from pprint import pprint

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrainTickets:
    def __init__(self, departure, destination, day, month=None, year=None):
        """
        :param departure: str()
        :param destination: str()
        :param day: int()
        :param month: int(), default = current month
        :param year: int(), default = current year
        """
        self.session = requests.Session()
        self.uz_url = 'https://booking.uz.gov.ua/ru/train_search/'
        self.departure, self.destination, self.date = self.validate(departure, destination, day, month, year)

    def find_tickets(self):
        logger.info('searching for tickets from "{}" to "{}" on {}'.format(self.departure, self.destination, self.date))
        available_trains = []
        departure_id = self.search_for_station_id(self.departure)
        destination_id = self.search_for_station_id(self.destination)
        data = {'from': departure_id,
                'to': destination_id,
                'date': self.date
                }
        response = self.session.post(self.uz_url, data=data)
        response_dict = json.loads(response.text)['data']
        try:
            logger.warning(response_dict['warning'])
        except KeyError:
            for train in response_dict['list']:
                if train['types']:
                    available_trains.append({'train_num': train['num'],
                                             'dep_time': train['from']['time'],
                                             'arr_time': train['to']['time'],
                                             'travel_time': train['travelTime'],
                                             'seats': train['types']
                                             })
        return available_trains

    @staticmethod
    def validate(departure, destination, day, month=None, year=None):
        departure = re.sub(r'[^а-яА-Я]', '', departure).title()
        if not departure:
            pass
            raise ValueError('Название города отправления введено не корректно')
        destination = re.sub(r'[^а-яА-Я]', '', destination).title()
        if not destination:
            raise ValueError('Название города назначения введено не корректно')
        # validate year
        curr_year = datetime.now().year
        if not year:
            year = curr_year
        elif year and year == curr_year or year == curr_year + 1:
            year = year
        else:
            raise ValueError('Неверно введен год')
        # validate month
        curr_month = datetime.now().month
        if not month:
            month = '{0:02d}'.format(curr_month)
        elif month and month <= 12:
            month = '{0:02d}'.format(month)
        else:
            raise ValueError('Неверно введен месяц(должно быть число от 1 до 12)')
        # validate day
        days_in_curr_month = monthrange(curr_year, curr_month)[1]
        if day <= days_in_curr_month:
            day = '{0:02d}'.format(day)
        else:
            raise ValueError('Неверно введена дата, в текущем месяце всего {} дней'.format(days_in_curr_month))
        # check if date if not in past
        date_now = datetime.now().date()
        date_we_have = datetime(int(year), int(month), int(day)).date()
        if date_we_have < date_now:
            raise ValueError('Указанная дата ведет в прошлое, те поезда уже ушли..')
        else:
            date = '-'.join([str(year), str(month), str(day)])

        return departure, destination, date

    @staticmethod
    def search_for_station_id(station):
        search_url = 'https://booking.uz.gov.ua/ru/train_search/station/?term={}'.format(station)
        response = json.loads(requests.get(search_url).text)
        for region in response:
            if region['title'] == station:
                return region['value']


if __name__ == '__main__':
    a = TrainTickets('киев', 'одесса', 27, 4)
    pprint(a.find_tickets())
