import argparse
from time import sleep

from search_tickets.search_module import TrainTickets


def main(**kwargs):
    train_tickets = TrainTickets(kwargs.get('departure'), kwargs.get('destination'), kwargs.get('day'),
                                 kwargs.get('month'), kwargs.get('year'), kwargs.get('types'), kwargs.get('specific'),
                                 kwargs.get('exclude'))
    for i in range(36):
        train_tickets.find_tickets()
        sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Search your tickets! Enter departure, destination and day if you're searching for tickets for 
        current month or specify date. Also you can specify search conditions""")
    parser.add_argument('-dep', '--departure', type=str, help='Point of departure', required=True)
    parser.add_argument('-dest', '--destination', type=str, help='Your destination', required=True)
    parser.add_argument('-d', '--day', type=int, help='Day of the month', required=True)
    parser.add_argument('-m', '--month', type=int, help='<optional> Month number (1-12), default= current')
    parser.add_argument('-y', '--year', type=int, help='<optional> Year (4 digits), default= current')
    parser.add_argument('-t', '--types', nargs='*', default=None, help='Desired type of coaches e.g. (п к л с1 с2)')
    parser.add_argument('-s', '--specific', nargs='*', default=None, help='Find only specific trains e.g. (148Ш 224К)')
    parser.add_argument('-e', '--exclude', nargs='*', default=None, help='Exclude specific trains e.g. (148Ш 224К)')
    # parser.add_argument('-b', '--booking', action='store_true', default=False, help='try to book you ticket')
    args = parser.parse_args()
    main(**vars(args))
    # main(departure='одесса', destination='киев', day=2, month=5, types=['к', 'л'])
