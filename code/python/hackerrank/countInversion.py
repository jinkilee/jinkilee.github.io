import math
import os
import random
import re
import sys

def count_subinv(a, b):
	res = 0
	for i in range(len(a)):
		if a[i] <= b[i]:
			continue
		for j in range(i+1, len(b)):
			if a[i] > b[j]:
			


# Complete the countInversions function below.
def countInversions(arr):
	res = 0
	return res
	
if __name__ == '__main__':
	arr = [1,2,3,4,5,6]
	result = countInversions(arr)

	s1 = [1,2,4,6]
	s2 = [2,3,4,5,6]
	count_subinv(s1, s2)
