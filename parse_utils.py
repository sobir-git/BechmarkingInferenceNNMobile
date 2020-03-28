# parse benchmark result files (pseudo-csv files:)) and save as csv
import os

def parse(file):
    '''Parses benchmark result file.'''
    lines = file.readlines()
    # get the line number of the following line:
    # Operator-wise Profiling Info for Regular Benchmark Runs:
    line_number = lines.index('Operator-wise Profiling Info for Regular Benchmark Runs:\n')
    # skip the next line as it is this:
    # ============================== Run Order ==============================
    line_number += 1
    # get the nearest next line which is empty
    next_empty_line_number = lines.index('\n', line_number)

    # return all lines between
    return lines[line_number + 1:next_empty_line_number]


def parse_benchmark_results(input_filepaths, output_dir):
    '''
    Reads benchmark result files and parses them. Writes the new files
    in csv format in the output directory. Returns the list of output files.
    '''
    output_files = []
    # iterate over input files
    for filepath in input_filepaths:
        print('Parsing:', filepath)

        # open the file and parse it
        with open(filepath) as f:
            lines = parse(f)

        # extract just the filename(without extension)
        filename = os.path.basename(filepath).rsplit('.', maxsplit=1)[0]

        # write the parsed lines to file
        output_file = os.path.join(output_dir, filename + '.csv')
        with open(output_file, 'w') as f:
            f.write('\n'.join(lines))

        # add to results list
        output_files.append(output_file)

    print("Outputs written to:", os.path.abspath(output_dir))
    return output_files


def test_parse():
    # test the parse function
    test_str='''

Number of nodes executed: 1
============================== Summary by node type ==============================
node type, count, avg_ms, avg %, cdf %, mem KB, times called
AllocateTensors, 1, 0.029, 100%, 100%, 0, 1

Timings (microseconds): count=1 curr=29
Memory (bytes): count=0
1 nodes observed


Operator-wise Profiling Info for Regular Benchmark Runs:
============================== Run Order ==============================
node type, start, first, avg_ms, %, cdf%, mem KB, times called, name
CONV_2D, 0, 0.11, 0.0930388, 44.8994%, 44.8994%, 0, 1, [sequential_11/conv2d_33/Conv2D]:0
ELU, 0.0931277, 0.034, 0.0300884, 14.5203%, 59.4197%, 0, 1, [sequential_11/conv2d_33/Elu]:1
AVERAGE_POOL_2D, 0.123291, 0.026, 0.0272269, 13.1394%, 72.559%, 0, 1, [sequential_11/average_pooling2d_22/AvgPool]:2
CONV_2D, 0.150559, 0.03, 0.0309657, 14.9436%, 87.5027%, 0, 1, [sequential_11/conv2d_34/Conv2D]:3
ELU, 0.181571, 0.01, 0.0102094, 4.92694%, 92.4296%, 0, 1, [sequential_11/conv2d_34/Elu]:4
AVERAGE_POOL_2D, 0.191832, 0.003, 0.00362065, 1.74728%, 94.1769%, 0, 1, [sequential_11/average_pooling2d_23/AvgPool]:5
CONV_2D, 0.195491, 0.008, 0.00765769, 3.6955%, 97.8724%, 0, 1, [sequential_11/conv2d_35/Conv2D]:6
ELU, 0.203215, 0.001, 0.000868238, 0.419001%, 98.2914%, 0, 1, [sequential_11/conv2d_35/Elu]:7
FULLY_CONNECTED, 0.204145, 0.002, 0.00214613, 1.03569%, 99.3271%, 0, 1, [sequential_11/dense_22/MatMul]:8
ELU, 0.206331, 0.001, 0.000645791, 0.311651%, 99.6387%, 0, 1, [sequential_11/dense_22/Elu]:9
FULLY_CONNECTED, 0.207017, 0, 0.000406285, 0.196068%, 99.8348%, 0, 1, [sequential_11/dense_23/MatMul]:10
SOFTMAX, 0.207468, 0.001, 0.000342312, 0.165195%, 100%, 0, 1, [Identity]:11

============================== Top by Computation Time ==============================
node type, start, first, avg_ms, %, cdf%, mem KB, times called, name
CONV_2D, 0, 0.11, 0.0930388, 44.8994%, 44.8994%, 0, 1, [sequential_11/conv2d_33/Conv2D]:0
    '''

    from io import StringIO
    file = StringIO(test_str)
    lines = parse(file)
    assert len(lines) == 13


if __name__ == '__main__':
    test_parse()
