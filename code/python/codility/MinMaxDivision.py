# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def validBlock(K, A, target):
	block_sum = 0
	block_cnt = 0
	for ai in A:
		if block_sum + ai > target:
			block_sum = ai
			block_cnt += 1
		else:
			block_sum += ai
			
		if block_cnt >= K:
			return False
	return True
	
	
def solution(K, M, A):
	del M
	lowest = max(A)
	highest = sum(A)
	while lowest <= highest:
		mid = (lowest + highest) // 2
		if validBlock(K, A, mid):
			highest = mid - 1
		else:
			lowest = mid + 1
	return lowest

