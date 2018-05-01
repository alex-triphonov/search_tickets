import requests


class TelegramMsg:
    def __init__(self, chat_id='122357622'):
        self.token = '555537404:AAGfWmueXxhPwrDA5ADuR8HIzzaYaeOGNek'
        self.chat_id = chat_id

    def send_message(self, msg):
        requests.post(
            url='https://api.telegram.org/bot' + self.token + '/sendMessage',
            data={'chat_id': self.chat_id, 'text': msg, 'parse_mode': 'HTML'}
        )

    def send_available_trains(self, available_trains, route, time):
        tickets_data = ['— Поезд № {}, отправление в {}, прибытие в {}, билеты в наличии: {}\n'.format(
            train['train_num'], train['dep_time'], train['arr_time'],
            ', '.join(train['seats'])
        ) for train in available_trains]

        html = """
        <strong>{} на {}</strong>\n<code>найдены билеты на поезда:</code>\n{}
        """.format(route, time, '\n'.join(tickets_data))

        requests.post(
            url='https://api.telegram.org/bot' + self.token + '/sendMessage',
            data={'chat_id': self.chat_id, 'text': html, 'parse_mode': 'HTML'}
        )

if __name__ == '__main__':
    pass
    a = [{'arr_time': '17:41',
          'dep_time': '07:38',
          'seats': ['Люкс: 20 шт', 'Купе: 74 шт'],
          'train_num': '223К',
          'travel_time': '10:03'},
         {'arr_time': '17:41',
          'dep_time': '07:38',
          'seats': ['Люкс: 20 шт', 'Купе: 74 шт'],
          'train_num': '223К',
          'travel_time': '10:03'}
         ]
    t = TelegramMsg()
    t.send_available_trains(a, 'Киев-Одесса', '29-04-2018')
