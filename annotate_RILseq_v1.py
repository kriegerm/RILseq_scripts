#!/usr/bin/env python3
import sys
import csv

'''
annotate_RILseq_v1.py
UPDATE: v1 1/27/2021

INPUT: Feature table CSV with the following columns (example first row included)
genomic_accession	seq_type	start	end	strand	feature type	symbol	locus_tag	name
CP041233.1	       chromosome	   1	139   +	         CDS	    dnaA	FG183_00005	chromosomal replication initiator protein DnaA

RILSeq results table .csv in the following format with the conditions: the RNA entry number and average column is manually added in excel, and only one RNA pair is annotated at a time. The RNA entry number will help you keep track of which entry is which so you can match them up manually with the output.
Entry	RNA2 chromosome	    Start of RNA2 last read	Start of RNA2 first read	Average Start of RNA2	RNA2 strand
1	    CP041234.1plasmid	43086	                43127	                    43107	                -
2	    CP041233.1chromosome307524	                307531	                    307528	                -

OUTPUT: You will get a .csv file as output, you have to manually "Find > Replace" all the "[", "]", and "'" becaus I was too lazy to figure out how to remove those in the code. It's easy with excel though.
If a hit has more than one gene that it's annotated in, you'll get multiple entires in each line for the multiple genes.

'''

def annotate_RILseq(featuretableCSV, RILseqresults, output):
    #stuff for the big feature table csv file
    assembly =[]
    seqtype = []
    start = []
    end = []
    featuretype = []
    strand = []
    symbol = []
    locustag = []
    name = []

    #stuff for the RIL seq output
    RNAentrynumber = []
    RNA_chromosome = []
    RNAfirst = []
    RNAlast = []
    RNAaverage =[]
    RNAstrand = []


    with open(featuretableCSV, 'r') as fh:
        fhcsv = csv.reader(fh, delimiter='\t') ##I REALIZED THAT IF I MADE IT delimiter=',' THEN I WOULDN'T HAVE TO DO ALL THE STRING STUFF BUT OH WELL
        next(fhcsv)
        for entry in fhcsv:
            entry = str(entry[0])
            entry = entry.rstrip("']")
            entry = entry.lstrip("['")
            entry = entry.split(",")

            assembly.append(entry[0])
            seqtype.append(entry[1])
            start.append(entry[2])
            end.append(entry[3])
            strand.append(entry[4])
            featuretype.append(entry[5])
            symbol.append(entry[6])
            locustag.append(entry[7])
            name.append(entry[8])

            #insert a check here to make sure all the lists are of equal length


    with open(RILseqresults, 'r') as RILfh:
        rilcsv = csv.reader(RILfh, delimiter = '\t')
        next(rilcsv)
        counter = 0
        for line in rilcsv:
            counter = counter + 1
            line = str(line)
            line = line.rstrip("']")
            line= line.lstrip("['")
            line = line.split(",")

            RNAentrynumber.append(line[0])
            RNA_chromosome.append(line[1])
            RNAfirst.append(int(line[2]))
            RNAlast.append(int(line[3]))
            RNAaverage.append(line[4])
            RNAstrand.append(line[5])


        # insert a check here to make sure all the lists are of equal length
        if len(RNAentrynumber) != len(RNA_chromosome) != len(RNAfirst) != len(RNAlast) != len(RNAaverage) != len(RNAstrand):
            print("ERROR: The lists generated from the RILseq results input are not of equal length.")

    results_number = []
    results_assembly =[]
    results_seqtype = []
    results_start = []
    results_end = []
    results_featuretype = []
    results_strand = []
    results_symbol = []
    results_locustag = []
    results_name = []


    for value in range (0, len(RNA_chromosome)):
        average = int(RNAaverage[value])

        saverlist_number = []
        saverlist_assembly = []
        saverlist_seqtype = []
        saverlist_start = []
        saverlist_end = []
        saverlist_featuretype = []
        saverlist_strand = []
        saverlist_symbol = []
        saverlist_locustag = []
        saverlist_name = []

        for location in range (0, len(assembly)):
            if seqtype[location] in RNA_chromosome[value]: #this checks if it's a chromosome or plasmid. If there are multiple chromosomes you might have to fiddle with this to make it specific.
                if average in range(int(start[location]), int(end[location])):

                    saverlist_number.append(RNAentrynumber[value])
                    saverlist_assembly.append(assembly[location])
                    saverlist_seqtype.append(seqtype[location])
                    saverlist_start.append(start[location])
                    saverlist_end.append(end[location])
                    saverlist_featuretype.append(featuretype[location])
                    saverlist_strand.append(strand[location])
                    saverlist_symbol.append(symbol[location])
                    saverlist_locustag.append(locustag[location])
                    saverlist_name.append(name[location])


        results_number.append(saverlist_number)
        results_assembly.append(saverlist_assembly)
        results_seqtype.append(saverlist_seqtype)
        results_start.append(saverlist_start)
        results_end.append(saverlist_end)
        results_featuretype.append(saverlist_featuretype)
        results_strand.append(saverlist_strand)
        results_symbol.append(saverlist_symbol)
        results_locustag.append(saverlist_locustag)
        results_name.append(saverlist_name)

    if len(results_featuretype) != len(RNAentrynumber):
        print("ERROR: Unequal number of results found compared to RILseq results input.")


    with open(output, 'a') as fh:
        writer = csv.writer(fh)
        header = ["RNA Number", "Genome", "SeqType", "Gene Start", "Gene End", "Gene Feature Type", "Gene Strand", "Gene Symbol", "Gene Locus Tag", "Gene Name"]
        writer.writerow(header)
        for value in range(0, len(results_number)):
            saver = []
            saver.append(results_number[value])
            saver.append(results_assembly[value])
            saver.append(results_seqtype[value])
            saver.append(results_start[value])
            saver.append(results_end[value])
            saver.append(results_featuretype[value])
            saver.append(results_strand[value])
            saver.append(results_symbol[value])
            saver.append(results_locustag[value])
            saver.append(results_name[value])
            writer.writerow(saver)




if __name__ == '__main__':
    if len(sys.argv) == 4:
        annotate_RILseq(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("")
        sys.exit(0)
