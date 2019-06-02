#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np

def minimumSwaps(arr):
	i, swap = -1, 0
	while i < len(arr) - 1:
		i += 1
		if arr[i] == i+1:
			continue
		j = arr[i] - 1
		arr[i], arr[j] = arr[j], arr[i]
		swap += 1
		i -= 1
	return swap

if __name__ == '__main__':
	arr = [4,3,1,2]
	arr = [1,5,3,4,2]
	arr = np.random.choice(10, (10), replace=False)
	arr += 1
	arr = arr.tolist()
	res = minimumSwaps(arr)
	print(res)
