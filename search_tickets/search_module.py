import json
import logging
import re
from calendar import monthrange
from datetime import datetime

import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError

from search_tickets.get_proxy import get_proxies
from telegram_modules.send_msg import TelegramMsg

logging.getLogger("requests").setLevel(logging.WARNING)
LOG_FORMAT = '%(asctime)s %(levelname)-10s %(name)-16s %(funcName)-20s <%(lineno)-3d> %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


class TrainTickets:
    def __init__(self, departure, destination, day, month=None, year=None, types=None, spec=None, exclude=None):
        """
        :param departure: str()
        :param destination: str()
        :param day: int()
        :param month: int(), default = current month
        :param year: int(), default = current year
        :param types: list() of types of coaches to search
        :param spec: list() of specific trains to search
        :param exclude: list() of trains exclude from search
        """
        self.session = requests.Session()
        self.set_session_proxy()
        self.telegram = TelegramMsg()
        self.uz_url = 'https://booking.uz.gov.ua/ru/train_search/'
        self.departure, self.destination, self.date = self.validate(departure, destination, day, month, year)
        self.departure_id = self.search_for_station_id(self.departure)
        self.destination_id = self.search_for_station_id(self.destination)
        self.coach_types = types
        self.specific_train = spec
        self.exclude_train = exclude

    def find_tickets(self):
        logger.info('searching for tickets from "{}" to "{}" on {}'.format(self.departure, self.destination, self.date))
        available_trains = []
        train_route = '{}-{}'.format(self.departure, self.destination)
        search_time = datetime.strptime(self.date, '%Y-%m-%d').strftime('%d-%m-%Y')

        data = {'from': self.departure_id,
                'to': self.destination_id,
                'date': self.date
                }
        response = self.session.post(self.uz_url, data=data)
        response_dict = json.loads(response.text)
        logger.debug(response_dict)
        try:
            logger.info(response_dict['data']['warning'])
        except TypeError:
            logger.warning(response_dict['data'])
        except KeyError:
            for train in response_dict['data']['list']:
                logger.debug(train)
                if train['types']:
                    for ttype in train['types']:
                        current_type = ttype['id']
                        current_train_id = train['num']
                        # if searching for tickets on specific train id:
                        if self.specific_train is None or current_train_id in self.specific_train:
                            # if user exclude specific train
                            if self.exclude_train is None or current_train_id not in self.exclude_train:
                                # if specific coach types specified
                                if self.coach_types is None or current_type.lower() in self.coach_types:
                                    try:
                                        logger.debug('get price for train {}, type {}'.format(train['num'], current_type))
                                        prices = self.get_price(train['num'], current_type)
                                        available_trains.append({'train_num': current_train_id,
                                                                 'dep_time': train['from']['time'],
                                                                 'arr_time': train['to']['time'],
                                                                 'travel_time': train['travelTime'],
                                                                 'seats': self.form_seats_info(train['types'], prices)
                                                                 })
                                    except TypeError:
                                        continue

            if available_trains:
                self.telegram.send_available_trains(available_trains, route=train_route, time=search_time)
            else:
                logger.info('Нет мест с заданными Вами характеристикам')

        return available_trains

    def book_tickets(self, target_train=None, target_type=None, amount=1):
        """
        :param target_train: str() - specific train id to search
        :param target_type: list() - type of coaches you want to find (п,к,л,с1,с2)
        :param amount: int() - amount of tickets
        :return:
        """
        pass
    #     form_data = {'roundtrip':0
        # 'places[0][ord]': '0',
        # 'places[0][from]': depart_id,
        # 'places[0][to]': dest_id,
        # 'places[0][train]': train_num,
        # 'places[0][date]':'2018-05-16',
        # 'places[0][wagon_num]': wagon_num
        # 'places[0][wagon_class]': wagon_class
        # 'places[0][wagon_type]':П
        # 'places[0][wagon_railway]':40
        # 'places[0][charline]':А
        # 'places[0][firstname]':Артем
        # 'places[0][lastname]':черный
        # 'places[0][bedding]':1
        # 'places[0][services][]':Ш
        # 'places[0][child]':
        # 'places[0][student]':
        # 'places[0][reserve]':0
        # 'places[0][place_num]':037}

    def search_for_station_id(self, station):
        search_url = 'https://booking.uz.gov.ua/ru/train_search/station/?term={}'.format(station)
        response = json.loads(self.session.get(search_url).text)
        for region in response:
            if region['title'] == station:
                return region['value']

    def get_price(self, train_id, wagon_type_id):
        """
        :param train_id: str() e.g. '148К'
        :param wagon_type_id: str(),
        :return: dict() - prices for different types of coaches
        """
        price_url = 'https://booking.uz.gov.ua/ru/train_wagons/'
        form_data = {
            'from': self.departure_id,
            'to': self.destination_id,
            'date': self.date,
            'train': train_id,
            'wagon_type_id': wagon_type_id,
            # 'get_tpl': 1
        }
        response = self.session.post(price_url, data=form_data)
        data = json.loads(response.text)
        logger.debug(data)
        prices = {}
        for coach in data['data']['types']:
            cost = str(coach['cost'])
            prices[coach['title']] = float('{}.{}'.format(cost[:len(cost)-2], cost[len(cost)-2:]))
        logger.debug(prices)

        return prices

    def set_session_proxy(self):
        logger.info('Preparing for search..')
        proxy_list = get_proxies()
        for proxy in proxy_list:
            try:
                self.session.proxies = {'https': proxy}
                self.session.get('https://booking.uz.gov.ua/ru/')
                break
            except (SSLError, MaxRetryError):
                logger.debug('This proxy suck, try another')
                pass

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
    def form_seats_info(coach_types, prices):
        seats_info = []
        for ctype in coach_types:
            string = '{}: {} шт. {} грн'.format(ctype['title'], str(ctype['places']), prices[ctype['title']])
            seats_info.append(string)
        logger.debug(seats_info)

        return seats_info

if __name__ == '__main__':
    pass
