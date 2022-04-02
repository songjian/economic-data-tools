from ast import arg
from .sina import go,zcfzb
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('hf_code', help='新浪财经hf_code', nargs='?', default='hf_CL')
    parser.add_argument('--zcfzb', help='资产负债表 例如: 600000', nargs='?')
    parser.add_argument('--year', help='年', nargs='?', default='part')
    args=parser.parse_args()
    if args.zcfzb:
        zcfzb(args.zcfzb, args.year)
    else:
        go(args.hf_code)
