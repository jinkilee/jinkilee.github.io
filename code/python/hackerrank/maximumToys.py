#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the maximumToys function below.
def maximumToys(prices, k):
	prices = sorted(prices)
	ntoys = 0
	total_price = 0
	for p in prices:
		total_price += p
		if total_price <= k:
			ntoys += 1
	return ntoys

if __name__ == '__main__':
	n = 7
	k = 50
	prices = [1, 12, 5 ,111, 200, 1000, 10]
	result = maximumToys(prices, k)
	print(result)

