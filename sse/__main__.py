from .stock import overview,profile
from .bond import kzhgszq
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('product_type', help='证券类型，stock, bond', nargs='?', default='stock')
    parser.add_argument('command', help='命令', nargs='?', default='overview')
    parser.add_argument('--code', help='证券代码', nargs='?')
    args=parser.parse_args()

    if args.product_type == 'stock':
        if args.command == 'overview':
            overview('20220329')
        elif args.command == 'profile':
            profile(args.code)
