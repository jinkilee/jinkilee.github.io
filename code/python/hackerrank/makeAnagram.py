#!/bin/python3

import math
import os
import random
import re
import sys

def remove_char(word, char):
	i = word.index(char)
	return word[:i]+word[i+1:]

# Complete the makeAnagram function below.
def makeAnagram(a, b):
	res = 0
	for ai in a:
		if ai in b:
			b = remove_char(b, ai)
			continue
		res += 1

	res += len(b)
	return res
	
if __name__ == '__main__':
	a = 'cde'
	b = 'abc'
	res = makeAnagram(a, b)
	print('-------')
	print(res)

