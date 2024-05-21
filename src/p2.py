import numpy
from functools import reduce
from operator import mul
import copy
import math
from general import prime_fact, hook_lengths, deg_of_irr_rep


# description: helper function to better visualize a prime factorization
#              groups together primes into powers
# input: prime_f (int[]) - increasing prime factors w/ multiplicities
# output: a dictionary mapping each prime to its power in the factorization
def format_prime(prime_f):

   # no primes in factorization
   if prime_f == []:
      return {}

   prime_powers = {}

   for prime in prime_f:

      # if prime already in dictionary, increment the count
      if prime in prime_powers:
         prime_powers[prime] += 1

      # if prime not yet in dictionary, initialize count to 1
      else:
         prime_powers[prime] = 1

   return prime_powers


# description: finds all self conjugate integer partitions of size n
# input: n (int) - the size of the integer partitions
# output: a list of all self conjugate partitions, each represented as a list 
#           of decreasing integers
def self_conjugates(n):
   
   # utilize the correspondence between distinct odd integer partitions and 
   #   self-conjugate integer partitions
   distinct_odds = []
   find_distinct_odds([0] * n, 0, n, n, distinct_odds)
   
   # compute the corresponding self conjugate integer partition for each list 
   #   of distinct odds 
   self_conjs = []
   for dist_odd in distinct_odds:
      self_conjs.append(dist_odd_to_self_conj(dist_odd))
   return self_conjs

   
# description: recursive helper function to find all partitions of distinct
#                odds of a certain size
# input: cur_part (int[]) - stores the current partition of distinct odds
#        idx (int) - next unused location in the current partition
#        n (int) - given size of integer partition
#        red_n (int) - reduced size left for the current partition
#        results (int[][]) - all found distinct odd partitions
# output: None - results variable contains the desired output
def find_distinct_odds(cur_part, idx, n, red_n, results):

   # if the reduced # is negative, this partition doesn't work (sum too large)
   if red_n < 0:
      return
   
   # if the reduced # is 0, the sum of distinct odds is n, ie. valid partition
   if red_n == 0:

      # deep copy since otherwise cur_part gets overwritten by later calls
      results.append(copy.deepcopy(cur_part[:idx]))

   # start at 1 if the current partition is empty or the next odd otherwise
   start = 1 if (idx == 0) else cur_part[idx - 1] + 2

   # recursively try all odd numbers left to see which yield valid partitions
   for k in range(start, n + 1, 2):
      cur_part[idx] = k
      find_distinct_odds(cur_part, idx + 1, n, red_n - k, results)


# description: convert a distinct odd integer partition to the corresponding 
#                self-conjugate partition (we know there is a bijection)
# input: dist_odd_part (int[]) - distinct odd partition (increasing)
# output: the corresponding self-conjugate partition (decreasing) 
def dist_odd_to_self_conj(dist_odd_part):

   # reverse the order to make it standard (decreasing)
   dist_odd_part.reverse()

   # the largest odd determines the dimension of the self conjugate partition
   #   since we perform the bijection by viewing each distinct odd integer as
   #   a symmetric L shape in the self-conjugate partition
   largest_odd = dist_odd_part[0]
   dim = largest_odd // 2 + 1
   
   # initialize a 2d list of large enough dimension with zeros - a 1 will 
   #   correspond to filling in a square of the Young diagram
   young_diagram = [[0 for col in range(dim)] for row in range(dim)]

   # fill in the Young diagram of the self conjugate partition by mapping each
   #   distinct odd to its L shape
   for idx in range(len(dist_odd_part)):

      # corner of the L
      young_diagram[idx][idx] = 1
      
      # length of the L up and to the right of the corner      
      traverse_num = dist_odd_part[idx] // 2

      # fill in diagram up from corner
      for j in range(1, traverse_num + 1):
         young_diagram[idx][idx + j] = 1

      # fill in diagram to right of corner
      for i in range(1, traverse_num + 1):
         young_diagram[idx + i][idx] = 1

   self_conj = []

   # create the self conjugate integer partition by summing up the boxes in 
   #   each row of the Young diagram
   for row in young_diagram:
      self_conj.append(sum(row))

   return self_conj

         
# description: experiment with all the functions above to make sure they work 
#                as expected
# input: none
# output: none
def experiment():

   for n in range(1, 20):

      self_conjs = self_conjugates(n)

      if len(self_conjs) == 0:
         continue

      print("The self conjugate integer partitions of size " + str(n) + \
            " are " + str(self_conjs) + ".")
      print()

      for int_part in self_conjs:

         print("Our self conjugate integer partition is " + str(int_part) + ".")
         
         hook_lens = hook_lengths(int_part)
         print("The hook lengths are " + str(hook_lens) + ".")

         prime_f = prime_fact(nested_product(hook_lens))
         print("The prime factorization is " + str(prime_f) + ",")

         formatted = format_prime(prime_f)
         print("  which can also be written " + str(formatted) + ".")
         
         print()
  
      print()
      print()


# description: test our hypothesis that the irreducible representations
#                corresponding to self-conjugate partitions of size 
#                n >= 2 have degree divisible by 2
# input: max_n (int) - the maximum integer partition size to test to
# output: none (the function will print "FAIL" if any test cases fail)
def test_hypothesis(max_n):

    # test integer partitions of all sizes from 2 to n
    for n in range(2, max_n):

        self_conjs = self_conjugates(n)

        # if there are no self-conjugate partitions of this size, skip to next
        if len(self_conjs) == 0:
            continue

        # test that 
        for self_conj in self_conjs:
            
            deg = deg_of_irr_rep(self_conj)

            if deg % 2 != 0:
                print("FAILED with self-conjugate partition" + str(self_conj))

test_hypothesis(100)
