#!/bin/python3

import math
import os
import random
import re
import sys
from bisect import bisect_left

def getNumberOperations(packageSequence):
    """
    The most optimal solution using Longest Increasing Subsequence (LIS).
    
    Key insight: The minimum number of operations needed is n - LIS_length.
    This is because the packages that are already in the correct relative order
    (forming the LIS) don't need to be moved, while all others need operations.
    
    Time Complexity: O(n log n) using binary search
    Space Complexity: O(n)
    """
    if not packageSequence:
        return 0
    
    n = len(packageSequence)
    
    # dp[i] will store the smallest ending element of all increasing subsequences of length i+1
    dp = []
    
    for num in packageSequence:
        # Find the position where num should be inserted to maintain sorted order
        pos = bisect_left(dp, num)
        
        if pos == len(dp):
            # num is larger than all elements in dp, extend the sequence
            dp.append(num)
        else:
            # Replace dp[pos] with num to maintain the smallest possible ending element
            dp[pos] = num
    
    # Length of LIS
    lis_length = len(dp)
    
    # Minimum operations = total packages - packages already in correct order
    return n - lis_length

#
# Complete the 'getNumberOperations' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY packageSequence as parameter.
#

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    packageSequence_count = int(input().strip())

    packageSequence = []

    for _ in range(packageSequence_count):
        packageSequence_item = int(input().strip())
        packageSequence.append(packageSequence_item)

    result = getNumberOperations(packageSequence)

    fptr.write(str(result) + '\n')

    fptr.close()