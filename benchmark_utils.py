import os
import subprocess
from tqdm import tqdm


def run_benchmarks(tf_path, filepaths, output_dir):
    '''
    Benchmark tflite models and write the results in a directory.
    Returns the list of output files.
    '''
    # path to benchmark tool binary
    benchmarktool = os.path.join(tf_path, "bazel-bin/tensorflow/lite/tools/benchmark/benchmark_model")

    # convert to absolute output path
    output_dir = os.path.abspath(output_dir)
    output_files = []
    for filepath in tqdm(filepaths):
        # create a name for csv output file
        model_filename = os.path.basename(filepath)

        # get the part without extension
        model_name = model_filename.rsplit('.', maxsplit=1)[0]
        output_file = os.path.join(output_dir, model_name)
        output_files.append(output_file)

        # create the shell arguments for execution
        argv = [benchmarktool,
                f"--graph={filepath}",
                "--enable_op_profiling=true",
                f"--profiling_output_csv_file={output_file}"]

        # execute the shell command
        print("Running:", ' \\\n'.join(argv))
        process = subprocess.Popen(argv,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # get the outputs and print them
        stdout, stderr = process.communicate()
        print(stdout.decode())
        print(stderr.decode())

    return output_files
