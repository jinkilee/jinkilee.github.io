#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the arrayManipulation function below.
def arrayManipulation(n, queries):
	res = [0] * (n+1)
	for q in queries:
		si, ei, k = q
		res[si-1] += k
		if ei != len(res):
			res[ei] -= k

	maxval = -1
	summ = 0
	for i, r in enumerate(res):
		summ += r
		if summ > maxval:
			maxval = summ
	return maxval
		

if __name__ == '__main__':
	'''
	5 3
	1 2 100
	2 5 100
	3 4 100
	-> 200
	'''
	queries = []
	with open('input.txt', 'r') as f:
		n, m = list(map(int, f.readline().rstrip().split()))
		for oneline in f:
			a, b, k = list(map(int, oneline.rstrip().split()))
			queries.append([a, b, k])
	n = 4
	m = 3
	queries = [
		[2,3,603],
		[1,1,286],
		[4,4,882],
	]
	res = arrayManipulation(n, queries)
	print('-----')
	print(res)
