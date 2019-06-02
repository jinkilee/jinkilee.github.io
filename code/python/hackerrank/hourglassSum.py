#!/bin/python3
import math
import os
import random
import re
import sys
import itertools

def hourglassSum(arr):
	obj = [[1,1,1],[0,1,0],[1,1,1]]
	obj = list(itertools.chain(*obj))

	# iterate matrix
	res = []
	for i in range(4):
		for j in range(4):
			mat = [arr[ii][j:j+3] for ii in range(i, i+3)]
			mat = list(itertools.chain(*mat))
			matsum = sum(list(map(lambda x: x[0]*x[1], zip(obj, mat))))
			res.append(sum(list(
				map(lambda x: x[0]*x[1], 
				zip(obj, mat)))))
	return max(res)
	
if __name__ == '__main__':
	#fptr = open(os.environ['OUTPUT_PATH'], 'w')

	arr = []
	arr = [
		[1,1,1,0,0,0],
		[0,1,0,0,0,0],
		[1,1,1,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0]]

	#arr = 
	res = hourglassSum(arr)
	print(res)

	#fptr.write(str(result) + '\n')

	#fptr.close()

