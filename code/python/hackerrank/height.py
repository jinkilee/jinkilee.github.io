class Node:
	def __init__(self, info): 
		self.info = info  
		self.left = None  
		self.right = None 
		self.level = None 

	def __str__(self):
		return str(self.info) 

class BinarySearchTree:
	def __init__(self): 
		self.root = None

	def create(self, val):  
		if self.root == None:
			self.root = Node(val)
		else:
			current = self.root
		 
			while True:
				if val < current.info:
					if current.left:
						current = current.left
					else:
						current.left = Node(val)
						break
				elif val > current.info:
					if current.right:
						current = current.right
					else:
						current.right = Node(val)
						break
				else:
					break

def is_end(node, l):
	if not node:
		return l
	if node.left == None and node.right == None:
		return l
	else:
		left_l = l
		right_l = l
		if node.left:
			left_l = is_end(node.left, l+1)
		if node.right:
			right_l = is_end(node.right, l+1)
		return max(left_l, right_l)

# Enter your code here. Read input from STDIN. Print output to STDOUT
def height(root):
	level = 0
	level = is_end(root, level)
	return level

tree = BinarySearchTree()
t = 7
arr = [1,2,3,4,5,6,7]
for i in range(t):
	tree.create(arr[i])

h = height(tree.root)
print(h)

