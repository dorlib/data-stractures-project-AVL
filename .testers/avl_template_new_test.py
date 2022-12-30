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

    def test_successor(self):
        assert self.a.getSuccessor() is self.b
        assert self.d.getSuccessor() == None

        self.e = avl.AVLNode("e",parent=self.b)
        self.b.setRight(self.e)
        assert self.e.getSuccessor() is self.c
        
        self.f = avl.AVLNode("f",parent=self.e)
        self.e.setRight(self.f)
        assert self.f.getSuccessor() is self.c
        assert self.e.getSuccessor() is self.f

    def test_predecessor(self):
        assert self.b.getPredecessor() is self.a
        assert self.a.getPredecessor() == None

        self.e = avl.AVLNode("e",parent=self.d)
        self.d.setLeft(self.e)
        assert self.e.getPredecessor() is self.c

        self.f = avl.AVLNode("f",parent=self.e)
        self.e.setLeft(self.f)
        assert self.f.getPredecessor() is self.c, self.f.getPredecessor()
        assert self.e.getPredecessor() is self.f

    def test_attributes_override(self):
        node = avl.AVLNode.virtualNode()
        node.value = None
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
    
    def test_getters(self):
        node = avl.AVLNode.virtualNode() # has None for children
        assert node.getLeft() == None
        assert node.getRight() == None

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
    

class Test_AVLTreeList(unittest.TestCase):
    def setUp(self):
        self.LETTERS = [None]+list("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890")

    def test_insertion(self):
        self.lst = avl.AVLTreeList()
        for i in range(10):
            self.lst.insert(i, str(i))
            assert self.lst.last() == str(i)
        
        # insert in the middle
        self.lst.insert(5, "%")
        assert self.lst.retrieve(4) == "4"
        assert self.lst.retrieve(5) == "%"
        assert self.lst.retrieve(6) == "5"


    def test_list_to_array(self):
        self.test_insertion()
        array = self.lst.listToArray()
        lst = [str(i) if i <= 5 else str(i-1) for i in range(11)]
        lst[5] = "%"
        assert array == lst
    
    def test_delete(self):
        self.lst = avl.AVLTreeList()
        for i in range (10):
            self.lst.insert(i, "_")
        
        for i in range(11):
            self.lst
    
    def test_sort(self):
        array = [str(i) for i in range(7)]
        for i in range(10000): # 10000 > 7!
            permutation = avl.AVLTreeList.shuffle(avl.AVLTreeList(), array.copy())
            list = avl.AVLTreeList(0, avl.AVLNode.virtualNode())
            for i, val in enumerate(permutation):
                list.insert(i, val)
            sorted = list.sort()
            assert list.listToArray() == permutation, "sort was inplace"
            assert sorted.listToArray() == array, str(sorted.listToArray())
    
    def test_sort_with_duplicates(self):
        lst = avl.AVLTreeList()
        lst.insert(0,'a')
        lst.insert(1,'d')
        lst.insert(2,'b')
        lst.insert(3,'c')
        lst.insert(4,'e')
        lst.insert(5,'b')
        # [a,d,b,c,e,b]
        fst_b = lst.retrieve(2)
        scnd_b = lst.retrieve(5)
        sorted = lst.sort()
        # [a,b,b,c,d,e]
        assert sorted.retrieve(1) == fst_b
        assert sorted.retrieve(2) == scnd_b
    
    def test_many_inserts_and_deletes(self):
        for i in range(1000):
            lst = avl.AVLTreeList()
            arr = []
            for j in range(15):
                l = lst.length()
                index = 0 if l <= 0 else random.randint(0, l)
                value = random.choice(self.LETTERS)
                lst.insert(index, value)
                arr.insert(index, value)
            
            assert lst.listToArray() == arr, lst.listToArray()

            # measure deletions
            for j in range(15):
                l = lst.length()-1
                index = 0 if l <= 0 else random.randint(0, l)
                lst.delete(index)
                assert lst.size == lst.root.size
            
            assert lst.root.value == None, lst.root

    def test_sort_with_none(self):
        arr = list("1362146015234")
        srted = [None,None] + sorted(arr)

        arr.insert(5, None)
        arr.insert(7,None)
        lst = avl.AVLTreeList.arrayToList(arr)
        lst = lst.sort()
        lst_arr = lst.listToArray()
        assert lst_arr == srted, f"{lst_arr}\n{srted}"

if __name__ == "__main__":
    unittest.main()