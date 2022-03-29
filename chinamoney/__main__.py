from .lpr import lpr
from .fx import fx
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command', help='调用的命令', nargs='?', choices=['lpr', 'fx'], default='lpr')
    args=parser.parse_args()
    if args.command == 'lpr':
        lpr()
    elif args.command == 'fx':
        fx()
