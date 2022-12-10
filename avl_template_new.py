#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  




class AVLNode(object):
	""" AVL Node
		--------
		A class represnting a node in an AVL tree
		@inv: for each node, abs(left.height - right.height) <= 1   # AVL
		
		fields
		------
			value: data held in node @type: str
		
			pointers:
				left: left child of the node @type: AVLNode \n
				right: right child of the node @type: AVLNode \n
				parent: parent of the node @type:AVLNode \n
			
			helpers:
				height: length of the longest path from the node to a leaf @type: int \n
				size: the number of nodes in the subtree @type: int
		"""
	
	def __init__(self, value, left, right, height, size, 
				parent=None):
		"""Constructor, creates a real node.
		if left or right are None, inserts virtual nodes instead
		
		@type value: str or None
		@param value: data of your node
		@type left: AVLNode
		@param left: left child the node
		@type right: AVLNode
		@param right: right child of the node
		@type height: int
		@param height: length of the longest path to a leaf FIXME maybe update from children?
		@type size: int
		@param size: the number of nodes in the subtree FIXME maybe update from children?
		"""
		self.value = value
		
		# pointers
		self.left = left
		self.right = right
		self.parent = parent
		
		# help fields
		self.height = height
		self.size = size
		# # uncomment if move to calculation of help fields
		# self.updateHelpers()
		
		# padding with virtual nodes
		if (value != None):
			self.padWithVirtuals()
	

	@staticmethod
	def virtualNode(parent=None):
		"""creates a new virtual node assigned with given parent
		
		@type parent: AVLNode 
		@param parent: node to be the parent
		"""
		return AVLNode(	value=None,
						left=None,
						right=None,
						height=-1,
						size=0,
						parent=parent )


	def getLeft(self):
		"""returns the left child

		@rtype: AVLNode
		@returns: the left child of self, None if there is no left child
		"""
		return self.left
		

	def getRight(self):
		"""returns the right child

		@rtype: AVLNode
		@returns: the right child of self, None if there is no right child
		"""
		return self.right


	def hasLeft(self):
		"""checks if the left child is a real node

		@rtype: bool
		@return: left != None and left is a real node
		"""
		left = self.getLeft()
		return left != None and left.isRealNode()


	def hasRight(self):
		"""checks if the right child is a real node

		@rtype: bool
		@return: right != None and right is a real node
		"""
		right = self.getRight()
		return right != None and right.isRealNode()


	def getParent(self):
		"""returns the parent 

		@rtype: AVLNode
		@returns: the parent of self, None if there is no parent
		"""
		return self.parent


	def getValue(self):
		"""return the value

		@rtype: str
		@returns: the value of self, None if the node is virtual
		"""
		return self.value


	def getSize(self):
		"""returns the size field
		
		@rtype: int
		@returns: the number of nodes in the subtree below self (inclusive)
		Doesn't check for correctness
		"""
		return self.size
	

	def getHeight(self):
		"""returns the height field

		@pre: height is correct
		@rtype: int
		@returns: the height of self, -1 if the node is virtual.
		"""
		return self.height


	def getBalanceFactor(self):
		"""returns the balance_factor 

		@pre: height correct for all fields
		@rtype: int
		@returns: the balace factor of self, 0 if the node is virtual
		"""
		right_height = self.getRight().getHeigth()
		left_height = self.getLeft().getHeigth()
		return left_height - right_height


	def getRank(self):
		"""gets the rank of a node.
			inOrder(tree)[self.getRank()-1] == self
		
		@rtype: int
		@return: the rank of self
		"""	
		rank = self.getLeft().getSize() + 1
		node = self
		while (node != None):
			parent = node.getParent()
			if ((parent != None) and (node is parent.getRight())):
				# using 'is' to make sure it has the same memory address
				rank += parent.getLeft().getSize() + 1
			node = parent
		return rank


	def setLeft(self, node):
		"""sets left child without rebalance

		@post: updates help fields
		@post: old left deleted
		@type node: AVLNode
		@param node: a node
		"""
		self.left = node
		self.updateHelpers()


	def setRight(self, node):
		"""sets right child without rebalance

		@post: updates help fields
		@post: old right deleted
		@type node: AVLNode
		@param node: a node
		"""
		self.right = node
		self.updateHelpers()


	def setParent(self, node):
		"""sets parent and update the parent node.
		
		@post: old parent deleted
		@type node: AVLNode
		@param node: a node to be the parent of self
		Doesn't affect node
		"""
		self.parent = node


	def setValue(self, value):
		"""sets value. 
		If self was a virtual node, updates help fields and pads with virtual nodes

		@type value: str
		@param value: data
		"""
		if (not self.isRealNode()):
			self.size = 1
			self.height = 0
			self.padWithVirtuals()
		self.value = value

	
	def padWithVirtuals(self):
		"""adds virtual nodes where self has no children"""
		left = self.getLeft()
		if (left == None):
			self.setLeft(AVLNode.virtualNode(parent=self))
		right = self.getRight()
		if (right == None):
			self.setLeft(AVLNode.virtualNode(parent=self))


	def setSize(self, s):
		"""sets the size of the node

		@type s: int
		@param s: the size
		@warning: Doesn't check for correctness
		"""
		self.size = s


	def setHeight(self, h):
		"""sets the height of the node

		@type h: int
		@param h: the height
		@warning: Doesn't check for correctness
		"""
		self.height = h


	def updateSize(self):
		"""sets the size based on the sizes of the left and the right children
		
		@pre: children sizes are updated
		"""
		left = self.getLeft()
		right = self.getRight()
		self.setSize(left.getSize() + right.getSize() + 1)


	def updateHeight(self):
		"""sets the height based on the heights of the left and the right children
		
		@pre: children heights are updated
		"""
		left_height = self.getLeft().getHeight()
		right_height = self.getRight().getHeight()

		self.setHeight(max(left_height, right_height) + 1)


	def updateHelpers(self):
		"""Updates both height and size"""
		self.updateHeight()
		self.updateSize()


	def updateHereAndUp(self):
		"""Updates the help field of self and his parents, up to the root"""
		node = self
		while (node != None):
			node.updateHelpers()
			node = node.getParent()


	def deepHeights(self):
		"""searches into the tree recursivly, 
		updates the height at each node.

		@rtype: int 
		@return: height of the node
		"""
		# handle virtual nodes		
		if (not self.isRealNode()):
			return -1
		
		# recursivly find height of left and right nodes
		left_node = self.getLeft()
		left_height = -1
		if (left_node != None):
			left_height = left_node.deepHeights()
		
		right_node = self.getRight()
		right_height = -1
		if (right_node != None):
			right_height = right_node.deepHeights()
		
		# set the field
		self.setHeight(max(right_height, left_height) + 1)
		return self.getHeight()


	def deepBalanceFactor(self):
		"""serches into the tree recursively,
		updated the height at each node, 
		and then returns the balance factor
		
		@rtype: int
		@return: balance factor of the tree
		"""
		self.deepHeights()
		return self.getBalanceFactor()


	def deepSizes(self):
		"""searches into the tree recursivly, 
		updates the size at each node.

		@rtype: int 
		@return: size of the node
		"""
		# handle virtual nodes
		if (not self.isRealNode()):
			return 0
		
		# recursively find size of left and right nodes
		left_node = self.getLeft()
		left_size = 0
		if (left_node != None):
			left_size = left_node.deepSizes()
		
		right_node = self.getRight()
		right_size = 0
		if (right_node != None):
			right_size = right_node.deepSizes()
		
		# set the field
		self.setSize(left_size + right_size + 1)
		return self.getSize()
		

	def isRealNode(self):
		"""returns whether self is not a virtual node 

		@rtype: bool
		@returns: False if self is a virtual node, True otherwise.
		"""
		return self.value != None


	def rebalance(self, is_insert = False):
		"""rebalance the tree after insertion or deletion of self
		
		@pre: the tree was AVL before modification
		@pre: help fields were not updated 
		@post help fields are updated
		@type is_insert: bool
		@param is_insert: if rebalance is after insertion
		@rtype: int
		@return: number of rotations
		"""
		rotations_count = 0

		parent = self.getParent()
		while parent != None:
			old_height = parent.getHeight()
			parent.updateHelpers()
			balance_factor = parent.getBalanceFactor()
			new_height = parent.getHeight()
			
			if (old_height == new_height):
				break	
			
			elif (-2 < balance_factor < 2):
				parent = parent.getParent()
			
			
			elif (balance_factor == 2):
				# self.left cannot be None 
				left_node = parent.getLeft()
				if (left_node.getBalanceFactor() == -1):
					left_node.rotateLeft()
					rotations_count += 1 
				parent.rotateRight() 
				rotations_count += 1
				if (is_insert): # only one rotation at insertion
					break
			
			elif (balance_factor == -2):
				# self.right cannot be None 
				right_node = parent.getRight()
				if (right_node.getBalanceFactor() == 1):
					right_node.rotateRight()
					rotations_count += 1
				parent.rotateLeft() 
				rotations_count += 1
				if (is_insert): # only one rotation at insertion
					break
			
			else: # this should never happen
				raise Exception("Balance factor is greater then 2 (in absolute value)")
		
		if (parent != None):
			parent.updateHereAndUp()
		return rotations_count


	def rotateLeft(self):
		"""makes self the left child of self.right
		
		@post: update help fields of the node and the child
		"""
		# prepare pointers
		parent = self.getParent()
		child = self.getRight()
		childs_left = child.getLeft()

		# rotate
		self.setRight(childs_left)
		child.setLeft(self)
		child.setParent(parent)	
		
		# update helpers
		self.updateHelpers()
		child.updateHelpers()



	def rotateRight(self):
		"""makes self the right child of self.left
		
		@post: update help fields of the node and the child 
		"""
		# prepare pointers
		parent = self.getParent()
		child = self.getLeft()
		childs_right = child.getRight()

		# rotate
		self.setLeft(childs_right)
		child.setRight(self)
		child.setParent(parent)

		# update helpers
		self.updateHelpers()
		child.updateHelpers()



"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self, size = 0):
		self.size = size
		self.root = AVLNode.virtualNode()
		# add your fields here


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.getRoot.value == None


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		node = self.getRoot
		index = i + 1

		while node.value != None:
			left = node.getLeft().size
			rank  = left.value + 1

			if rank == i:
				return node.value

			if rank > i:
				node = left
				continue

			node = node.right
			index -= (i-rank)
			

	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		if self.size == 0:
			self.root = AVLNode(val, None, None, 1, 1, None)
			return 0

		if i == self.length:
			max = self.findMaximum()
			max.right = biggerNode.createNewSonNode(val)
			max.right.rebalance()
			return # need to return the number of rotations done.

		biggerNode = self.retrieve(i)

		if not biggerNode.hasLeft():
			biggerNode.left = biggerNode.createNewSonNode(val)
			biggerNode.left.rebalance()
			return # need to return the number of rotations done.

		else:
			pred = self.findPredecessor()
			pred.right = pred.createNewSonNode(val)
			pred.right.rebalance()
			return # need to return the number of rotations done. 


	"""find the predecessor of the node in the tree. 

	@pre: self.left != None virtual node
	@rtype: AVLNode
	@returns: predecessor of the node in the tree.
	"""
	def findPredecessor(self):
		node = self.left
		while node.value != None:
			node = node.right

		return node.parent

	"""create a new node to insert in insert() as son. 

	@rtype: AVLNode
	@returns: node to insert
	"""
	def createNewSonNode(self, val):
		return AVLNode(val, None, None, self.getHeight() + 1, self.left.size + self.right.size + 1, self)

	
	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		return -1


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.size == 0:
			return None

		return self.findMinimum().value

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.size == 0:
			return None

		return self.findMaximum().value


	"""find the node with the minimum value in the tree. 

	@pre: self.length > 0 
	@rtype: AVLNode
	@returns: node with the minimum value in the tree. 
	"""
	def findMinimum(self):
		node = self.root
		while node.value is not None:
			node = node.left

		return node.parent


	"""find the node with the maximum value in the tree. 

	@pre: self.length > 0 
	@rtype: AVLNode
	@returns: node with the maximum value in the tree. 
	"""
	def findMaximum(self):
		node = self.root
		while node.value is not None:
			node = node.right

		return node.parent


	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		return None

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.root.size

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		if not self.root.isRealNode():
			return
		
		if self.root == val:
			return self.root.getRank - 1

		res1 = self.search(val)
		if res1 != None:
			return res1

		res2 = self.search(val)
		if res2 != None:
			return res2		


	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		if self.size == 0:
			return None

		return self.root

