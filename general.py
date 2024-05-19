import copy

def integer_partitions(n):
    int_partitions = []
    int_partitions_helper([0] * n, 0, n, n, int_partitions)
    return int_partitions

def int_partitions_helper(cur_part, idx, n, red_n, partitions):

    # if the reduced # is negative, this partition doesn't work (sum too large)
    if red_n < 0:
        return

    # if the reduced # is 0, the sum is n, ie. valid partition
    if red_n == 0:

        # deep copy since otherwise cur_part gets overwritten by later calls
        partitions.append(copy.deepcopy(cur_part[:idx]))
        return

    # start at n if the current partition is empty or the prev # otherwise
    start = n if (idx == 0) else cur_part[idx - 1]

    # recursively try all combinations to see which yield valid partitions
    for k in range(start, 0, -1):
        cur_part[idx] = k
        int_partitions_helper(cur_part, idx + 1, n, red_n - k, partitions)


print(integer_partitions(60))
