import argparse


def get_argparser():
    parser = argparse.ArgumentParser(description='jupyternvccPlugin params')
    parser.add_argument('--compile', default=False, action='store_true')
    parser.add_argument('--run', default=False, action='store_true')
    parser.add_argument('--cudart', default="static", type=str)
    parser.add_argument('--std', default="c++14", type=str)
    parser.add_argument('--threads', default=1, type=int)
    parser.add_argument('-arch', default="sm_70", type=str)
    parser.add_argument('-t', '--timeit', action='store_true', help='flag to return timeit result instead of stdout')
    return parser

def print_out(out: str):
    for l in out.split('\n'):
        print(l)