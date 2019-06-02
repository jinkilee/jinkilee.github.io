#!/bin/python3
import time
import math
import os
import random
import re
import sys
import itertools
from collections import Counter

def checkAnagrams(a, b):
	if sorted(a) == sorted(b):
		return True
	else:
		return False

# Complete the sherlockAndAnagrams function below.
def sherlockAndAnagrams(s):
	substring_dict = {}
	for sublen in range(1, len(s)):
		substrings = ([s[j:j+sublen] for j in range(len(s)-sublen+1)])
		substring_dict[sublen] = substrings

	numAna = 0
	for k in substring_dict:
		pairs = list(itertools.combinations(substring_dict[k], 2))
		numAna += sum([checkAnagrams(*p) for p in pairs])
	return numAna

if __name__ == '__main__':
	s = 'ifailuhkqqhucpoltgtyovarjsnrbfpvmupwjjjfiwwhrlkpekxxnebfrwibylcvkfealgonjkzwlyfhhkefuvgndgdnbelgruel'

	start = time.time()
	result = sherlockAndAnagrams(s)
	end = time.time()
	print(result)
	print('elapsed: %.4f' % (end-start))
