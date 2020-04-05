#!/usr/bin/env python3
# coding: utf-8

# Gibbs-Sampling procedure to compute the Probability Matrix of a Discrete-Time Markov
# Chain whose states are the d-dimensional cartesian product of the form 
# {0,1,...n-1} x {0,1,...n-1} x ... X {0,1,...n-1} (i.e. d-many products)
# 
# The target stationary distribution is expressed over the n**d many states 
#
# Written by Prof. R.S. Sreenivas for
# IE531: Algorithms for Data Analytics
#

import sys
import argparse
import random
import numpy as np 
import time
import math
import matplotlib.pyplot as plt
import itertools as it

# need this to keep the matrix print statements to 4 decimal places
np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})

# This function computes a random n-dimensional probability vector (whose entries sum to 1)
def generate_a_random_probability_vector(n) :
    random_darts = np.random.uniform(0, 1, n-1)
    sort_random_darts = sorted(random_darts)
    y = [sort_random_darts[i] if i == 0 else (sort_random_darts[i] - sort_random_darts[i-1]) for i in range(0, n-1)]
    y.extend([1 - sort_random_darts[n-2]])
    return y

# Two d-tuples x and y are Gibbs-Neighbors if they are identical, or they differ in value at just
# one coordinate
def check_if_these_states_are_gibbs_neighbors(x, y) :
    # x and y are dim-tuples -- we will assume they are not equal
    # count the number of coordinates where they differ
    gibbs_neighbours_difference = [0 if a == b else 1 for a, b in zip(x, y)]
    if(sum(gibbs_neighbours_difference) == 1):
        gibbs_neighbours = True
    else:
        gibbs_neighbours = False
    
    return gibbs_neighbours


# Given two Gibbs-Neighbors -- that are not identical -- find the coordinate where they differ in value
# this is the "free-coordinate" for this pair
def free_coordinates_of_gibbs_neighbors(x, y) :
    # we assume x and y are gibbs neighbors, then the must agree on at least (dim-1)-many coordinates
    # or, they will disagree on just one of the (dim)-many coordinates... we have to figure out which 
    # coordinate/axes is free
    free_index = [i for i, (a, b) in enumerate(zip(x, y)) if a != b]
    return free_index[0]


# x in a dim-tuple (i.e. if dim = 2, it is a 2-tuple; if dim = 4, it is a 4-tuple) state of the Gibbs MC
# each of the dim-many variables in the dim-tuple take on values over range(n)... this function returns 
# the lexicographic_index (i.e. dictionary-index) of the state x
def get_lexicographic_index(x, n, dim) :
    all_possible_lexicographic_combo = list(it.product(range(n), repeat = dim))
    number = all_possible_lexicographic_combo.index(x)
    return number

# This is an implementaton of the Gibbs-Sampling procedure
# The MC has n**dim many states; the target stationary distribution is pi
# The third_variable_is when set to True, prints the various items involved in the procedure
# (not advisable to print for large MCs)
def create_gibbs_MC(n, dim, pi, do_want_to_print) :
    if (do_want_to_print) :
        print ("Generating the Probability Matrix using Gibbs-Sampling")
        print ("Target Stationary Distribution:")
        for x in it.product(range(n), repeat = dim) :
            number = get_lexicographic_index(x, n, dim)
            print ("\u03C0", x, " = \u03C0(", number , ") = ", pi[number])
    
    # the probability matrix will be (n**dim) x (n**dim) 
    probability_matrix = [[0 for x in range(n**dim)] for y in range(n**dim)]
    
    # the state of the MC is a dim-tuple (i.e. if dim = 2, it is a 2-tuple; if dim = 4, it is a 4-tuple)
    # got this from https://stackoverflow.com/questions/7186518/function-with-varying-number-of-for-loops-python
    for x in it.product(range(n), repeat = dim) :
        # x is a dim-tuple where each variable ranges over 0,1,...,n-1
        row_sum = 0
        for y in it.product(range(n), repeat = dim) :
            
            gibbs_neighbours = check_if_these_states_are_gibbs_neighbors(x, y)
            if gibbs_neighbours == True:
                denominator = 0
                free_coordinates_index = free_coordinates_of_gibbs_neighbors(x, y)
                for i in range(n):
                    convert_tuple_to_list = list(y)
                    convert_tuple_to_list[free_coordinates_index] = i
                    denominator += pi[get_lexicographic_index(tuple(convert_tuple_to_list), n, dim)]
                
                stochastic_value = (pi[get_lexicographic_index(y, n, dim)] / (denominator * dim))
                probability_matrix[get_lexicographic_index(x, n, dim)][get_lexicographic_index(y, n, dim)] = stochastic_value
                row_sum += stochastic_value 
        probability_matrix[get_lexicographic_index(x, n, dim)][get_lexicographic_index(x, n, dim)] = (1 - row_sum)
    return probability_matrix

# Trial 1... States: {(0,0), (0,1), (1,0), (1,1)} (i.e. 4 states)
n = 2
dim = 2
a = generate_a_random_probability_vector(n**dim)
print("(Random) Target Stationary Distribution\n", a)
p = create_gibbs_MC(n, dim, a, True) 
print ("Probability Matrix:")
print (np.matrix(p))
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 2... States{(0,0), (0,1),.. (0,9), (1,0), (1,1), ... (9.9)} (i.e. 100 states)
n = 10
dim = 2
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False) 
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 3... 1000 states 
n = 10
dim = 3
t1 = time.time()
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False) 
t2 = time.time()
hours, rem = divmod(t2-t1, 3600)
minutes, seconds = divmod(rem, 60)
print ("It took ", hours, "hours, ", minutes, "minutes, ", seconds, "seconds to finish this task")
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 4... 10000 states 
n = 10
dim = 4
t1 = time.time()
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False) 
t2 = time.time()
hours, rem = divmod(t2-t1, 3600)
minutes, seconds = divmod(rem, 60)
print ("It took ", hours, "hours, ", minutes, "minutes, ", seconds, "seconds to finish this task")
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

