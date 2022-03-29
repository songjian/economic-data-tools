from .sina import go
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('hf_code', help='新浪财经hf_code', nargs='?', default='hf_CL')
    args=parser.parse_args()
    go(args.hf_code)
