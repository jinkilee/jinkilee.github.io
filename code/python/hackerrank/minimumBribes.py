#!/bin/python3

import math
import os
import random
import re
import sys

MAXBRB = 2

# Complete the minimumBribes function below.
def minimumBribes(q):
	result = 0
	for i in range(len(q)-1, -1, -1):
		if q[i] - (i+1) > 2:
			print('Too chaotic')
			return
		for j in range(max(0, q[i]-2), i):
			if q[i] < q[j]:
				result += 1
	print(result)

if __name__ == '__main__':
	#q = [2,1,5,3,4]	# 3
	#q = [2,5,1,3,4]	# chaos
	#q = [1,2,5,3,4,7,8,6]	# 4
	#q = [5,1,2,3,7,8,6,4]	# Too chaotic
	q = [1,2,5,3,7,8,6,4]	# 7
	#i = [1,2,3,4,5,6,7,8]
	minimumBribes(q)

