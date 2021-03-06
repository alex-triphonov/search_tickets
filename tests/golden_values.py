from datetime import datetime

THIS_DAY = datetime.now().day
THIS_MONTH = datetime.now().month
THIS_YEAR = datetime.now().year
GOLDEN_DATE = ':'.join(['{0:02d}'.format(THIS_DAY), '{0:02d}'.format(THIS_MONTH), str(THIS_YEAR)])

TRAINS_OK_RESP = {'data': {'list': [{'allowBooking': 1,
                                     'allowPrivilege': 0,
                                     'allowRoundtrip': 1,
                                     'allowStudent': 1,
                                     'category': 0,
                                     'child': {'maxDate': '2018-04-26', 'minDate': '2004-04-29'},
                                     'from': {'code': '2200001',
                                              'date': 'суббота, 28.04.2018',
                                              'sortTime': 1524872100,
                                              'srcDate': '2018-04-28',
                                              'station': 'Киев-Пассажирский',
                                              'stationTrain': 'Минск-Пассажирский',
                                              'time': '02:35'},
                                     'isCis': 0,
                                     'isEurope': 0,
                                     'num': '094Б',
                                     'to': {'code': '2208001',
                                            'date': 'суббота, 28.04.2018',
                                            'sortTime': 1524908280,
                                            'station': 'Одесса-Главная',
                                            'stationTrain': 'Одесса-Главная',
                                            'time': '12:38'},
                                     'travelTime': '10:03',
                                     'types': [{'id': 'П',
                                                'letter': 'П',
                                                'places': 24,
                                                'title': 'Плацкарт'},
                                               {'id': 'К',
                                                'letter': 'К',
                                                'places': 104,
                                                'title': 'Купе'}]},
                                    {'allowBooking': 1,
                                     'allowPrivilege': 0,
                                     'allowRoundtrip': 1,
                                     'allowStudent': 1,
                                     'category': 0,
                                     'child': {'maxDate': '2018-04-26', 'minDate': '2004-04-29'},
                                     'from': {'code': '2200001',
                                              'date': 'суббота, 28.04.2018',
                                              'sortTime': 1524890280,
                                              'srcDate': '2018-04-28',
                                              'station': 'Киев-Пассажирский',
                                              'stationTrain': 'Киев-Пассажирский',
                                              'time': '07:38'},
                                     'isCis': 0,
                                     'isEurope': 0,
                                     'num': '223К',
                                     'to': {'code': '2208001',
                                            'date': 'суббота, 28.04.2018',
                                            'sortTime': 1524926460,
                                            'station': 'Одесса-Главная',
                                            'stationTrain': 'Одесса-Главная',
                                            'time': '17:41'},
                                     'travelTime': '10:03',
                                     'types': [{'id': 'Л',
                                                'letter': 'Л',
                                                'places': 24,
                                                'title': 'Люкс'},
                                               {'id': 'К',
                                                'letter': 'К',
                                                'places': 104,
                                                'title': 'Купе'}]},
                                    ]}}

NO_TRAINS_RESP = {'data': {'list': [{'allowBooking': 1,
                                     'allowPrivilege': 0,
                                     'allowRoundtrip': 1,
                                     'allowStudent': 1,
                                     'category': 0,
                                     'child': {'maxDate': '2018-04-26', 'minDate': '2004-04-29'},
                                     'from': {'code': '2200001',
                                              'date': 'суббота, 28.04.2018',
                                              'sortTime': 1524872100,
                                              'srcDate': '2018-04-28',
                                              'station': 'Киев-Пассажирский',
                                              'stationTrain': 'Минск-Пассажирский',
                                              'time': '02:35'},
                                     'isCis': 0,
                                     'isEurope': 0,
                                     'num': '094Б',
                                     'to': {'code': '2208001',
                                            'date': 'суббота, 28.04.2018',
                                            'sortTime': 1524908280,
                                            'station': 'Одесса-Главная',
                                            'stationTrain': 'Одесса-Главная',
                                            'time': '12:38'},
                                     'travelTime': '10:03',
                                     'types': []},
                                    {'allowBooking': 1,
                                     'allowPrivilege': 0,
                                     'allowRoundtrip': 1,
                                     'allowStudent': 1,
                                     'category': 0,
                                     'child': {'maxDate': '2018-04-26', 'minDate': '2004-04-29'},
                                     'from': {'code': '2200001',
                                              'date': 'суббота, 28.04.2018',
                                              'sortTime': 1524890280,
                                              'srcDate': '2018-04-28',
                                              'station': 'Киев-Пассажирский',
                                              'stationTrain': 'Киев-Пассажирский',
                                              'time': '07:38'},
                                     'isCis': 0,
                                     'isEurope': 0,
                                     'num': '223К',
                                     'to': {'code': '2208001',
                                            'date': 'суббота, 28.04.2018',
                                            'sortTime': 1524926460,
                                            'station': 'Одесса-Главная',
                                            'stationTrain': 'Одесса-Главная',
                                            'time': '17:41'},
                                     'travelTime': '10:03',
                                     'types': []},
                                    ]}}
