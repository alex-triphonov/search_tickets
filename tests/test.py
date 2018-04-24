import unittest

import logging
from datetime import datetime

from search_tickets.search_module import TrainTickets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

THIS_DAY = datetime.now().day
THIS_MONTH = datetime.now().month
THIS_YEAR = datetime.now().year
GOLDEN_DATE = ':'.join(['{0:02d}'.format(THIS_DAY), '{0:02d}'.format(THIS_MONTH), str(THIS_YEAR)])


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


if __name__ == '__main__':
    unittest.main()