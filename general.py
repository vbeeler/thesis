import sys
from copy import deepcopy
from sympy import primerange
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

# description: computes the degree of the irreducible representation of Sn 
#                corresponding to the given integer partition using the hook
#                length formula
# input: int_part (int[]) the integer partition
# output: the degree of the representation
def deg_of_irr_rep(int_part):
    n = sum(int_part)
    hook_lens = hook_lengths(int_part)
    hook_prod = nested_product(hook_lens)
    return math.factorial(n) / hook_prod


# description: finds all integer partitions of size n
# input: n (int) - given size of integer partitions
# output: the list of integer partitions
def integer_partitions(n):
    int_partitions = []
    int_partitions_helper([0] * n, 0, n, n, int_partitions)
    return int_partitions


# description: recursive helper function to find all integer partitions of n
# input: cur_part (int[]) - stores the current partition
#        idx (int) - next unused location in the current partition
#        n (int) - given size of integer partition
#        n_left (int) - partial sum left for the current partition
#        partitions (int[][]) - all found integer partitions
# output: None - partitions variable contains the desired output
def int_partitions_helper(cur_part, idx, n, n_left, partitions):

    # if the reduced # is negative, this partition doesn't work (sum too large)
    if n_left < 0:
        return

    # if the reduced # is 0, the sum is n, ie. valid partition
    if n_left == 0:

        # deep copy since otherwise cur_part gets overwritten by later calls
        partitions.append(deepcopy(cur_part[:idx]))
        return

    # start at n if the current partition is empty or the prev # otherwise
    start = n if (idx == 0) else cur_part[idx - 1]

    # recursively try all combinations to see which yield valid partitions
    for k in range(start, 0, -1):
        cur_part[idx] = k
        int_partitions_helper(cur_part, idx + 1, n, n_left - k, partitions)

# description: finds the number of integer partitions of size n whose degree 
#                is not divisible by p
# input: n (int) - the size of the integer partitions
# output: p (int) - the prime
def num_not_div_by_p(n, p):

    count = 0
    int_parts = integer_partitions(n)

    # for each integer partition of size n, compute the degree and increment 
    #   the count by 1 if not divisible by p
    for part in int_parts:
        degree = deg_of_irr_rep(part)

        if degree % p != 0:
            count += 1

    return count

# description: print the integer partitions of size given as command line arg
# input: none
# output: none
def print_int_partitions():
    
    # get the command line argument for partition size n, if provided
    if len(sys.argv) != 1:
        n = int(sys.argv[1])
        print(integer_partitions(n))

# description: tests the general hypothesis we are aiming to prove by iterating
#                over every combination of n and p, up to the max n given
# input: max_n (int) - the maximum integer partition size to test
# output: none 
def test_general_hypothesis(max_n):

    # iterate through all possible partition sizes up to the max
    for n in range(max_n):

        # the prime p must be between 0 and n since the size of an irr rep of Sn
        #   is capped by n
        for p in primerange(0, n + 1):

            # the total number of integer partitions whose corresponding irr 
            #   rep for Sn has degree not divisible by p should itself by 
            #   divisible by p
            if num_not_div_by_p(n, p) % p == 0:
                print("success with n = " + str(n) + " and p = " + str(p) + ".")

            else:
                print("FAILED with n = " + str(n) + " and p = " + str(p) + ".")


print_int_partitions()
test_general_hypothesis(10)
