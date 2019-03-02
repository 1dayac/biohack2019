import sys
import os
import re

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("\nUsage:\npython parser.py {input_file}\npython parser.py {input_file} {output_file}")
    sys.exit(-1)

with open(sys.argv[1]) as file:
    lines = file.readlines()
    if len(sys.argv) == 3:
        output_file = open(sys.argv[2], 'w')
    else:
        output_file = open(os.path.splitext(sys.argv[1])[0] + ".vcf", 'w')
    for line_num, line in enumerate(lines):
        if not line.startswith("NODE"):
            continue
        node = line.split('\t')
        chromosome = node[2]
        elements = re.findall(r"[0-9]+\w", node[5])

        ref_pos = int(node[3])
        seq_pos = 0

        for elem in elements:
            shift = int(elem[:-1])
            if elem[-1] == "S":
                seq_pos += shift
            elif elem[-1] == "N":
                ref_pos += shift
            elif elem[-1] == "M":
                seq_pos += shift
                ref_pos += shift
            elif elem[-1] == "I":
                sequence = node[9][seq_pos:seq_pos + shift]
                output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    line_num,
                    chromosome,
                    ref_pos,
                    ref_pos,
                    "INS",
                    sequence,
                    node[0],
                    seq_pos + 1))
                seq_pos += shift
            elif elem[-1] == "D":
                output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    line_num,
                    chromosome,
                    ref_pos,
                    ref_pos + shift - 1,
                    "DEL",
                    "-",
                    node[0],
                    seq_pos + 1))
                ref_pos += shift
