from .sina import go,zcfzb
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('hf_code', help='新浪财经hf_code', nargs='?', default='hf_CL')
    parser.add_argument('--zcfzb', help='资产负债表', nargs='?')
    args=parser.parse_args()
    if args.zcfzb:
        zcfzb(args.zcfzb)
    else:
        go(args.hf_code)
