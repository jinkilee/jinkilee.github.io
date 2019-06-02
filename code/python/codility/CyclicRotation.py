# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
def solution(A, K):
	if len(A) == 0:
		return A
	# write your code in Python 3.6
	k = K % len(A)
	
	right = A[:len(A)-k]
	left = A[len(A)-k:]
	rotated = left + right
	return rotated
	
