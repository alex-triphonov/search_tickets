import unittest

import logging

from search_tickets.search_module import TrainTickets
from tests.golden_values import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestTrainTickets(unittest.TestCase):

    def test_validate(self):

        train = TrainTickets('прив', 'ет', THIS_DAY)
        # test complete wrong cities input
        with self.assertRaises(ValueError) as context:
            train.validate('odessa', 'кие3в', 7)
            self.assertTrue('отправления' in str(context.exception))
            train.validate('киев', 'dfg45', 7)
            self.assertTrue('назначения' in str(context.exception))
        # test cutting the crap out of cities input
        crap_cities = train.validate('киев', 'оде23,сcса', THIS_DAY)
        self.assertEqual(crap_cities, ('Киев', 'Одесса', GOLDEN_DATE))
        # test crap dates
        with self.assertRaises(ValueError) as context:
            # wrong day
            train.validate('Киев', 'Одесса', 32, 15)
            self.assertTrue('Неверно введена дата' in str(context.exception))
            # wrong month
            train.validate('Киев', 'Одесса', 18, 15)
            self.assertTrue('Неверно введен месяц' in str(context.exception))
            # wrong year
            train.validate('Киев', 'Одесса', 18, 11, 2022)
            self.assertTrue('Неверно введен год' in str(context.exception))
            # past date
            train.validate('Киев', 'Одесса', 1, 3)
            self.assertTrue('Указанная дата ведет в прошлое' in str(context.exception))

        just_date = train.validate('киев', 'одесса', datetime.now().day)
        self.assertEqual(just_date, ('Киев', 'Одесса', GOLDEN_DATE))


    # @patch()
    # def test_search_for_station_id(self):


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)

if __name__ == '__main__':
    unittest.main()