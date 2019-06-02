
#!/bin/python3

import math
import os
import random
import re
import sys

def remove_lt_bi(arr, bi, idx):
	while arr[idx] > bi:
		if idx == -1:
			break
		idx -= 1
	return idx

def triplets(a, b, c):
	a = sorted(set(a))
	b = sorted(set(b))
	c = sorted(set(c))

	ai = 0
	bi = 0
	ci = 0
	res = 0
	while bi < len(b):
		while ai < len(a) and a[ai] <= b[bi]:
			ai += 1
		while ci < len(c) and c[ci] <= b[bi]:
			ci += 1

		res += (ai*ci)
		bi += 1

	return res

if __name__ == '__main__':

	arra = '41705157 97849134 45597343 16768845 22004255 8599189 2105694 89992290 67225143 89110311'.split()
	arrb = '13272876 84702911 8455586 8597056 131603 80740505 44236720 92144494 57795598'.split()
	arrc = '82044489 35357393 83576278 87430244 76673809 10617871 83652958 2163170'.split()
	arra = list(map(int, arra))
	arrb = list(map(int, arrb))
	arrc = list(map(int, arrc))

	#arra = [1,3,7,7,10]
	#arrb = [5,9,9]
	#arrc = [7,7,8,13]

	# 12
	arra = [1,3,5]
	arrb = [2,3]
	arrc = [1,2,3]
	ans = triplets(arra, arrb, arrc)
	print(ans)


