from ast import arg
from .sina import go,zcfzb
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('hf_code', help='新浪财经hf_code', nargs='?', default='hf_CL')
    parser.add_argument('-z', '--zcfzb', action='store_true', help='资产负债表')
    parser.add_argument('--year', help='年', nargs='?', default='part')
    args=parser.parse_args()
    if args.zcfzb:
        zcfzb(args.hf_code, args.year)
    else:
        go(args.hf_code)
