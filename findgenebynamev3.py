#!/usr/bin/env python3

'''
findgenebynamev3.py

This code is to be used with CLC csv output of "find broken pairs."  You can input the gene name of your choice, and the script will find all occurances of that gene in the input csv and return an output file with the first column (you will have to separate by ";" using text to columns in excel):
reference annotation
reference start
reference end
number of unique hits for the reference (if it was mapped in multiple locations, should only be 1 for non-specific mapping)
mate annonation
mate start
mate unique hits

the second column will be a tally of the number of times that entry occurs in the file.

If you want to make this code simplier, you can take out everything but the reference annotation and the mate annotation and it will count up the number of times a certain gene name occurs in pairing with a certain mate name.
'''

import csv
import sys

def search_for_gene(inputcsv, genename, outputcsv):

    uniquematchdict = {}

    with open(inputcsv, 'r') as fh:
        fhcsv = csv.reader(fh, delimiter=',')
        field_names_list = next(fhcsv)

        with open(outputcsv, 'a') as fh:
            writer = csv.writer(fh)
            writer.writerow(field_names_list)

        for entry in fhcsv:
            Ref_annotation = entry[4]

            if Ref_annotation == genename:
                with open(outputcsv, 'a') as fh:
                    writer = csv.writer(fh)
                    writer.writerow(entry)

    with open(outputcsv, 'r') as fh:
        fhcsv = csv.reader(fh, delimiter=',')
        next(fhcsv)

        for entry in fhcsv:
            Ref_start = int(entry[1])
            Ref_end = int(entry[2])
            Ref_hits = int(entry[3])
            Ref_annotation = entry[4]
            Mate_start = int(entry[6])
            Mate_end = int(entry[7])
            Mate_hits = int(entry[8])
            Mate_annotation = entry[9]

            alltogether = Ref_annotation + ";%d" % (Ref_start) + ";%d" % (Ref_end) + ";%d" %(Ref_hits) + ";" + Mate_annotation + ";%d" % (Mate_start) + ";%d" % (Mate_end) + ";%d" %(Mate_hits)

            if alltogether in uniquematchdict:
                uniquematchdict[alltogether] += 1
            else:
                uniquematchdict[alltogether] = 1

    with open(outputcsv, 'w') as fh:
        writer = csv.writer(fh)
        for key, value in uniquematchdict.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    if len(sys.argv) == 4:
         search_for_gene(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
         print("Usage: findgenebyname.py input.csv genename output.csv")
         sys.exit(0)
