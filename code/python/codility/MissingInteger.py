# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
def solution(A):
	if len(A) == 1:
		if A[0] > 1:
			return 1
		return A[0] + 1 if A[0] == 1 else 1
		
	A = sorted(A)
	if A[0] > 1:
		return 1
		
	for i in range(len(A) - 1):
		if A[i] >= 0:
			if A[i+1] - A[i] < 2:
				continue
			else:
				return A[i] + 1
		else:
			if A[i+1] <= 1:
				continue
			else:
				return 1
	return 1 if A[-1] <= 0 else A[-1]+1

