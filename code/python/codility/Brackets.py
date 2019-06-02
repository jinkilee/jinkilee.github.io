
# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
def solution(S):
	if S == '':
		return 1
	if S[0] == ']' or S[0] == '}' or S[0] == ')':
		return 0
		
	#brackets = [S[0]]
	brackets = []
	for i in range(len(S)):
		si = S[i]
		if si == '[' or si == '{' or si == '(':
			brackets.append(si)
		else:
			if len(brackets) == 0:
				return 0
				
			top = brackets.pop()
			if (si == ']' and top != '['):
				return 0
			if (si == '}' and top != '{'):
				return 0
			if (si == ')' and top != '('):
				return 0
				
	if len(brackets) == 0:
		return 1
	else:
		return 0


