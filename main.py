#!/usr/bin/env python3

from game.region import Region
from json import dumps
import argparse

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
    if(args.compressed):
        print(r.to_compressed_json(show_all=args.all))
    if(args.json):
        print(r.to_json(show_all=args.all))
    if(args.region):
        print(r)


if __name__ == '__main__':
    main()
