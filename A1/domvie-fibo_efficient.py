#!/usr/bin/env python3

#AlgoUE BIOINF20
#A1 - Fibonacci Zahlen Methoden
#Dominic Viehböck

import sys
from datetime import datetime
from argparse import ArgumentParser

# Argumentparser
parser = ArgumentParser(description="Script to calculate the nth Fibonacci number (-n []) or print out all Fibonacci numbers up to the nth (--all)")

# positional arguments/flags
parser.add_argument("-n", type=int, help="nth Fibonacci number to calculate")
parser.add_argument("--all", action="store_true", help="Print all Fibonacci numbers up to n including their runtime")

args = parser.parse_args()

printAll = False # Standardwerte
n = 10

if not args.n and not args.all:
    print("Keine Parameter angegeben! Folgende Werte werden angenommen: n = 10, all = false")
if args.n:
    n = args.n
if args.all:
    if args.n:
        n = args.n
        printAll = True
    else:
        printAll = True

# Effizienter Algorithmus

def EfficientFibonacci(n,printAll):
    f1 = 1
    f2 = 1
    result = [1,1]

    for i in range(2, n):
        fn = f1 + f2
        f1 = f2
        f2 = fn
        result.append(fn)
    if printAll is True:
        return result[:]
    else:
        return result[-1]

# Laufzeitmessung

def FibonacciSpeed(n,  fibonacci):
    global total_time
    total_time = datetime.now() - datetime.now() # Erstellen eines Datetime Objekts mit Zeit = 0

    start = datetime.now()
    num = fibonacci(n,printAll=False)
    end = datetime.now()
    speed = end - start
    total_time += speed

    return[n,num,speed]

if printAll:
    speed_data = open("speed_data_efficient.csv", "w")
    print("n  Fibonacci number     t Efficient [h:m:s]")

    for i in range(1, n + 1):
        speed_output = FibonacciSpeed(i, EfficientFibonacci)

        # Output
        print("{0[0]}\t{0[1]}\t\t{0[2]}".format(speed_output))

        # Schreiben der Daten
        secs = speed_output[2].total_seconds()
        speed_data.write("{0[0]},{1:.6f}\n".format(speed_output, secs))

    print("Total time:     \t{}".format(total_time))
    print("\nAs a list: ")
    print(EfficientFibonacci(n,printAll=True))
    speed_data.close()
else:
    print(EfficientFibonacci(n,printAll=False))
