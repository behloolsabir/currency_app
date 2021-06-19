import argparse
import warnings
import yaml

from src.provider import source1, source2
from src import utils

warnings.filterwarnings("ignore")


if __name__ == '__main__':
    # capturing all valid currencies
    with open('src/config.yaml') as f:
        try:
            config_dict = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('-s',
                           '--sell',
                           dest='operations',
                           action='append_const',
                           const='sell')
    my_parser.add_argument('-b',
                           '--buy',
                           dest='operations',
                           action='append_const',
                           const='buy',
                           help='Set a switch to true')
    my_parser.add_argument(
        'base',
        action='store',
        nargs=1,
        choices=config_dict['valid_currencies'],
        type=str.upper,
        help='Enter base currency from the valid currency codes')

    args = my_parser.parse_args()
    base = args.base[0].lower()

    providers = [source1(), source2()]
    for operation in args.operations:
        print(f"Finding best {operation} value for {base}")
        utils.transact(providers, base, operation)
