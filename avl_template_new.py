#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  

import warnings #TODO delete all warnings bafore submition
import random


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
	def __init__(self, value, left=None, right=None, height=None, size=None, 
				parent=None, is_real=True):
		"""Constructor, creates a real node.
		if node should be a real node, pads with virtuals
		
		@type value: str or None
		@param value: data of your node
		@type left: AVLNode
		@param left: left child the node
		@type right: AVLNode
		@param right: right child of the node
		@type height: int
		@param height: length of the longest path to a leaf. Updates from children if None
		@type size: int
		@param size: the number of nodes in the subtree. Updates from children if None
		@type parent: AVLNode
		@param parent: parent of the node
		@type is_real: bool
		@param is_real: is this node real or not
		@time complexity: O(1)
		"""
		# Convention: attributes starting with p_ are private
		self.p_value = value 
		
		# pointers
		self.p_left = left
		self.p_right = right
		self.p_parent = parent
		

		# padding with virtual nodes
		if (is_real):
			self.padWithVirtuals()

	
		# help fields
		self.p_height = height
		if height == None:
			self.updateHeight()
		
		self.p_size = size
		if size == None:
			self.updateSize()
		
		

	@staticmethod
	def virtualNode(parent=None):
		"""creates a new virtual node assigned with given parent
		
		@type parent: AVLNode 
		@param parent: node to be the parent
		@time complexity: O(1)
		"""
		return AVLNode(	value=None,
						left=None,
						right=None,
						height=-1,
						size=0,
						parent=parent,
						is_real=False)


	def __repr__(self):
		""" Overrides the str representation of a node.

		@rtype: str
		@return: "node" and then the value of the node
		@time complexity: O(1)
		"""
		if self.isRealNode():
			return f"node: {self.getValue()}"
		return "a virtual node"


	def __getattr__(self, name):
		"""Overrides get attributes.
		
		Runs iff __getarttribute__ couldn't find name.
		Should not be called explicitly, only by using
		node_instance.name
		@type name: str
		@param name: the attribute to be found
		@time complexity: O(1)
		"""
		if name == "value":
			return self.getValue()
		elif name == "right":
			return self.getRight()
		elif name == "left":
			return self.getLeft()
		elif name == "parent":
			return self.getParent()
		elif name == "height":
			return self.getHeight()
		elif name == "size":
			return self.getSize()
		elif name == "balance_factor":
			return self.getBalanceFactor()
		


	def __setattr__(self, name, value):
		"""Overrides some set attributes
		
		if none of the options, falls back to default behavior
		Should not be called explicitly, only by using
		node_instance.name = value
		@type name: str
		@param name: the attribute to be set
		@time complexity: O(1)
		"""
		if name == "value":
			self.setValue(value)
		elif name == "right":
			self.setRight(value)
		elif name == "left":
			self.setLeft(value)
		elif name == "parent":
			self.setParent(value)
		elif name == "height":
			self.setHeight(value)
		elif name == "size":
			self.setSize(value)
		else: # default behavior
			object.__setattr__(self, name, value)
	

	def getLeft(self):
		"""returns the left child

		@rtype: AVLNode
		@returns: the left child of self, virtualNode if there is no left child
		@time complexity: O(1)
		"""
		left = self.p_left
		if left == None and self.isRealNode():
			warnings.warn(f"a node with the value {self} left child was None") # TODO delete this warning before submition
			return AVLNode.virtualNode(self)
		return left
		

	def getRight(self):
		"""returns the right child

		@rtype: AVLNode
		@returns: the right child of self, None if there is no right child
		@time complexity: O(1)
		"""
		right = self.p_right 
		if right == None and self.isRealNode():
			warnings.warn(f"a node with the value {self} right child was None") # TODO delete this warning before submition
			return AVLNode.virtualNode(self)
		return right


	def hasLeft(self):
		"""checks if the left child is a real node

		@rtype: bool
		@return: left != None and left is a real node
		@time complexity: O(1)
		"""
		left = self.getLeft()
		return left != None and left.isRealNode()


	def hasRight(self):
		"""checks if the right child is a real node

		@rtype: bool
		@return: right != None and right is a real node
		@time complexity: O(1)
		"""
		right = self.getRight()
		return right != None and right.isRealNode()


	def getParent(self):
		"""returns the parent 

		@rtype: AVLNode
		@returns: the parent of self, None if there is no parent
		@time complexity: O(1)
		"""
		return self.p_parent


	def getValue(self):
		"""return the value

		@rtype: str
		@returns: the value of self, None if the node is virtual
		@time complexity: O(1)
		"""
		return self.p_value


	def getSize(self):
		"""returns the size field
		
		@rtype: int
		@returns: the number of nodes in the subtree below self (inclusive)
		Doesn't check for correctness
		@time complexity: O(1)
		"""
		return self.p_size
	

	def getHeight(self):
		"""returns the height field

		@pre: height is correct
		@rtype: int
		@returns: the height of self, -1 if the node is virtual.
		@time complexity: O(1)
		"""
		return self.p_height


	def getBalanceFactor(self):
		"""returns the balance_factor 
		
		@pre: height correct for all fields
		@rtype: int
		@returns: the balace factor of self, 0 if the node is virtual
		@time complexity: O(1)
		"""
		if not self.isRealNode():
			return 0
		right_height = self.getRight().getHeight()
		left_height = self.getLeft().getHeight()
		return left_height - right_height


	def getRank(self):
		"""gets the rank of a node.
			inOrder(tree)[self.getRank()-1] == self
		
		@rtype: int
		@return: the rank of self
		@time complexity: O(log n)
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
		"""sets left child 

		@post: doesn't update help fields
		@post: old left deleted
		@post: does not rebalance
		@type node: AVLNode
		@param node: a node
		@time complexity: O(1)
		"""
		self.p_left = node


	def setRight(self, node):
		"""sets right child 

		@post: doesn't update help fields
		@post: old right deleted
		@post: does not rebalance
		@type node: AVLNode
		@param node: a node
		@time complexity: O(1)
		"""
		self.p_right = node


	def setParent(self, parent):
		"""sets parent 
		
		@post: old parent deleted
		@post: doesn't affect parent
		@type parent: AVLNode
		@param parent: a node to be the parent of self
		@time complexity: O(1)
		"""
		self.p_parent = parent


	def setValue(self, value):
		"""sets value. 

		@post: If self was virtual, updates help fields and pads with virtual nodes
		@type value: str
		@param value: data
		@time complexity: O(1)
		"""
		if (not self.isRealNode()):
			self.p_size = 1
			self.p_height = 0
			self.padWithVirtuals()
		self.p_value = value

	
	def padWithVirtuals(self):
		"""adds virtual nodes where self has no children
		
		@time complexity: O(1)
		"""
		left = self.p_left # unsafe attribute access
		if (left == None):
			self.p_left = AVLNode.virtualNode(parent=self)
		right = self.p_right # unsafe attribute access
		if (right == None):
			self.p_right = AVLNode.virtualNode(parent=self)


	def setSize(self, s):
		"""sets the size of the node

		@pre: inserted size is correct
		@type s: int
		@param s: the size
		@time complexity: O(1)
		"""
		self.p_size = s


	def setHeight(self, h):
		"""sets the height of the node

		@pre: inserted height is correct
		@type h: int
		@param h: the height
		@time complexity: O(1)
		"""
		self.p_height = h


	def updateSize(self):
		"""sets the size based on the sizes of the left and the right children
		
		@pre: children sizes are updated
		@time complexity: O(1)
		"""
		left = self.getLeft()
		right = self.getRight()
		self.setSize(left.getSize() + right.getSize() + 1)


	def updateHeight(self):
		"""sets the height based on the heights of the left and the right children
		
		@pre: children heights are updated
		@time complexity: O(1)
		"""
		left_height = self.getLeft().getHeight()
		right_height = self.getRight().getHeight()

		self.setHeight(max(left_height, right_height) + 1)


	def updateHelpers(self):
		"""Updates both height and size
		
		@pre: children size and height are correct
		@time complexity: O(1)
		"""
		self.updateHeight()
		self.updateSize()


	def updateHereAndUp(self):
		"""Updates the help field of self and his parents, up to the root
		
		@time complexity: O(log n)
		"""
		node = self
		while (node != None):
			node.updateHelpers()
			node = node.getParent()


	def isRealNode(self):
		"""returns whether self is not a virtual node 

		@rtype: bool
		@returns: False if self is a virtual node, True otherwise.
		@time complexity: O(1)
		"""
		return self.p_height != -1 and self.p_size != 0


	def rebalance(self, is_insert = False):
		"""rebalance the tree after insertion or deletion of self
		
		@pre: the tree was AVL before modification
		@pre: help fields were not updated 
		@post help fields are updated
		@type is_insert: bool
		@param is_insert: if rebalance is after insertion
		@rtype: int
		@return: number of rotations
		@time complexity: O(log n)
		"""
		rotations_count = 0

		parent = self.getParent()
		while parent != None:
			old_height = parent.getHeight()
			parent.updateHelpers()
			balance_factor = parent.getBalanceFactor()
			new_height = parent.getHeight()
			
			if ((-2 < balance_factor < 2) and old_height == new_height):
				break	
			
			elif (-2 < balance_factor < 2):
				parent = parent.getParent()
				continue # for readability
			
			
			elif (balance_factor == 2):
				# self.left cannot be None 
				left_node = parent.getLeft()
				if (left_node.getBalanceFactor() == -1):
					left_node.rotateLeft()
					rotations_count += 1 
				parent = parent.rotateRight() # iterate upwards
				rotations_count += 1
				if (is_insert): # only one rotation at insertion
					break

			
			elif (balance_factor == -2):
				# self.right cannot be None 
				right_node = parent.getRight()
				if (right_node.getBalanceFactor() == 1):
					right_node.rotateRight()
					rotations_count += 1
				parent = parent.rotateLeft() # iterate upwards
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
		@rtype: AVLNode
		@return: the original parent of self (before rotation)
		@time complexity: O(1)
		"""
		# prepare pointers
		parent = self.getParent()
		child = self.getRight()
		childs_left = child.getLeft()

		# rotate
		childs_left.setParent(self)
		self.setRight(childs_left)
		self.setParent(child)
		child.setLeft(self)
		child.setParent(parent)
		if (parent != None):
			if (parent.getLeft() is self):
				parent.setLeft(child)
			elif (parent.getRight() is self):
				parent.setRight(child)
			else:
				raise Exception("parent was disconnected from rotated node")

		# update helpers
		self.updateHelpers()
		child.updateHelpers()
		return parent


	def rotateRight(self):
		"""makes self the right child of self.left
		
		@post: update help fields of the node and the child 
		@rtype: AVLNode
		@return: the original parent of self (before rotation)
		@time complexity: O(1)
		"""
		# prepare pointers
		parent = self.getParent()
		child = self.getLeft()
		childs_right = child.getRight()

		# rotate
		childs_right.setParent(self)
		self.setLeft(childs_right)
		self.setParent(child)
		child.setRight(self)
		child.setParent(parent)
		if (parent != None):
			if (parent.getLeft() is self):
				parent.setLeft(child)
			elif (parent.getRight() is self):
				parent.setRight(child)
			else:
				raise Exception("parent was disconnected from rotated node")
			

		# update helpers
		self.updateHelpers()
		child.updateHelpers()
		return parent
	
	
	def getPredecessor(self):
		"""find the predecessor of the node in the tree. 

		@rtype: AVLNode
		@returns: predecessor of the node in the tree.
		@time complexity: O(log n)
		"""
		return self.getSucOrPred(
			hasChild=lambda x: x.hasLeft(),
			getChild=lambda x: x.getLeft(),
			getOtherChild=lambda x: x.getRight(),
		)
				
	def getSuccessor(self):
		"""find the successor of the node in the tree. 

		@rtype: AVLNode
		@returns: successor of the node in the tree.
		@time complexity: O(log n)
		"""
		return self.getSucOrPred(
			hasChild=lambda x: x.hasRight(),
			getChild=lambda x: x.getRight(),
			getOtherChild=lambda x: x.getLeft(),
		)
	
	def getSucOrPred(self, hasChild, getChild, getOtherChild):
		"""logic for get successor and get predecessor.
		
		@type hasChild: lambda AVLNode: bool
		@param hasChild: check if has left or right child
		@type hasChild: lambda AVLNode: AVLNode
		@param hasChild: gets the same that hasChild checks
		@type hasChild: lambda AVLNode: AVLNode
		@param hasChild: gets the other child
		@rtype: AVLNode
		@returns: successor or predeccesor of the node in the tree.
		@time complexity: O(log n)
		"""
		if hasChild(self):
			node = getChild(self)
			while node.isRealNode():
				node = getOtherChild(node)
			return node.getParent()
		else:
			node = self
			parent = node.getParent()
			while parent != None and node is getChild(parent):
				node = parent
				parent = parent.getParent()
			return parent
				


"""
A class implementing the ADT list, using an AVL tree.
"""
class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self, size = 0, root = AVLNode.virtualNode(), firstNode=None, lastNode=None):
		self.size = size
		self.root = root
		self.firstNode = firstNode
		self.lastNode = lastNode


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.getRoot() is None or not self.getRoot().isRealNode()


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if self.length() <= i or i < 0:
			return None

		node = self.getRoot()
		index = i + 1

		while node.isRealNode():
			rank  = node.getLeft().size + 1

			if rank == index:
				return node.getValue()

			if rank > index:
				node = node.left
				continue

			node = node.getRight()
			index = (index-rank)


	"""retrieves the node of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: AVLNode
	@returns: the the node of the i'th item in the list
	"""
	def retrieveNode(self, i):
		node = self.getRoot()
		index = i + 1

		while node.isRealNode():
			rank  = node.getLeft().size + 1

			if rank == index:
				return node

			if rank > index:
				node = node.getLeft()
				continue

			node = node.getRight()
			index = (index-rank)



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
			self.root = AVLNode(val, None, None, 0, 1, None)
			self.firstNode = self.lastNode = self.root
			self.size = 1
			return 0

		if i == self.length():
			max = self.findLastNode()
			max.right = AVLNode(val, None, None, 0, 1, max)
			self.size += 1
			
			numOfRotations = max.right.rebalance(True)
			self.updatePointers()
			return numOfRotations

		biggerNode = self.retrieveNode(i)

		if not biggerNode.hasLeft():
			biggerNode.left = AVLNode(val, None, None, 0, 1, biggerNode)
			self.size += 1
			
			numOfRotations = biggerNode.left.rebalance(True)
			self.updatePointers()
			return numOfRotations

		else:
			pred = biggerNode.getPredecessor()
			pred.right = AVLNode(val, None, None, 0, 1, pred)
			self.size += 1

			numOfRotations =  pred.right.rebalance(True)
			self.updatePointers()
			return numOfRotations

	
	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		if i >= self.length() or i < 0:
			return -1

		nodeToDelete = self.retrieveNode(i)
		parent = nodeToDelete.getParent()

		# nodeToDelete is a leaf.
		if not nodeToDelete.hasRight() and not nodeToDelete.hasLeft():
			return self.deleteLeaf(nodeToDelete, parent)
			
		# nodeToDelete has only one child.
		elif (not nodeToDelete.hasRight() and nodeToDelete.hasLeft()) or (nodeToDelete.hasRight() and not nodeToDelete.hasLeft()):
			return self.deleteNodeWithOneChild(nodeToDelete, parent)

		# nodeToDelete has two childes.
		return self.deleteNodeWithTwoChild(nodeToDelete, parent)


	"""deletes the i'th item in the list if its a leaf

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def deleteLeaf(self, nodeToDelete, parent):
		virtNode = AVLNode.virtualNode(parent)
		
		if parent == None:
			nodeToDelete = virtNode
			self.size -= 1
			self.root = self.firstNode = self.lastNode = nodeToDelete
			return 0

		elif parent.getRight() is nodeToDelete:
			parent.right = virtNode
			numOfRotations = parent.getRight().rebalance()
		else:
			parent.left = virtNode
			numOfRotations = parent.getLeft().rebalance()

		self.size -= 1
		self.updatePointers()

		return numOfRotations 


	"""deletes the i'th item in the list if it has only one child

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def deleteNodeWithOneChild(self, nodeToDelete, parent):
		if not nodeToDelete.hasRight() and nodeToDelete.hasLeft():
			if parent is None:
				self.root = nodeToDelete.getLeft()
				nodeToDelete.getLeft().parent = parent
			else:
				if parent.getRight() is nodeToDelete:
					parent.setRight(nodeToDelete.getLeft())
				else: # parent.left is nodeToDelete
					parent.setLeft(nodeToDelete.getLeft())
				nodeToDelete.getLeft().parent = parent

			
			numOfRotations = nodeToDelete.getLeft().rebalance()
			self.size -=1
			self.updatePointers()

			return numOfRotations

		elif nodeToDelete.hasRight() and not nodeToDelete.hasLeft():
			if parent is None:
				self.root = nodeToDelete.getRight()
				nodeToDelete.getRight().parent = parent
			else:
				if parent.getRight() is nodeToDelete:
					parent.setRight(nodeToDelete.getRight())
				else: # parent.left is nodeToDelete
					parent.setLeft(nodeToDelete.getRight())
				nodeToDelete.getRight().parent = parent

			numOfRotations = nodeToDelete.getRight().rebalance()
			self.size -=1
			self.updatePointers()

			return numOfRotations


	"""deletes the i'th item in the list if it has 2 childs
	
	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def deleteNodeWithTwoChild(self, nodeToDelete, parent):
		successor = nodeToDelete.getSuccessor()
		successorParent = successor.getParent()
		# replace with the successor
		nodeToDelete.setValue(successor.getValue())
		# delete the successor
		if successor.hasRight():
			return self.deleteNodeWithOneChild(successor, successorParent)
		else: # successor is a leaf
			return self.deleteLeaf(successor, successorParent)
      
	
	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.size == 0:
			return None

		return self.firstNode.value

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.size == 0:
			return None

		return self.lastNode.value


	"""find the first node in the tree. 

	@pre: self.length > 0 
	@rtype: AVLNode
	@returns: the first node in the tree. 
	"""
	def findFirstNode(self):
		node = self.root
		while node.isRealNode():
			node = node.left

		return node.parent


	"""find the last node in the tree. 

	@pre: self.length > 0 
	@rtype: AVLNode
	@returns: the last node in the tree. 
	"""
	def findLastNode(self):
		node = self.root
		while node.isRealNode():
			node = node.right

		return node.getParent()


	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		if self.size == 0:
			return []

		current = self.getRoot()
		stack = [] 
		result = [0] * self.size
		i = 0
		
		while True:
			if current.isRealNode():
				stack.append(current)
				current = current.getLeft()

			elif(stack):
				current = stack.pop()
				result[i] = current.getValue()
				current = current.getRight()
				i += 1
	
			else:
				break
		
		return result

	@staticmethod
	def arrayToList(arr):
		""" Turns arr to a list

		@type arr: list
		@param arr: array to turn into a list
		"""
		def arrToList_rec(arr, start, end, parent):
			""" act as if arr is from start (inclusive)
			to end (not inclusive).
			"""
			if start >= end:
				return AVLNode.virtualNode(parent)
			mid = start + (end - start)//2
			root = AVLNode(arr[mid], parent=parent)
			left = arrToList_rec(arr, start, mid, root)
			right = arrToList_rec(arr, mid+1, end, root)
			
			root.setLeft(left)
			root.setRight(right)
			root.updateHelpers()
			return root
		if len(arr) == 0:
			return AVLTreeList(0)

		lst_root = arrToList_rec(arr, 0, len(arr), None)
		lst = AVLTreeList(len(arr), lst_root)
		lst.updatePointers()
		return lst

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		if self and self.root.isRealNode():
			return self.size
		
		return 0

	def sort(self):
		"""sort the info values of the list

		@rtype: AVLTreeList
		@returns: new list values are sorted by the info of the original list.
		"""
		array = self.listToArray()
		new_list = AVLTreeList(0, AVLNode.virtualNode())
		for item in array:
			new_list.insertAsSearchTree(item)
		return new_list


	def searchInSorted(self, value):
		"""searches into the tree as if it was a BST
		
		@pre: list is a BST
		@post: if value == None, returns the first node
		@type value: str
		@param value: value to search for
		@rtype: AVLNode
		@return: the node where value is or should be (if not in the search tree)
		"""
		if value == None:
			return self.findFirstNode()

		node = self.root
		while node.isRealNode():
			node_value = node.getValue()
			if value == node_value:
				return node
			elif node_value == None or value > node_value:
				node = node.getRight()
			else: # value < node_value
				node = node.getLeft()
		return node


	def insertAsSearchTree(self, value):
		"""insert to the list in sorted way (BST)
		used for sorting

		@pre: list is a BST
		@post: insert to list as search tree
		@post: if there's more then one occurance, insert right next to it.
		@type value: str
		@param value: value inserted to the list
		"""
		place_to_insert = self.searchInSorted(value)

		if place_to_insert.isRealNode():
			# this is a repeating value, check for children
			if not place_to_insert.hasLeft():
				# insert to the left
				place_to_insert = place_to_insert.getLeft()

			elif not place_to_insert.hasRight():
				# insert to the right
				place_to_insert = place_to_insert.getRight()

			else: # has both children
				successor = place_to_insert.getSuccessor()
				# successor has no left child
				place_to_insert = successor.getLeft()

		place_to_insert.setValue(value)
		place_to_insert.padWithVirtuals()
		place_to_insert.rebalance(is_insert=True)
		self.size += 1
		# update the pointers 
		self.updatePointers()



	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list.
	"""
	def permutation(self):
		lst = self.listToArray()
		lst = self.shuffle(lst)

		tree = AVLTreeList.arrayToList(lst)
		
		return tree


	""" A function to generate a random permutation of arr[]

	@rtype: list
	@returns: a list where the values are permuted randomly by the info of the original list.
	"""
	def shuffle(self, array):
		arrLength = len(array)

		for i in range(arrLength - 1, 0, -1):
			j = random.randint(0, i)
			array[i], array[j] = array[j], array[i]
		
		return array


	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		absDiff = abs(self.root.getHeight() - lst.root.getHeight())
		
		# handle case original or given lists are empty
		if lst.size == 0:
			return absDiff
		if self.size == 0:
			self.root = lst.root
			self.size = lst.size
			self.updatePointers()
			return absDiff


		if self.root.getHeight() >= lst.root.getHeight():
			self.concatSelfIsBigger(lst)
		else:
			self.concatGivenIsBigger(lst)

		self.size += lst.size + 1
		self.updatePointers()
		return absDiff

	def concatGivenIsBigger(self, givenTree):
		"""concat if given tree has greater height
		
		should only be called from concat
		@type givenTree: AVLTreeList
		@param givenTree: tree to concatenate to self
		"""
		originalTree = self
		
		maxInOriginal = originalTree.lastNode
		originalTree.delete(originalTree.size - 1)

		b = givenTree.getRoot()
		while b.getHeight() > originalTree.root.getHeight():
			b = b.getLeft()
		

		# if b is not the root of lst
		if b.getParent() != None:
			maxInOriginal.parent = b.getParent()
			b.getParent().left = maxInOriginal

			maxInOriginal.right = b
			b.parent = maxInOriginal

			maxInOriginal.left = originalTree.getRoot()
			maxInOriginal.updateHelpers()
			originalTree.root.parent = maxInOriginal

			maxInOriginal.rebalance()
			self.root = givenTree.root

		# if b is the root of lst
		else:
			maxInOriginal.parent = None
			maxInOriginal.right = b
			b.parent = maxInOriginal

			maxInOriginal.left = originalTree.getRoot()
			maxInOriginal.updateHelpers()
			originalTree.root.parent = maxInOriginal

			self.root = maxInOriginal


	def concatSelfIsBigger(self, givenTree):
		"""concat if the original tree has grater height
		
		should only be called from concat
		@type givenTree: AVLTreeList
		@param givenTree: tree to concatenate to self
		"""

		firstInGiven = givenTree.firstNode
		givenTree.delete(0)
		
		b = self.getRoot()
		while b.getHeight() > givenTree.root.getHeight():
			b = b.getRight()
		
		# if b is not the root of originalTree
		if b.getParent() != None:
			firstInGiven.parent = b.getParent()
			b.getParent().right = firstInGiven

			firstInGiven.left = b
			b.parent = firstInGiven
			
			firstInGiven.right = givenTree.getRoot()
			firstInGiven.updateHelpers()
			givenTree.root.setParent(firstInGiven)
			
			firstInGiven.rebalance()

		# if b is the root of originalTree
		else:
			firstInGiven.parent = None
			firstInGiven.left = b
			b.parent = firstInGiven

			firstInGiven.right = givenTree.getRoot()
			firstInGiven.updateHelpers()
			givenTree.root.setParent(firstInGiven)

			self.root = firstInGiven
			

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		arr = self.listToArray()
		
		for i in range (len(arr)):
			if arr[i] == val:
				return i
		
		return -1


	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		if self.size == 0:
			return None

		return self.root
	
	def setRoot(self, node):
		"""sets the root of the tree representing the list
		
		@type node: AVLNode
		@param node: node to be the new root 
		"""
		self.root = node

	"""finds the new root of the tree

	@rtype: AVLNode
	@return: the root of the tree
	"""
	def findRoot(self):
		root = self.root

		while root.getParent() != None:
			root = root.getParent()
		
		return root

	"""updates the root, lastNode and firstNode after rebalancing  

	"""
	def updatePointers(self):
		# update root
		self.setRoot(self.findRoot())

		if self.empty():
			self.firstNode = self.root
			self.lastNode = self.root
		
		else:
			# update firstNode
			self.firstNode = self.findFirstNode()

			# update lastNode
			self.lastNode = self.findLastNode()

	def append(self, value):#TODO delete before submission
		self.insert(self.length(), value)
