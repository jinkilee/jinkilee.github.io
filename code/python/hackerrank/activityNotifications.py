#!/bin/python3

import math
import os
import random
import re
import sys
import time
import numpy as np

MAXEXP = 201
def median(exp, d):
	iseven = True if not d%2 else False
	idx = 0

	counter = 0
	for i in range(MAXEXP):
		counter += exp[i]
		if counter >= d//2+1:
			break

	if iseven:
		for j in range(i,-1,-1):
			counter -= exp[j]
			if counter < d//2:
				return (i+j)/2
	else:
		return i

# Complete the activityNotifications function below.
def activityNotifications(expenditure, d):
	notice = 0
	exparr = [0] * MAXEXP

	for e in expenditure[:d]:
		exparr[e] += 1
	med = median(exparr, d)

	for i in range(d, len(expenditure)):
		#print(expenditure[i], 2*med)
		if expenditure[i] >= 2*med:
			notice += 1

		newidx = expenditure[i]
		oldidx = expenditure[i-d]
		exparr[newidx] += 1
		exparr[oldidx] -= 1
		med = median(exparr, d)

	return notice


if __name__ == '__main__':
	n = 9
	d = 5
	expenditure = [2,3,4,2,3,6,8,4,5]
	result = activityNotifications(expenditure, d)
	print(result)
	print('--------------')

	n = 5
	d = 3
	expenditure = [10,20,30,40,50]
	result = activityNotifications(expenditure, d)
	print(result)
	print('--------------')
	n = 5
	d = 4
	expenditure = [1,2,3,4,4]
	result = activityNotifications(expenditure, d)
	print(result)

	with open('input.txt', 'r') as f:
		f.readline()
		n = 200000
		d = 10000
		expenditure = list(map(int, f.readline().rstrip().split()))
	print(expenditure[:10])
	result = activityNotifications(expenditure, d)
	print(result)
