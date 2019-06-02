from collections import Counter
def solution(A):
	cnt = Counter(A)
	for k, v in cnt.items():
		if v%2 == 1:
			return k

