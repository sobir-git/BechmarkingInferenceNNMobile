'''This script will run benchmarks on a given set of tflite models.

Example usage:
profiler --models-dir "tflite_models" --output-dir "results"
'''

import argparse
import os

from benchmark_utils import run_benchmarks
from parse_utils import parse_benchmark_results
from utils import abs_listdir

parser = argparse.ArgumentParser()
parser.add_argument("--models-dir", help="Directory where models reside", required=True)
parser.add_argument("--output-dir", help="Directory in which profiling results will be saved", required=True)
parser.add_argument("--tf-path", help="Path to tensorflow directory",
                    default="/home/loveml/Downloads/tensorflow")
parser.add_argument("-ki", "--keep-intermediate", action="store_true",
                    help="Keep intermediate benchmark outputs")
args = parser.parse_args()

# make sure output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# get all files in models directory having .tflite extension
filepaths = list(filter(lambda s: s.endswith('.tflite'), abs_listdir(args.models_dir)))

# run benchmarks and get output files
benchmark_output_files = run_benchmarks(tf_path=args.tf_path, filepaths=filepaths, output_dir=args.output_dir)

# parse benchmark output and write them in .csv files
csv_results = parse_benchmark_results(benchmark_output_files, output_dir=args.output_dir)

# remove intermediate benchmark output files
if not args.keep_intermediate:
    for f in benchmark_output_files:
        os.remove(f)
