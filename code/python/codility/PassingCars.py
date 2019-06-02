
# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
def bsearch(west, target):
	start = 0
	end = len(west) - 1
	while start <= end:
		mid = (start + end) // 2
		if west[mid] < target:
			start = mid + 1
		elif west[mid] > target:
			end = mid - 1
		else:
			return mid
	return start
	
	
def solution(A):
	# write your code in Python 3.6
	east = [i for i, ai in enumerate(A) if ai == 0]
	west = [i for i, ai in enumerate(A) if ai == 1]
	
	pair = 0
	for ei in east:
		idx = bsearch(west, ei)
		pair += (len(west)-idx)
		#print(ei, west, len(west)-idx)
	
	if pair > 1000000000:
		return -1
	return pair


