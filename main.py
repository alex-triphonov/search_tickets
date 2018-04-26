import argparse
from time import sleep

from search_tickets.search_module import TrainTickets


def main(**kwargs):
    train_tickets = TrainTickets(kwargs['departure'], kwargs['destination'], kwargs['day'],
                                 kwargs['month'], kwargs['year'])
    for i in range(36):
        train_tickets.find_tickets()
        sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Checking urls for points of compromise with VirusTotal. 
            Warning! Check can take some time: 
            "Keep in mind that URLs sent using the API have the lowest scanning priority, 
            depending on VirusTotal's load, it may take several hours before the URL is scanned" (C)VirusTotal''')
    parser.add_argument('-dep', '--departure', type=str, help='Point of departure')
    parser.add_argument('-dest', '--destination', type=str, help='Your destination')
    parser.add_argument('-d', '--day', type=int, help='Day of the month')
    parser.add_argument('-m', '--month', type=int, help='<optional> Month number (1-12), default= current')
    parser.add_argument('-y', '--year', type=int, help='<optional> Year (4 digits), default= current')
    parser.add_argument('-b', '--booking', action='store_true', default=False, help='try to book you ticket')
    args = parser.parse_args()
    main(**vars(args))
