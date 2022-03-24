import sys
from .netease import historical_prices

if __name__ == '__main__':
    print(historical_prices(sys.argv[1], sys.argv[2], sys.argv[3])) # 例: python -m netease 0601318 20220323 20220323