from .stock import overview,profile
from .bond import kzhgszq
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('product_type', help='证券类型，stock, bond', nargs='?', default='stock')
    parser.add_argument('command', help='命令', nargs='?', default='overview')
    parser.add_argument('--code', help='证券代码', nargs='?')
    parser.add_argument('--date', help='查询日期，格式：20220329', nargs='?')
    parser.add_argument('--product_code', help='产品代码 01 A股, 02 B股, 03 科创, 11 股票回购, 17 汇总股票', nargs='?', default='01,02,03,11,17')
    args=parser.parse_args()

    if args.product_type == 'stock':
        if args.command == 'overview':
            overview(args.date, args.product_code)
        elif args.command == 'profile':
            profile(args.code)
