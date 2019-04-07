#!/usr/bin/env python3

# Algo UE A4 Dominic Viehböck
# BIOINF20 SS19
# results: rmHVD_10_10: 67.76; rmHVD_999_10: 7198.31

import sys


def MatrixReader(direction):
    directionList = []
    i = 0
    if direction == "vertical":
        matrix = open(file, "r")
        for line in matrix:
            if line.startswith(" "):
                temp = line.split()
                directionList.append([])
                for number in temp:
                    directionList[i].append(float(number))
                i += 1
            if line.startswith("-"):
                break
    elif direction == "horizontal":
        matrix = open(file, "r")
        for line in matrix:
            if line.startswith(" "):
                temp = line.split()
                directionList.append([])
                for number in temp:
                    directionList[i].append(float(number))
                i += 1
            if line.startswith("G_right"):
                directionList.clear()
                i = 0

    elif direction == "diagonal":
        matrix = open(file, "r")
        for line in matrix:
            if line.startswith(" "):
                temp = line.split()
                directionList.append([])
                for number in temp:
                    directionList[i].append(float(number))
                i += 1
            if line.startswith("G_diag"):
                directionList.clear()
                i = 0

    matrix.close()
    return directionList


def MTP(file):
    down = MatrixReader("vertical")
    right = MatrixReader("horizontal")
    diag = MatrixReader("diagonal")
    length = len(down[0])
    mtpmatrix = []

    for i in range(length - 1):
        if len(down[i]) != length:
            print("Something is wrong with G_down matrix")

    for i in range(length):
        if len(right[i]) != length - 1:
            print("Something is wrong with G_right matrix")
    # fill empty NxN matrix
    for j in range(0, length):
        mtpmatrix.append([])
    for j in mtpmatrix:
        for i in range(0, length):
            j.append(0)
    # fill first column
    mtpmatrix[0][0] = 0
    for i in range(0, length - 1):
        mtpmatrix[i + 1][0] = mtpmatrix[i][0] + down[i][0]
    # fill first row
    for j in range(0, length - 1):
        mtpmatrix[0][j + 1] = mtpmatrix[0][j] + right[0][j]
    # apply algorithm
    for i in range(1, length):
        for j in range(1, length):
            mtpmatrix[i][j] = max(mtpmatrix[i - 1][j] + down[i - 1][j],
                                  mtpmatrix[i][j - 1] + right[i][j - 1],
                                  mtpmatrix[i-1][j-1] + diag[i-1][j-1])

    return mtpmatrix[length - 1][length - 1]


# Execute and print result

file = sys.argv[1]
score = MTP(file)
print(score)
