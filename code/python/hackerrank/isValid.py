#!/bin/python3

import math
import os
import random
import re
import sys
from collections import Counter

# Complete the isValid function below.
def isValid(s):
	cnt = Counter(s)
	uniqchar = len(cnt)

	cnt_dict = {}
	for k, v in cnt.items():
		try:
			cnt_dict[v].append(k)
		except KeyError:
			cnt_dict[v] = [k]
	keys = list(cnt_dict.keys())
	# every characyer has same number of frequency
	if len(keys) > 2:
		return 'NO'
	elif len(keys) == 1:
		return 'YES'
	else:
		k0, k1 = keys
		if abs(k0-k1) == 1:
			minkey = min(k0, k1)
			if len(cnt_dict[minkey]) == 1 or \
				len(cnt_dict[minkey]) == uniqchar-1:
				return 'YES'
			return 'NO'
		else:
			minkey = min(k0, k1)
			if minkey == 1 and len(cnt_dict[minkey]) == 1:
				return 'YES'
			return 'NO'
if __name__ == '__main__':
	s = 'aabbc'	# yes
	s = 'aabbcd'	# no
	s = 'xxxaabbccrry'	# no
	s = 'abbccddeefghi'	# no
	s = 'abcdefghhgfedecba'	# yes
	s = 'aaaabbcc'	# NO
	s = 'abcdefghhgfedecba'	# yes
	result = isValid(s)
	print('----------')
	print(result)

