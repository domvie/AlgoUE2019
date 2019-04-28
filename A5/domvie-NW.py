#!/usr/bin/python3

# AlgoUE BIOINF20
# A5 Needleman-Wunsch algorithm
# Dominic Viehböck

import sys
from sys import stdin
from Bio import SeqIO
from argparse import ArgumentParser

parser = ArgumentParser(description="Needleman-Wunsch (NW) algorithm for global alignment of two sequences")
parser.add_argument("--match", type=int, default=1, help="Enter matching score for sequence alignment, default = 1")
parser.add_argument("--mismatch", type=int, default=-1, help="Enter mismatching score for "
                                                             "sequence alignment, default = -1")
parser.add_argument("--gap", type=int, default=-2, help="Enter gap penalty, default = -2")
args = parser.parse_args()

matchscore = args.match
mismatchscore = args.mismatch
gapscore = args.gap

def scoring_function(pos1, pos2):
    """returns score value for given pair"""
    if pos1 == pos2:
        return matchscore
    if pos1 == '-' or pos2 == '-':
        return gapscore
    return mismatchscore

def similarity(sequence1, sequence2):
    """builds a similarity matrix"""
    m = len(sequence1)
    n = len(sequence2)

    # empty matrix
    scoring_matrix = []
    for j in range(0, m + 1):
        scoring_matrix.append([])
    for j in scoring_matrix:
        for i in range(0, n + 1):
            j.append(0)

    # build scores, fill matrix
    for i in range(0, m + 1):
        scoring_matrix[i][0] = gapscore * i
    for j in range(0, n + 1):
        scoring_matrix[0][j] = gapscore * j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = scoring_matrix[i - 1][j - 1] + scoring_function(sequence1[i - 1], sequence2[j - 1])
            delete = scoring_matrix[i - 1][j] + gapscore
            insert = scoring_matrix[i][j - 1] + gapscore
            scoring_matrix[i][j] = max(match, delete, insert)

    return scoring_matrix

def alignment(sequence1, sequence2, score):
    """takes two sequences and a scoring matrix and returns aligned sequences"""
    i = len(sequence1)
    j = len(sequence2)
    alignedseq1 = ""
    alignedseq2 = ""
    while True:
        if i == 0 and j == 0:
            break
        if j == 0:
            alignedseq1 += sequence1[i - 1]
            alignedseq2 += '-'
            i -= 1
            continue
        if i == 0:
            alignedseq1 += '-'
            alignedseq2 += sequence2[j - 1]
            j -= 1
            continue
        if score[i][j] == score[i-1][j] + gapscore:
            alignedseq1 += sequence1[i - 1]
            alignedseq2 += '-'
            i -= 1
        elif score[i][j] == score[i][j-1] + gapscore:
            alignedseq1 += '-'
            alignedseq2 += sequence2[j - 1]
            j -= 1
        elif score[i][j] == score[i-1][j-1] + scoring_function(sequence1[i - 1], sequence2[j - 1]):
            alignedseq1 += sequence1[i - 1]
            alignedseq2 += sequence2[j - 1]
            i -= 1
            j -= 1

    return alignedseq1, alignedseq2

def calculate(alignedseq1, alignedseq2):
    """calculates score and similarity for two given alignments"""
    # reverse sequences
    alignedseq1 = alignedseq1[::-1]
    alignedseq2 = alignedseq2[::-1]

    # calculate similarity, score and aligned sequences
    score = 0
    sim = 0

    for i in range(0, len(alignedseq1)):
        if alignedseq1[i] == alignedseq2[i]:
            sim += 1
            score += scoring_function(alignedseq1[i], alignedseq2[i])
        elif alignedseq1[i] != alignedseq2[i] and alignedseq1[i] != '-' and alignedseq2[i] != '-':
            score += scoring_function(alignedseq1[i], alignedseq2[i])
        else:
            score += gapscore

    sim = int(float(sim) / len(alignedseq1) * 100)

    return sim, score

def NMW(sequence1, sequence2, seqID1, seqID2):
    """performs NMW pairwise global sequence alignment and prints out in CLUSTAL format"""
    scoring_matrix = similarity(sequence1, sequence2)
    alignedseq1, alignedseq2 = alignment(sequence1, sequence2, scoring_matrix)
    asteriks = ""
    for i in range(0, len(alignedseq1)):
        if alignedseq1[i] is alignedseq2[i]:
            asteriks += "*"
        else:
            asteriks += " "
    s = alignedseq1[::-1]
    t = alignedseq2[::-1]
    asteriks = asteriks[::-1]
    n = len(sequence1) / 60
    # print out in CLUSTAL format
    print("CLUSTAL\n\n")
    for i in range(1, int(n)+2):
        if i == int(n)+2 and n > int(n):
            print(seqID1, s[60 * (i - 1)::])
            print(seqID2, t[60 * (i - 1)::])
            print("".ljust(len(seqID1)), asteriks[60 * (i - 1)::], "\n")
            break
        print(seqID1, s[60*(i-1):60*i])
        print(seqID2, t[60*(i-1):60*i])
        print("".ljust(len(seqID1)), asteriks[60*(i-1):60*i], "\n")

    sim, score = calculate(alignedseq1, alignedseq2)
    sys.stderr.write(str(sim))

def main():
    seqIDs = []
    sequences = []
    #read from STDIN
    if sys.stdin.isatty():
        parser.print_help()
    for Sequence in SeqIO.parse(stdin, "fasta"):
        seqIDs.append(str(Sequence.id))
        sequences.append(str(Sequence.seq).lower())

    sequence1 = sequences[0]
    sequence2 = sequences[1]
    seqID1 = seqIDs[0]
    seqID2 = seqIDs[1]
    NMW(sequence1, sequence2, seqID1, seqID2)

if __name__ == "__main__":
    main()