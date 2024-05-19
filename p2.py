import numpy
from functools import reduce
from operator import mul
import copy
import math

# description: computes the hook lengths for each cell in Young diagram
# input: int_part (int[]) - integer partition in standard form (decreasing)
# output: 2d list of hook lengths of the integer partition
def hook_lengths(int_part):

   hook_lengths = []

   # length of the partition
   part_length = len(int_part)

   # maximum element of the partition
   max_part = int_part[0]

   # track # cells above a given column to compute hook lengths
   cells_above = [0] * max_part

   # iterate in reverse order (increasing) through the partition
   for i in range(part_length - 1, -1, -1):
      cur_row_len = int_part[i]
      cur_row_hooks = []
      
      # compute hook length at each cell by adding # of cells above + to the 
      #   right (including current cell)
      for j in range(cur_row_len):
         cur_row_hooks.append(cells_above[j] + cur_row_len - j)

      # add the current row of hook lengths to the result
      hook_lengths.append(cur_row_hooks)

      # increment the counter of cells above to keep track for the next row
      for i in range(cur_row_len):
         cells_above[i] = cells_above[i] + 1

   return(hook_lengths)


# description: computes the prime factorization of a given number
# input: n (int) - the given number
# output: a list containing each prime factor (with corresponding multiplicity)
def prime_fact(n):

   i = 2 # potential prime divisor
   factors = []

   # stop iterating when i * i > n since if this is the case there are no more 
   #   divisors of n - if there were, one divisor would be less than i and one 
   #   would be greater than i, but we've already checked all #s less than i
   while i * i <= n:
      # if leftover num is not div by i, increment i and continue
      if n % i:
         i += 1

      # if leftover num is div by i, divide n by this factor and add to factors
      else:
         n //= i
         # i must be prime since composite nums have primes as factors which are
         #   smaller integers, so those are reached first (i increases)
         factors.append(i)

   # if a nontrivial factor of n is left, it must be prime (no divisors)
   if n > 1:
      factors.append(n)

   return factors


# description: helper function to compute the nested product of 2d list
# input: nested_list (int[][]) - given list
# output: the product of all numbers in the nested list
def nested_product(nested_list):

   prod = 1

   # multiply together all #s in the list
   for l in nested_list:
      for num in l:
         prod *= num

   return prod


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


# description: test our hypothesis that all self-conjugate partitions of size 
#                n >= 2 have corresponding degree divisible by 2
# input: max_n (int) - the maximum integer partition size to test to
# output: none (the function will print "FAIL" if any test cases fail)
def test_hypothesis(max_n):
   for n in range(2, max_n):
      self_conjs = self_conjugates(n)

      if len(self_conjs) == 0:
         continue

      n_fact_primes = prime_fact(math.factorial(n))
      twos_in_n_fact = sum(p == 2 for p in n_fact_primes)
      
      for int_part in self_conjs:
         hook_lens = hook_lengths(int_part)
         hook_prod_primes = prime_fact(nested_product(hook_lens))
         twos_in_hook_prod = sum(p == 2 for p in hook_prod_primes)

         # print("the int part is " + str(int_part))
         # print("n = " + str(n) + ", # twos in n! = " + str(twos_in_n_fact) + \
         #       ", # twos in hook prod = " + str(twos_in_hook_prod))
         # print("Pass!") if twos_in_n_fact > twos_in_hook_prod \ 
         #                else print("FAIL")
         if twos_in_n_fact <= twos_in_hook_prod:
            print("FAIL")

test_hypothesis(100)
