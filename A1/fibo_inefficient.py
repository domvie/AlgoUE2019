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

# Rekursiver Algorithmus

def RecursiveFibonacci(n):

    if n == 1 or n == 2:
        return 1
    else:
        a = RecursiveFibonacci(n - 1)
        b = RecursiveFibonacci(n - 2)
        return a + b

# Laufzeitmessung

def FibonacciSpeed(n,  fibonacci):
    global total_time

    total_time = datetime.now() - datetime.now() # Erstellen eines Datetime Objekts mit Zeit = 0
    start = datetime.now()
    num = fibonacci(n)
    end = datetime.now()
    speed = end - start
    total_time += speed

    return[n,num,speed]

if printAll:
    speed_data = open("speed_data_recursive.csv", "w")
    print("n  Fibonacci number     t Recursive [h:m:s]")
    result = [1, 1]
    for i in range(1, n + 1):
        speed_output = FibonacciSpeed(i, RecursiveFibonacci)

        # Output
        print("{0[0]}\t{0[1]}\t\t{0[2]}".format(speed_output))
        result.append(speed_output[1])

        # Schreiben der Daten
        secs = speed_output[2].total_seconds()
        speed_data.write("{0[0]},{1:.6f}\n".format(speed_output, secs))

    print("Total time:     \t{}".format(total_time))
    print("\nAs a list: ")
    print(result)
    speed_data.close()
else:
    print(RecursiveFibonacci(n))



