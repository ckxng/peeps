#!/usr/bin/env python3

import argparse
from threading import Thread
from time import sleep

from lib.region import Region


def parse_args():
    parser = argparse.ArgumentParser(
        prog='peeps',
        description='Simulate a world of little peeps',
        epilog='All your base are belong to us.',
    )
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-r', '--region', action='store_true')
    parser.add_argument('-j', '--json', action='store_true')
    parser.add_argument('-c', '--compressed', action='store_true')
    parser.add_argument('-s', '--seed', type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    r = Region(seed=args.seed)

    step = 0
    while True:
        print("step", step)
        if args.compressed:
            print(r.to_compressed_json(show_all=args.all))
        if args.json:
            print(r.to_json(show_all=args.all))
        if args.region:
            print(r)

        r.step()
        step += 1
        sleep(1)


if __name__ == '__main__':
    main_th = Thread(target=main).start()
