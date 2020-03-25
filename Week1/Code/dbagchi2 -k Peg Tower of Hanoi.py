#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
import math
from collections import deque

parser = argparse.ArgumentParser(description='Process K-Peg tower of hanoi (No of disks, No. of pegs.')
parser.add_argument('nod', type=str)
parser.add_argument('pegs', type=str)
args = parser.parse_args()
# l1_list = args.l1.split(',') # ['1','2','3','4']

print(args.nod)
print(type(args.nod))
print(args.pegs)
print(type(args.pegs))

# See https://www.geeksforgeeks.org/deque-in-python/ for details on Deques
Towers = deque()

# Global variable that keeps track of the number of steps in our solution
number_of_steps = 0

k = int(args.pegs)
n = int(args.nod)

print(type(k))

# It is always a good idea to set a limit on the depth-of-the-recursion-tree in Python
sys.setrecursionlimit(30000)


# The function ${\sf initialize(n)}$ first inserts the numbers $(1, 2, \cdots, n)$ in deque \#0 of ${\sf Towers}$; and puts an empty-deque for deque \#1, deque \#2 and deque \#3

def initialize(n):
    global k
    for i in range(k):
        X = deque()
        if (i == 0):
            for j in range(n):
                X.append(j + 1)
        Towers.append(X)


# Function ${\sf is\_everything\_legal()}$ checks if a larger number (i.e. a larger diameter disk) is placed on top of a smaller number (i.e. a smaller diameter disk) in any of the 4 Deques of ${\sf Towers}$.  I am not suggesting that this check is efficient -- it just does the job (and can be improved, if necessary)!

def is_everything_legal():
    global k
    result = True
    for i in range(k):
        for j in range(len(Towers[i])):
            for k in range(j, len(Towers[i])):
                if (Towers[i][k] < Towers[i][j]):
                    result = False
    return (result)


# Function ${\sf move\_top\_disk (source, dest)}$ moves the top-disk from ${\sf source}$ and places it on ${\sf dest}$.  Following this, it checks if any larger-diameter disk has been placed on a smaller diameter disk in any of the 4 Pegs.

def move_top_disk(source, dest):
    global number_of_steps
    number_of_steps = number_of_steps + 1
    x = Towers[source].popleft()
    Towers[dest].appendleft(x)
    if (True == is_everything_legal()):
        y = " (Legal)"
    else:
        y = " (Illegal)"

    print ("Move disk " + str(x) + " from Peg " + str(source + 1) + " to Peg " + str(dest + 1) + y)


# This is the (familiar) recursive solution to the 3-Peg Tower of Hanoi Problem.

def move_using_three_pegs(number_of_disks, source, dest, intermediate):
    # print(intermediate)
    # print(type(intermediate))
    if (1 == number_of_disks):
        move_top_disk(source, dest)
    else:
        move_using_three_pegs(number_of_disks - 1, source, intermediate, dest);
        move_top_disk(source, dest)
        move_using_three_pegs(number_of_disks - 1, intermediate, dest, source)


# This is the recursive solution to the 4-Peg Tower of Hanoi Problem -- where we move $(\lfloor \frac{\mbox{no of disks}}{2} \rfloor)$-many disks from the source-peg to the first-intermediate peg, and we let it sit there till the remaining disks are moved from the source-peg to the destination-peg using the second-intermediate peg (via the 3-Peg solution).  Following this, we move the $(\lfloor \frac{\mbox{no of disks}}{2} \rfloor)$-many disks from the first-intermediate peg to the detination peg.

def move_using_four_pegs(number_of_disks, source, dest, intermediate1):
    if (number_of_disks > 0):
        p = math.floor(number_of_disks / 2)
        move_using_four_pegs(p, source, intermediate1[0], [intermediate1[1], dest])
        move_using_three_pegs(number_of_disks - p, source, dest, intermediate1[1])
        move_using_four_pegs(p, intermediate1[0], dest, [intermediate1[1], source])


def print_peg_state(m):
    global number_of_steps
    print ("-----------------------------")
    print ("State of Peg " + str(m + 1) + " (Top to Bottom): " + str(Towers[m]))
    print ("Number of Steps = " + str(number_of_steps))
    print ("-----------------------------")


initialize(n)
print_peg_state(0)
pegs = k
a = [i for i in range(k - 1) if i != 0]
move_using_four_pegs(n, 0, k - 1, [i for i in range(k - 1) if i != 0])
print_peg_state(pegs - 1)
