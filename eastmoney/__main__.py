from .eastmoney import _js
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stat', help='stat code', nargs='?', default='12')
    args=parser.parse_args()
    _js(stat=args.stat)