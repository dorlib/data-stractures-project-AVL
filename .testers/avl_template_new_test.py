import avl_template_new as avl
import unittest
import random

class Test_AVLNode(unittest.TestCase):
    def setUp(self):
        # called before each test
        self.a = avl.AVLNode("a", None, None, 0, 1)
        self.d = avl.AVLNode("d", None, None, 0, 1)
        self.b = avl.AVLNode("b", self.a, None, 1, 2)
        self.c = avl.AVLNode("c", self.b, self.d, 2, 4)
        self.a.setParent(self.b) #       (c)
        self.b.setParent(self.c) #    (b)↲ ↳(d)
        self.d.setParent(self.c) # (a)↲

    def test_attributes_override(self):
        node = avl.AVLNode.virtualNode()
        assert type(node.right) == avl.AVLNode # it passed through __getattr__
        
        child = avl.AVLNode.virtualNode(node)
        node.right = child
        assert node.getRight() is child # it passed through __setattribute__
        assert child.parent is node

    def test_updates_lonely_node(self):
        # node without children
        self.c.setLeft(avl.AVLNode.virtualNode(self.c))
        self.c.setRight(avl.AVLNode.virtualNode(self.c))
        self.c.updateHelpers()
        assert self.c.getHeight() == 0, "height is incorrect"
        assert self.c.getSize() == 1, "size is incorrect"

    def test_updates_left_leaning(self):
        # left is bigger and longer
        self.c.setHeight(0) # mess up the fields
        self.c.setSize(0)
        self.c.updateHelpers()
        assert self.c.getHeight() == 2, "height is incorrect"
        assert self.c.getSize() == 4, "size is incorrect"
    
    def test_update_right_leaning(self):
        self.c.setLeft(self.c.getRight()) # switch sides
        self.c.setRight(self.b)
        self.c.setHeight(0) # mess up fields
        self.c.setSize(0)
        self.c.updateHelpers()
        assert self.c.getHeight() == 2, "height is incorrect"
        assert self.c.getSize() == 4, "size is incorrect"
    
    def test_deep_heights(self):
        self.a.setHeight(0)
        self.b.setHeight(0)
        self.c.setHeight(0)
        self.d.setHeight(0)
        
        self.c.deepHeights()
        assert self.a.getHeight() == 0, f"a error"
        assert self.b.getHeight() == 1, f"b error"
        assert self.c.getHeight() == 2, f"c error"
        assert self.d.getHeight() == 0, f"d error"

    def test_getters(self):
        node = avl.AVLNode.virtualNode() # has None for children
        assert type(node.getLeft()) == avl.AVLNode
        assert type(node.getRight()) == avl.AVLNode

    def test_rebalance_after_deletion(self):
        # delete (d)
        self.c.setRight(avl.AVLNode.virtualNode())
        #       (c)
        #    (b)↲
        # (a)↲
        self.d.rebalance()
        #    (b)
        # (a)↲ ↳(c)
        assert self.b.getLeft() == self.a, f"b.left is {self.b.getLeft()}"          
        assert self.b.getRight() == self.c, f"b.right is {self.b.getRight()}"       
        assert self.b.getParent() == None, f"b.parent is {self.b.getParent()}"
        assert self.b.getHeight() == 1, f"b.height is {self.b.getHeight()}"
        assert self.a.getHeight() == self.c.getHeight() == 0, f"height are a: {self.a.getHeight()}, c: {self.c.getHeight()}"
        assert self.a.getParent() == self.c.getParent() == self.b, f"parents are a: {self.a.getParent()}, c: {self.c.getParent()}"

    def test_rebalance_after_insertion(self):
        # insert (e) to the right of (a)
        e = self.a.getRight()
        e.setValue("e")
        #       (c)
        #    (b)↲ ↳(d)
        # (a)↲
        #   ↳(e)
        e.rebalance(is_insert=True)
        #          ( c )
        #       (e)↲   ↳(d) 
        #    (a)↲ ↳(b)
        assert e.getParent() == self.c, f"e.parent = {e.getParent()}"
        assert e.getLeft() == self.a, f"e.left = {e.getLeft()}"
        assert e.getRight() == self.b, f"e.right = {e.getRight()}"
        assert self.a.getParent() == e, f"a.parent = {self.a.getParent()}"
        assert self.b.getParent() == e, f"a.parent = {self.b.getParent()}"
        assert (not self.a.right.isRealNode()) and (not self.a.left.isRealNode()), \
                f"a.left = {self.a.getLeft()}, a.right = {self.a.getRight()}"
        assert (not self.b.getRight().isRealNode()) and (not self.b.getLeft().isRealNode()), \
                f"a.left = {self.b.getLeft()}, a.right = {self.b.getRight()}"
    
    def test_copy(self):
        copy = self.c.copyForSort()
        origin = self.c

        def rec_assert_copy(copy, origin):
            assert copy is not origin, f"same instance {copy}, {origin}"
            assert copy.value == origin.value, f"different value {copy}, {origin}"
            if copy.isRealNode():
                rec_assert_copy(copy.right, origin.right)
                rec_assert_copy(copy.left, origin.left)
    
        rec_assert_copy(copy, origin)
    
    def test_adding_and_removing_pointers(self):
        copy = self.c.copyForSort(set_list_node=True)
        origin = self.c

        def rec_assert_copy(copy, origin):
            assert copy is not origin, f"same instance {copy}, {origin}"
            assert copy.getListNode() is origin or origin.value == None, f"pointer error {copy}, {origin}"
            assert copy.value == origin.value, f"different value {copy}, {origin}"
            if copy.isRealNode():
                rec_assert_copy(copy.right, origin.right)
                rec_assert_copy(copy.left, origin.left)
    
        rec_assert_copy(copy, origin)

        # test_pointer_deletion
        copy.removeListNodePointers()
        assert copy.getListNode() == None
        assert copy.getLeft().getListNode() == None
        assert copy.getRight().getListNode() == None

class Test_AVLTreeList(unittest.TestCase):
    def setUp(self):
        # called before each test
        self.a = avl.AVLNode("a", None, None, 0, 1)
        self.d = avl.AVLNode("d", None, None, 0, 1)
        self.b = avl.AVLNode("b", self.a, None, 1, 2)
        self.c = avl.AVLNode("c", self.b, self.d, 2, 4)
        self.a.setParent(self.b) #       (c)
        self.b.setParent(self.c) #    (b)↲ ↳(d)
        self.d.setParent(self.c) # (a)↲

    def test_insertion_to_avl_search_tree(self):
        list = avl.AVLTreeList()
        nodes_to_insert = [self.a, self.b, self.c, self.d]
        for i in range(24): #4!=24
            random.shuffle(nodes_to_insert)
            
            list = avl.AVLTreeList(size=4)
            list.setRoot(self.c)
            for node in nodes_to_insert:
                list.insertToSearchTree(node)
            
            root = list.sorted_root
            assert root.deepHeights() == 2
            assert abs(root.getBalanceFactor()) < 2
            assert root.value > root.left.value 
            assert root.value < root.right.value

    def test_double_insertion(self):
        # init list
        self.list = avl.AVLTreeList(size=4)
        self.list.setRoot(self.c)
        self.list.setSortedRoot(self.c.copyForSort(True))
        # insert some node (no need for rotations)
        a_copy = self.a.copyForSort()
        a_copy.setParent(self.d)
        self.d.setLeft(a_copy)
        a_copy.updateHereAndUp()
        # test insert
        self.list.insertToSearchTree(a_copy)
        found = self.list.searchInSorted("a")
        
        assert found != None
        assert found.left.value == "a" or found.right.value == "a" or found.getSuccessor().left.value == "a"
    
    def test_deletion(self):
        #init
        self.test_double_insertion()

        list_root = self.list.getRoot()
        self.list.deleteFromSearchTree(list_root)
        assert self.list.searchInSorted(list_root.value).value == None, "not deleted"
        assert self.list.searchInSorted("a"), "deleted a"
        assert self.list.searchInSorted("b"), "deleted b"
        assert self.list.searchInSorted("d"), "deleted d"

        a_origin = list_root.left.left
        a_copy = list_root.right.left
        self.list.deleteFromSearchTree(a_copy) # delete duplicate a
        stayed_a = self.list.searchInSorted("a")
        assert stayed_a.value != None, "deleted both nodes" 
        assert stayed_a.list_node is a_origin, "deleted wrong node"
        assert self.list.searchInSorted("b"), "deleted b"
        assert self.list.searchInSorted("d"), "deleted d"

    def test_sort(self):
        list = avl.AVLTreeList(4)
        nodes_to_insert = [self.a, self.b, self.c, self.d]
        for i in range(24): #4!=24
            random.shuffle(nodes_to_insert)
            
            list = avl.AVLTreeList(size=4)
            list.setRoot(self.c)
            for node in nodes_to_insert:
                list.insertToSearchTree(node)
            sorted = list.sort()
            root = sorted.getRoot()
            sorted_root = sorted.getSortedRoot()
            assert not sorted is list
            assert root.value == sorted_root.value
            assert root.left.value == sorted_root.left.value
            assert root.right.value == sorted_root.right.value
            z = avl.AVLNode("z",None,None)
            sorted.insertToSearchTree(z)
            assert list.searchInSorted("z").value == None, "z inserted to both lists"
    
    def test_sort_empty(self):
        list = avl.AVLTreeList()
        assert type(list.sort()) == avl.AVLTreeList


            
        

if __name__ == "__main__":
    unittest.main()