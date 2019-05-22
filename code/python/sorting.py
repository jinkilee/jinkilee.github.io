# assuming we have k sorted list to merge(),
# and parameter of merge has two lists with length of n
# this sort function give us O(nklog(k)) complexity

import numpy as np
import time

def merge(a, b):
	result = []
	i = 0
	j = 0
	while True:
		if (i == len(a)) or (j == len(b)):
			break
		if a[i] < b[j]:
			result.append(a[i])
			i += 1
			continue
		else:
			result.append(b[j])
			j += 1
			continue

	if i < j:
		result += a[i:]
	else:
		result += b[j:]
	return result

def sort(numlist):
	if len(numlist) == 1:
		return numlist

	mid = int(len(numlist)/2)
	a = numlist[:mid]
	b = numlist[mid:]

	a = sort(a)
	b = sort(b)
	return merge(a, b)

c = np.random.randint(0, 50000, (9999999)).tolist()

start = time.time()
sort_c = sort(c)
end = time.time()
print('sort(): %.2f' % (end  - start))

start = time.time()
sorted_c = sorted(c)
end = time.time()
print('built-in sorted(): %.2f' % (end  - start))

print(sort_c == sorted_c)
