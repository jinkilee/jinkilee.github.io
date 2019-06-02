def is_palindrome(s):
	if len(s) == 1:
		return True

	tgt = s[0]
	for i in range(len(s)//2):
		if s[i] != tgt or s[len(s)-i-1] != tgt:
			return False
	return True

def substrCount(n, s):
	res = 0
	clist = []
	samechar = 0
	idx = 0
	for i in range(len(s)):
		if i == 0:
			samechar += 1
			old = s[i]
			clist.append([idx, samechar, s[i]])
			continue
		if old == s[i]:
			clist[idx][1] += 1
			continue

		idx += 1
		old = s[i]
		try:
			clist[idx][1] += 1
		except:
			clist.append([idx, samechar, s[i]])
	

	for (c0, c1, c2) in clist:
		res += (int(c1*(c1+1)/2))

	for i in range(1, len(clist)-1):
		if clist[i][1] == 1 and \
				clist[i-1][2] == clist[i+1][2]:
				#clist[i-1][1] <= clist[i+1][1]:
			print(clist[i-1], clist[i], clist[i+1])
			res += min(clist[i-1][1], clist[i+1][1])
		
	return res


s = 'abcbaba'	# 10
s = 'asasd'		# 7
s = 'aaaa'	# 10
s = 'mnonopoo'	# 12
with open('input.txt', 'r') as f:
	f.readline()
	s = f.readline().rstrip()
res = substrCount(len(s), s)
print(s)
print('----')
print(res)
