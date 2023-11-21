import argparse
import importlib


def params_parser(args):
    config = dict()
    config['dataset'] = args.dataset
    config['stu_num'] = args.stu_num
    config['least_respone_num'] = args.least_respone_num

    method = importlib.import_module(f'{args.dataset}.preprocess')
    method.run(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, choices=['XES3G5M', 'AAAI2023', 'EdNet', 'EDM2023-CUP', 'Assist19-20', 'Assist20-21'], required=True,
                        help='Choose the dataset: XES3G5M, AAAI2023, EdNet, EDM2023-CUP, Assist19-20 or Assist20-21')
    parser.add_argument('--stu_num', type=int, default=8000)
    parser.add_argument('--least_respone_num', type=int, default=80)
    args = parser.parse_args()
    params_parser(args)
