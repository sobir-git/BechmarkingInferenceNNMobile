'''This script will run benchmarks on a given set of tflite models.

Example usage:
benchmark_parser input-dir output-dir
'''

import argparse
import os

from parse_utils import parse_benchmark_results
from utils import abs_listdir

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Directory in which benchmark outputs reside")
parser.add_argument("output_dir", help="Directory in which parsed results will be saved")
args = parser.parse_args()

# get all benchmark files
benchmark_output_files = abs_listdir(args.input_dir)

# make sure output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# parse benchmark output and write them in .csv files
csv_results = parse_benchmark_results(benchmark_output_files, output_dir=args.output_dir)
