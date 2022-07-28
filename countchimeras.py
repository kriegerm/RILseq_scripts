#!/usr/bin/env python3

'''
countchimeras.py

This script takes in the chimeric mapping output file of RILseq 0.74 and produces an output file with only the chimeric reads. 
It also counts up and prints the total chimeric and and single reads.
'''

import sys

def sortoutput (input, output):
    
    chimeracounter = 0
    singlecounter = 0

    with open(input, 'r') as fh:
        for line in fh:
            holdine =line
            holdine = holdine.strip().split("\t")
            if holdine[-1] == "chimera":
                with open(output, 'a') as out:
                    out.write(line)
                    chimeracounter = chimeracounter + 1
            if holdine[-1] == "single":
                singlecounter = singlecounter + 1
                
    print("There are %d chimeric reads in this file." %(chimeracounter))
    print("there are %d single reads in this file." %(singlecounter))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        sortoutput(sys.argv[1], sys.argv[2])
    else:
        print("Usage: map_chimeric_fragments_output.txt, output.txt ")
        sys.exit(0)
