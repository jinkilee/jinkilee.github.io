from functools import cmp_to_key

class Player:
	def __init__(self, name, score):
		self.name = name
		self.score = score

	def __repr__(self):
		return '{} {}'.format(self.name, self.score)
		
	def comparator(a, b):
		if a.score < b.score:
			return 1
		elif a.score > b.score:
			return -1
		else:
			if a.name < b.name:
				return -1
			elif a.name > b.name:
				return 1
			else:
				return 0

	
data = [
	Player('amy', 100),
	Player('david', 100),
	Player('heraldo', 50),
	Player('aakansha', 75),
	Player('aleksa', 150)]
data = sorted(data, key=cmp_to_key(Player.comparator))
for i in data:
	print(i.name, i.score)

