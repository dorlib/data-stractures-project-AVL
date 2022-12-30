import avl_template_new
from avl_template_new import AVLTreeList as avl_list
import unittest

class AVLTreeList(avl_list):
    def append(self, val):
        return self.insert(self.length(), val)

"""
IN ORDER TO USE THE TEST TOU NEED TO DO THE FOLLOWING:
1. IMPLEMENT APPEND METHOD IN AVLTreeList THIS WAY:
def append(self, val):
        self.insert(self.length(), val)
2. YOU NEED TO HAVE FIELDS POINTING TO FIRST AND LAST NODE IN THE TREE REPRESENTING THE LIST. 
NAME THEM firstNode and lastNode OR ALTERNATIVELY CHANGE THE TEST ITSELF TO FIT WITH THE NAMES
OF THESE FIELDS AT YOUR IMPLEMENTATION. 
3. YOU NEED TO HAVE A METHOD THAT RETURNS THE TREE HEIGHT AND NAME IT 'getTreeHeight'
4. THERE ARE TESTS THAT ASSERTS THAT THE FATHER OF THE ROOT IS NONE. IF YOU IMPLEMENTED IT 
DIFFERENTLY THEN YOU WILL NEED TO FIT THOSE TESTS OR COMMENT THEM.
"""


class testAVLList(unittest.TestCase):

    emptyList = AVLTreeList()
    twentyTree = AVLTreeList()
    twentylist = []

    for i in range(20):
        twentylist.append(i)
        twentyTree.append(i)

    def in_order(self, tree, node, func):
        if node is not None:
            if node.isRealNode():
                self.in_order(tree, node.getLeft(), func)
                func(node, tree)
                self.in_order(tree, node.getRight(), func)

    def compare_with_list_by_in_order(self, tree, lst):
        def rec(node, cnt, lst):
            if node.isRealNode():
                rec(node.getLeft(), cnt, lst)
                self.assertEqual(node.getValue(), lst[cnt[0]])
                cnt[0] += 1
                rec(node.getRight(), cnt, lst)

        cnt = [0]
        if not tree.empty():
            rec(tree.getRoot(), cnt, lst)
        else:
            self.assertEqual(len(lst), 0)

    def compare_with_list_by_retrieve(self, tree, lst):
        for i in range(max(len(lst), tree.length())):
            self.assertEqual(tree.retrieve(i), lst[i])

    def test_empty(self):
        self.assertTrue(self.emptyList.empty())
        self.assertFalse(self.twentyTree.empty())

    def test_retrieve_basic(self):
        self.assertIsNone(self.emptyList.retrieve(0))
        self.assertIsNone(self.emptyList.retrieve(59))
        self.assertIsNone(self.twentyTree.retrieve(30))
        self.assertIsNone(self.twentyTree.retrieve(-1))
        for i in range(20):
            self.assertEqual(self.twentylist[i], self.twentyTree.retrieve(i))
        T = AVLTreeList()
        T.append('a')
        self.assertEqual(T.retrieve(0), "a")

    def check_first(self, tree, lst):
        if not tree.empty():
            self.assertEqual(tree.first(), lst[0])
        else:
            self.assertEqual(len(lst), 0)
            self.assertIsNone(tree.first())

    def check_last(self, tree, lst):
        if not tree.empty():
            self.assertEqual(tree.last(), lst[-1])
        else:
            self.assertEqual(len(lst), 0)
            self.assertIsNone(tree.last())

    ###TESTING INSERTION###

    def test_insertBasic(self):
        T1 = AVLTreeList()
        T1.insert(0, 1)
        self.assertEqual(T1.getRoot().getValue(), 1)

    def test_insert_at_start(self):
        # inserts at start
        T2 = AVLTreeList()
        L2 = []

        for i in range(50):
            T2.insert(0, str(i))
            L2.insert(0, str(i))
            self.compare_with_list_by_in_order(T2, L2)
            self.compare_with_list_by_retrieve(T2, L2)

        self.check_first(T2, L2)
        self.check_last(T2, L2)

    def test_insert_at_end_small(self):
        T1 = AVLTreeList()
        L1 = []

        for i in range(3):
            T1.append(i)
            L1.append(i)
            self.compare_with_list_by_in_order(T1, L1)
            self.compare_with_list_by_retrieve(T1, L1)

        for j in range(10, 20):
            T3 = AVLTreeList()
            L3 = []
            for i in range(j):
                T3.insert(T3.length(), i)
                L3.insert(len(L3), i)
                self.compare_with_list_by_retrieve(T3, L3)
                self.compare_with_list_by_in_order(T3, L3)

        self.check_first(T3, L3)
        self.check_last(T3, L3)
        self.check_first(T1, L1)
        self.check_last(T1, L1)

    def test_insert_at_end_big(self):
        T3 = AVLTreeList()
        L3 = []
        for i in range(100):
            T3.insert(T3.length(), i)
            L3.insert(len(L3), i)
        self.compare_with_list_by_retrieve(T3, L3)
        self.compare_with_list_by_in_order(T3, L3)
        self.check_first(T3, L3)
        self.check_last(T3, L3)

    def test_insert_at_the_middle_small(self):
        for j in range(10, 20):
            T = AVLTreeList()
            L = []

            for i in range(j):
                T.insert(i//2, i)
                L.insert(i//2, i)
                self.compare_with_list_by_retrieve(T, L)
                self.compare_with_list_by_in_order(T, L)
        self.check_first(T, L)
        self.check_last(T, L)

    def test_insert_at_the_middle_big(self):
        T4 = AVLTreeList()
        L4 = []

        for i in range(100):
            T4.insert(i//2, i)
            L4.insert(i//2, i)
            self.compare_with_list_by_retrieve(T4, L4)
            self.compare_with_list_by_in_order(T4, L4)
            self.check_first(T4, L4)
            self.check_last(T4, L4)

    def test_insert_alternately(self):
        T5 = AVLTreeList()
        L5 = []

        for i in range(100):
            if i % 5 == 0:
                T5.insert(0, i)
                L5.insert(0, i)
            elif i % 5 == 1:
                T5.insert(len(L5), i)
                L5.insert(len(L5), i)
            elif i % 5 == 2:
                T5.insert(i//2, i)
                L5.insert(i//2, i)
            elif i % 5 == 3:
                T5.insert(i//3, i)
                L5.insert(i//3, i)
            else:
                T5.insert(i//7, i)
                L5.insert(i//7, i)
            if i % 10 == 0:
                self.compare_with_list_by_retrieve(T5, L5)
                self.compare_with_list_by_in_order(T5, L5)
                self.check_first(T5, L5)
                self.check_last(T5, L5)

    ### TESTING DELETION ### (assuming insertion works perfectly)#
    def test_deleting_not_existing(self):
        self.assertEqual(self.emptyList.delete(0), -1)
        self.assertEqual(self.twentyTree.delete(-1), -1)
        self.assertEqual(self.twentyTree.delete(30), -1)

    def test_delete_list_with_only_one_element(self):
        T = AVLTreeList()
        T.insert(0, 1)
        T.delete(0)
        self.assertIsNone(T.getRoot())
        self.assertIsNone(T.first())
        self.assertIsNone(T.last())
        self.assertIsNone(T.first())
        self.assertIsNone(T.last())

    def test_delete_from_list_with_two_elements(self):
        T1 = AVLTreeList()
        for i in range(2):
            T1.append(i)
        T1.delete(0)

        self.assertEqual(T1.getRoot().getValue(), 1)
        T1.delete(0)
        self.assertIsNone(T1.getRoot())

        T1 = AVLTreeList()
        for i in range(2):
            T1.append(i)
        T1.delete(1)
        self.assertEqual(T1.getRoot().getValue(), 0)
        T1.delete(0)
        self.assertIsNone(T1.getRoot())

        T1 = AVLTreeList()
        for i in range(2):
            T1.append(0)

        T1.delete(0)
        self.assertEqual(T1.getRoot().getValue(), 0)
        T1.delete(0)
        self.assertIsNone(T1.getRoot())

    def test_delete_from_start_small(self):
        for j in range(10, 20):
            T = AVLTreeList()
            L = []
            for i in range(j):
                T.append(i)
                L.append(i)

            while not T.empty():
                self.compare_with_list_by_in_order(T, L)
                self.compare_with_list_by_retrieve(T, L)
                self.check_first(T, L)
                self.check_last(T, L)
                T.delete(0)
                L.pop(0)

        self.assertEqual(len(L), 0)

    def test_delete_from_start_big(self):
        T = AVLTreeList()
        L = []
        for i in range(100):
            T.append(i)
            L.append(i)

        while not T.empty():
            self.compare_with_list_by_in_order(T, L)
            self.compare_with_list_by_retrieve(T, L)
            self.check_first(T, L)
            self.check_last(T, L)
            T.delete(0)
            L.pop(0)

        self.assertEqual(len(L), 0)

    def test_delete_from_end_small(self):
        for j in range(10, 20):
            T = AVLTreeList()
            L = []
            for i in range(j):
                T.append(i)
                L.append(i)

            while not T.empty():
                self.compare_with_list_by_in_order(T, L)
                self.compare_with_list_by_retrieve(T, L)
                self.check_first(T, L)
                self.check_last(T, L)
                T.delete(T.length()-1)
                L.pop(len(L)-1)

            self.assertEqual(len(L), 0)

    def test_delete_from_end_big(self):
        T = AVLTreeList()
        L = []
        for i in range(100):
            T.append(i)
            L.append(i)

        while not T.empty():
            self.compare_with_list_by_in_order(T, L)
            self.compare_with_list_by_retrieve(T, L)
            self.check_first(T, L)
            self.check_last(T, L)
            T.delete(T.length()-1)
            L.pop(len(L)-1)

        self.assertEqual(len(L), 0)

    def test_delete_from_middle_small(self):
        for j in range(10, 20):
            T = AVLTreeList()
            L = []
            for i in range(j):
                T.append(i)
                L.append(i)

            while not T.empty():
                self.compare_with_list_by_in_order(T, L)
                self.compare_with_list_by_retrieve(T, L)
                self.check_first(T, L)
                self.check_last(T, L)
                T.delete(T.length()//2)
                L.pop(len(L)//2)

            self.assertEqual(len(L), 0)

    def test_delete_from_middle_big(self):
        T = AVLTreeList()
        L = []

        for i in range(100):
            T.append(i)
            L.append(i)

        while not T.empty():
            self.compare_with_list_by_in_order(T, L)
            self.compare_with_list_by_retrieve(T, L)
            self.check_first(T, L)
            self.check_last(T, L)
            T.delete(T.length()//2)
            L.pop(len(L)//2)

        self.assertEqual(len(L), 0)

    def test_delete_altenatly(self):
        T = AVLTreeList()
        L = []
        for i in range(100):
            T.append(i)
            L.append(i)
        cnt = 0
        while not T.empty():
            self.compare_with_list_by_in_order(T, L)
            self.compare_with_list_by_retrieve(T, L)
            self.check_first(T, L)
            self.check_last(T, L)
            if cnt % 4 == 0:
                T.delete(T.length()//2)
                L.pop(len(L)//2)
            elif cnt % 4 == 1:
                T.delete(0)
                L.pop(0)
            elif cnt % 4 == 2:
                T.delete(T.length()-1)
                L.pop(len(L)-1)
            else:
                T.delete(T.length()//4)
                L.pop(len(L)//4)
            cnt += 1

        self.assertEqual(len(L), 0)

    ### TESTING INSERTION AND DELETION TOGETHER###

    def test_delete_and_insert_equal_number_of_times_small(self):
        cnt = 1
        T = AVLTreeList()
        for i in range(10):
            T.append(i)

        for i in range(100):
            if cnt % 2 == 0:
                T.insert(cnt % T.length(), i+10)
            else:
                T.delete(cnt % T.length())
            cnt += 17

    def test_delete_and_insert_equal_number_of_times_big(self):
        cnt = 1
        T = AVLTreeList()
        for i in range(100):
            T.append(i)

        for i in range(1000):
            if cnt % 2 == 0:
                T.insert(cnt % T.length(), i+10)
            else:
                T.delete(cnt % T.length())
            cnt += 17

    def test_delete_and_insert_with_more_insertions_small(self):
        T = AVLTreeList()
        T.append(40)
        for i in range(30):
            if (i % 3 != 2):
                T.insert((i*17) % T.length(), i)
            else:
                T.delete((i*17) % T.length())

    def test_delete_and_insert_with_more_insertions_big(self):
        T = AVLTreeList()
        T.append(40)
        for i in range(150):
            if (i % 3 != 2):
                T.insert((i*17) % T.length(), i)
            else:
                T.delete((i*17) % T.length())

    def test_delete_and_insert_altenatly_small(self):
        T = AVLTreeList()
        L = []

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
                L.insert(len(L)//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
                L.insert(0, i)
            else:
                T.delete(T.length()//2)
                L.pop(len(L)//2)
            self.compare_with_list_by_in_order(T, L)
            self.compare_with_list_by_retrieve(T, L)
            self.check_first(T, L)
            self.check_last(T, L)

    ### TESTING FAMILTY ### (testing that node == node.getchild.gerparent)#

    def check_family(self, node, tree):
        self.assertEqual(node, node.getLeft().getParent())
        self.assertEqual(node, node.getRight().getParent())

    def test_family_basic(self):
        self.in_order(self.twentyTree, self.twentyTree.getRoot(),
                      self.check_family)

        self.assertIsNone(self.twentyTree.getRoot().getParent())

    def test_family_after_insertion_at_start(self):
        T2 = AVLTreeList()

        for i in range(50):
            T2.insert(0, i)
            self.in_order(T2, T2.getRoot(), self.check_family)

    def test_family_after_deletion_from_start(self):
        T = AVLTreeList()
        for i in range(50):
            T.insert(0, i)

        for i in range(49):
            T.delete(0)
            self.in_order(T, T.getRoot(), self.check_family)

    def test_family_after_insertion_at_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)
            self.in_order(T3, T3.getRoot(), self.check_family)

    def test_family_after_deletion_from_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)

        for i in range(49):
            T3.delete(T3.length()-1)
            self.in_order(T3, T3.getRoot(), self.check_family)

    def test_family_after_insertion_at_middle(self):
        T4 = AVLTreeList()

        for i in range(50):
            T4.insert(i//2, i)
            self.in_order(T4, T4.getRoot(), self.check_family)

    def test_family_after_deletion_from_middle(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(0, i)

        for i in range(49):
            if i//2 < T3.length():
                T3.delete(i//2)
                self.in_order(T3, T3.getRoot(), self.check_family)

    def test_family_after_insertion_alternatly(self):
        T5 = AVLTreeList()

        for i in range(200):
            if i % 5 == 0:
                T5.insert(0, i)
            elif i % 5 == 1:
                T5.insert(T5.length(), i)
            elif i % 5 == 2:
                T5.insert(i//2, i)
            elif i % 5 == 3:
                T5.insert(i//3, i)
            else:
                T5.insert(i//7, i)
            self.in_order(T5, T5.getRoot(), self.check_family)

    def test_family_after_deletion_alternatly(self):
        T = AVLTreeList()

        for i in range(100):
            T.insert(0, i)

        for i in range(99):
            if i % 5 == 0:
                T.delete(0)
            elif i % 5 == 1:
                T.delete(T.length()-1)
            elif i % 5 == 2:
                T.delete((T.length()-1)//2)
            elif i % 5 == 3:
                T.delete((T.length()-1)//3)
            else:
                T.delete((T.length()-1)//7)
            self.in_order(T, T.getRoot(), self.check_family)

    def test_family_after_deleting_and_inserting_small(self):
        T = AVLTreeList()

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_family)

    def test_family_after_deleting_and_inserting_big(self):
        T = AVLTreeList()

        for i in range(500):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_family)

    ###TESTING SIZE###

    def check_size(self, node, tree):
        self.assertEqual(node.getSize(), node.getLeft(
        ).getSize() + node.getRight().getSize() + 1)

    def test_size_after_insertion_at_start(self):
        T2 = AVLTreeList()

        for i in range(50):
            T2.insert(0, i)
            self.in_order(T2, T2.getRoot(), self.check_size)

    def test_size_after_deletion_from_start(self):
        T = AVLTreeList()
        for i in range(50):
            T.insert(0, i)

        for i in range(49):
            T.delete(0)
            self.in_order(T, T.getRoot(), self.check_size)

    def test_size_after_insertion_at_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)
            self.in_order(T3, T3.getRoot(), self.check_size)

    def test_size_after_deletion_from_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)

        for i in range(49):
            T3.delete(T3.length()-1)
            self.in_order(T3, T3.getRoot(), self.check_size)

    def test_size_after_insertion_at_middle(self):
        T4 = AVLTreeList()

        for i in range(50):
            T4.insert(i//2, i)
            self.in_order(T4, T4.getRoot(), self.check_size)

    def test_size_after_deletion_from_middle(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(0, i)

        for i in range(49):
            if i//2 < T3.length():
                T3.delete(i//2)
                self.in_order(T3, T3.getRoot(), self.check_size)

    def test_size_after_insertion_alternatly(self):
        T5 = AVLTreeList()

        for i in range(200):
            if i % 5 == 0:
                T5.insert(0, i)
            elif i % 5 == 1:
                T5.insert(T5.length(), i)
            elif i % 5 == 2:
                T5.insert(i//2, i)
            elif i % 5 == 3:
                T5.insert(i//3, i)
            else:
                T5.insert(i//7, i)
            self.in_order(T5, T5.getRoot(), self.check_size)

    def test_size_after_deletion_alternatly(self):
        T = AVLTreeList()

        for i in range(100):
            T.insert(0, i)

        for i in range(99):
            if i % 5 == 0:
                T.delete(0)
            elif i % 5 == 1:
                T.delete(T.length()-1)
            elif i % 5 == 2:
                T.delete((T.length()-1)//2)
            elif i % 5 == 3:
                T.delete((T.length()-1)//3)
            else:
                T.delete((T.length()-1)//7)
            self.in_order(T, T.getRoot(), self.check_size)

    def test_size_after_deleting_and_inserting_small(self):
        T = AVLTreeList()

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_size)

    def test_size_after_deleting_and_inserting_big(self):
        T = AVLTreeList()

        for i in range(500):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_size)

        ###TESTING HEIGHT###

    def check_height(self, node, tree):
        self.assertEqual(node.getHeight(), max(node.getLeft(
        ).getHeight(), node.getRight().getHeight()) + 1)

    def test_height_after_insertion_at_start(self):
        T2 = AVLTreeList()

        for i in range(50):
            T2.insert(0, i)
            self.in_order(T2, T2.getRoot(), self.check_height)

    def test_height_after_deletion_from_start(self):
        T = AVLTreeList()
        for i in range(50):
            T.insert(0, i)

        for i in range(49):
            T.delete(0)
            self.in_order(T, T.getRoot(), self.check_height)

    def test_height_after_insertion_at_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)
            self.in_order(T3, T3.getRoot(), self.check_height)

    def test_height_after_deletion_from_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)

        for i in range(49):
            T3.delete(T3.length()-1)
            self.in_order(T3, T3.getRoot(), self.check_height)

    def test_height_after_insertion_at_middle(self):
        T4 = AVLTreeList()

        for i in range(50):
            T4.insert(i//2, i)
            self.in_order(T4, T4.getRoot(), self.check_height)

    def test_height_after_deletion_from_middle(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(0, i)

        for i in range(49):
            if i//2 < T3.length():
                T3.delete(i//2)
                self.in_order(T3, T3.getRoot(), self.check_height)

    def test_height_after_insertion_alternatly(self):
        T5 = AVLTreeList()

        for i in range(200):
            if i % 5 == 0:
                T5.insert(0, i)
            elif i % 5 == 1:
                T5.insert(T5.length(), i)
            elif i % 5 == 2:
                T5.insert(i//2, i)
            elif i % 5 == 3:
                T5.insert(i//3, i)
            else:
                T5.insert(i//7, i)
            self.in_order(T5, T5.getRoot(), self.check_height)

    def test_height_after_deletion_alternatly(self):
        T = AVLTreeList()

        for i in range(100):
            T.insert(0, i)

        for i in range(99):
            if i % 5 == 0:
                T.delete(0)
            elif i % 5 == 1:
                T.delete(T.length()-1)
            elif i % 5 == 2:
                T.delete((T.length()-1)//2)
            elif i % 5 == 3:
                T.delete((T.length()-1)//3)
            else:
                T.delete((T.length()-1)//7)
            self.in_order(T, T.getRoot(), self.check_height)

    def test_height_after_deleting_and_inserting_small(self):
        T = AVLTreeList()

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_height)

    def test_height_after_deleting_and_inserting_big(self):
        T = AVLTreeList()

        for i in range(500):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_height)

    ### TESTING BALACNE FACTOR ###

    def check_BF(self, node, tree):
        self.assertTrue(abs(node.getLeft().getHeight() -
                            node.getRight().getHeight()) < 2)

    def test_BF_after_insertion_at_start(self):
        T2 = AVLTreeList()

        for i in range(50):
            T2.insert(0, i)
            self.in_order(T2, T2.getRoot(), self.check_BF)

    def test_BF_after_deletion_from_start(self):
        T = AVLTreeList()
        for i in range(50):
            T.insert(0, i)

        for i in range(49):
            T.delete(0)
            self.in_order(T, T.getRoot(), self.check_BF)

    def test_BF_after_insertion_at_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)
            self.in_order(T3, T3.getRoot(), self.check_BF)

    def test_BF_after_deletion_from_end(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(T3.length(), i)

        for i in range(49):
            T3.delete(T3.length()-1)
            self.in_order(T3, T3.getRoot(), self.check_BF)

    def test_BF_after_insertion_at_middle(self):
        T4 = AVLTreeList()

        for i in range(50):
            T4.insert(i//2, i)
            self.in_order(T4, T4.getRoot(), self.check_BF)

    def test_BF_after_deletion_from_middle(self):
        T3 = AVLTreeList()

        for i in range(50):
            T3.insert(0, i)

        for i in range(49):
            if i//2 < T3.length():
                T3.delete(i//2)
                self.in_order(T3, T3.getRoot(), self.check_BF)

    def test_BF_after_insertion_alternatly(self):
        T5 = AVLTreeList()

        for i in range(200):
            if i % 5 == 0:
                T5.insert(0, i)
            elif i % 5 == 1:
                T5.insert(T5.length(), i)
            elif i % 5 == 2:
                T5.insert(i//2, i)
            elif i % 5 == 3:
                T5.insert(i//3, i)
            else:
                T5.insert(i//7, i)
            self.in_order(T5, T5.getRoot(), self.check_BF)

    def test_BF_after_deletion_alternatly(self):
        T = AVLTreeList()

        for i in range(100):
            T.insert(0, i)

        for i in range(99):
            if i % 5 == 0:
                T.delete(0)
            elif i % 5 == 1:
                T.delete(T.length()-1)
            elif i % 5 == 2:
                T.delete((T.length()-1)//2)
            elif i % 5 == 3:
                T.delete((T.length()-1)//3)
            else:
                T.delete((T.length()-1)//7)
            self.in_order(T, T.getRoot(), self.check_BF)

    def test_BF_after_deleting_and_inserting_small(self):
        T = AVLTreeList()

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_BF)

    def test_BF_after_deleting_and_inserting_big(self):
        T = AVLTreeList()

        for i in range(500):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
            else:
                T.delete(T.length()//2)
            self.in_order(T, T.getRoot(), self.check_BF)

    ###TESTING SEARCH###

    def test_search_basic(self):
        self.assertEqual(-1, self.emptyList.search(None))
        self.assertEqual(-1, self.emptyList.search(20))
        for i in range(20):
            self.assertEqual(i, self.twentyTree.search(i))
        self.assertEqual(-1, self.twentyTree.search(21))

    def test_search_after_insertion_at_start(self):
        T2 = AVLTreeList()
        L2 = []

        for i in range(50):
            T2.insert(0, i)
            L2.insert(0, i)
            for j in range(len(L2)):
                self.assertEqual(T2.search(L2[j]), j)
            self.assertEqual(-1, T2.search(-20))

    def test_search_after_deletion_from_start(self):
        T = AVLTreeList()
        L = []
        for i in range(50):
            T.append(i)
            L.append(i)

        for i in range(49):
            T.delete(0)
            L.pop(0)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_insertion_at_end(self):
        T = AVLTreeList()
        L = []

        for i in range(50):
            T.append(i)
            L.append(i)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_deletion_from_end(self):
        T = AVLTreeList()
        L = []

        for i in range(50):
            T.append(i)
            L.append(i)

        for i in range(49):
            T.delete(T.length()-1)
            L.pop(len(L)-1)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_insertion_at_middle(self):
        T = AVLTreeList()
        L = []

        for i in range(50):
            T.insert(i//2, i)
            L.insert(i//2, i)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_deletion_from_middle(self):
        T = AVLTreeList()
        L = []

        for i in range(50):
            T.insert(0, i)
            L.insert(0, i)

        for i in range(49):
            T.delete(T.length()//2)
            L.pop(len(L)//2)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_insertion_alternatly(self):
        T = AVLTreeList()
        L = []

        for i in range(200):
            if i % 5 == 0:
                T.insert(0, i)
                L.insert(0, i)
            elif i % 5 == 1:
                T.append(i)
                L.append(i)
            elif i % 5 == 2:
                T.insert(i//2, i)
                L.insert(i//2, i)
            elif i % 5 == 3:
                T.insert(i//3, i)
                L.insert(i//3, i)
            else:
                T.insert(i//7, i)
                L.insert(i//7, i)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_height_search_deletion_alternatly(self):
        T = AVLTreeList()
        L = []

        for i in range(100):
            T.insert(0, i)
            L.insert(0, i)

        for i in range(99):
            if i % 5 == 0:
                T.delete(0)
                L.pop(0)
            elif i % 5 == 1:
                T.delete(T.length()-1)
                L.pop(len(L)-1)
            elif i % 5 == 2:
                T.delete((T.length()-1)//2)
                L.pop((len(L)-1)//2)
            elif i % 5 == 3:
                T.delete((T.length()-1)//3)
                L.pop((len(L)-1)//3)
            else:
                T.delete((T.length()-1)//7)
                L.pop((len(L)-1)//7)

            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_deleting_and_inserting_small(self):
        T = AVLTreeList()
        L = []

        for i in range(20):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
                L.insert(len(L)//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
                L.insert(0, i)
            else:
                T.delete(T.length()//2)
                L.pop(len(L)//2)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    def test_search_after_deleting_and_inserting_big(self):
        T = AVLTreeList()
        L = []

        for i in range(500):
            if i % 3 == 0:
                T.insert(T.length()//2, i)
                L.insert(len(L)//2, i)
            elif i % 3 == 1:
                T.insert(0, i)
                L.insert(0, i)
            else:
                T.delete(T.length()//2)
                L.pop(len(L)//2)
            for j in range(len(L)):
                self.assertEqual(T.search(L[j]), j)
            self.assertEqual(-1, T.search(-20))

    ### TESTING CONCAT AND LISTASARRAY ###
    TR1 = AVLTreeList()
    LR1 = list()
    TR2 = AVLTreeList()
    LR2 = list()

    for i in range(20):
        TR1.append(i)
        TR2.append(i+10)
        LR1.append(i)
        LR2.append(i+10)

    # def test_compare_treelist_and_list(self):
        # self.assertEqual (self.TR1.listToArray(),self.LR1)

    TR1.concat(TR2)
    LR3 = LR1 + LR2

    def test_compare_concatinated_treelists_and_list(self):
        self.compare_with_list_by_in_order(self.TR1, self.LR3)
        self.compare_with_list_by_retrieve(self.TR1, self.LR3)
        self.check_first(self.TR1, self.LR3)
        self.check_last(self.TR1, self.LR3)
        self.assertEqual(self.TR1.listToArray(), self.LR3)
        self.in_order(self.TR1, self.TR1.getRoot(), self.check_BF)
        self.in_order(self.TR1, self.TR1.getRoot(), self.check_height)
        self.in_order(self.TR1, self.TR1.getRoot(), self.check_size)
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        L1 = list()
        L2 = list()
        for i in range(10):
            T1.append(i)
            L1.append(i)
        for i in range(5):
            T2.append(i)
            L2.append(i)
        T1.concat(T2)
        L3 = L1+L2
        self.compare_with_list_by_in_order(T1, L3)
        self.compare_with_list_by_retrieve(T1, L3)
        self.check_first(T1, L3)
        self.check_last(T1, L3)
        self.assertEqual(T1.listToArray(), L3)
        self.in_order(T1, T1.getRoot(), self.check_BF)
        self.in_order(T1, T1.getRoot(), self.check_height)
        self.in_order(T1, T1.getRoot(), self.check_size)
        T3 = AVLTreeList()
        T4 = AVLTreeList()
        L3 = list()
        L4 = list()
        for i in range(10):
            T4.append(i)
            L4.append(i)
        for i in range(5):
            T3.append(i)
            L3.append(i)
        T3.concat(T4)
        L5 = L3+L4
        self.compare_with_list_by_in_order(T3, L5)
        self.compare_with_list_by_retrieve(T3, L5)
        self.check_first(T3, L5)
        self.check_last(T3, L5)
        self.assertEqual(T3.listToArray(), L5)
        self.in_order(T3, T3.getRoot(), self.check_BF)
        self.in_order(T3, T3.getRoot(), self.check_height)
        self.in_order(T3, T3.getRoot(), self.check_size)

    def test_compare_concatinated_treelists_and_list_small(self):
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        L1 = list()
        L2 = list()
        for i in range(3):
            T1.append(i)
            L1.append(i)
        for i in range(1):
            T2.append(i)
            L2.append(i)
        T1.concat(T2)
        L3 = L1+L2
        self.compare_with_list_by_in_order(T1, L3)
        self.compare_with_list_by_retrieve(T1, L3)
        self.check_first(T1, L3)
        self.check_last(T1, L3)
        self.assertEqual(T1.listToArray(), L3)
        self.in_order(T1, T1.getRoot(), self.check_BF)
        self.in_order(T1, T1.getRoot(), self.check_height)
        self.in_order(T1, T1.getRoot(), self.check_size)
        T3 = AVLTreeList()
        T4 = AVLTreeList()
        L3 = list()
        L4 = list()
        for i in range(3):
            T4.append(i)
            L4.append(i)
        for i in range(1):
            T3.append(i)
            L3.append(i)
        T3.concat(T4)
        L5 = L3+L4
        self.compare_with_list_by_in_order(T3, L5)
        self.compare_with_list_by_retrieve(T3, L5)
        self.check_first(T3, L5)
        self.check_last(T3, L5)
        self.assertEqual(T3.listToArray(), L5)
        self.in_order(T3, T3.getRoot(), self.check_BF)
        self.in_order(T3, T3.getRoot(), self.check_height)
        self.in_order(T3, T3.getRoot(), self.check_size)

    def test_concat_with_empty_list_as_self(self):
        empty = AVLTreeList()
        LR4 = [i for i in range(10)]
        TR4 = AVLTreeList()
        for i in range(10):
            TR4.append(i)
        empty.concat(TR4)
        self.assertEqual(empty.listToArray(), LR4)
        self.check_first(empty, LR4)
        self.check_last(empty, LR4)

    def test_concat_with_empty_list_as_lst(self):
        self.TR1.concat(self.emptyList)
        self.assertEqual(self.TR1.listToArray(), self.LR3)
        self.check_first(self.TR1, self.LR3)
        self.check_last(self.TR1, self.LR3)

    def test_concat_first(self):
        self.assertEqual(self.TR1.first(), self.LR3[0])

    def test_concat_last(self):
        self.assertEqual(self.TR1.last(), self.LR3[-1])

    def test_concat_height_difference_empty_lists(self):
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        self.assertEqual(T1.concat(T2), 0)

    def test_assert_height_difference_one_empty_list(self):
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        T3 = AVLTreeList()
        T4 = AVLTreeList()
        for i in range(3):
            T1.append(i)
            T2.append(i)

        # the height of an empty tree is -1.
        self.assertEqual(T1.concat(T3), 2)
        self.assertEqual(T4.concat(T2), 2)

    def test_assert_height_difference_non_empty_lists(self):
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        for i in range(3):
            T1.append(i)
        for i in range(1):
            T2.append(i)
        self.assertEqual(T1.concat(T2), 1)
        T3 = AVLTreeList()
        T4 = AVLTreeList()
        for i in range(3):
            T4.append(i)
        for i in range(1):
            T3.append(i)
        self.assertEqual(T3.concat(T4), 1)

    def test_assert_height_difference_non_empty_lists_big(self):
        T1 = AVLTreeList()
        T2 = AVLTreeList()
        for i in range(10):
            T1.append(i)
        for i in range(5):
            T2.append(i)
        self.assertEqual(abs(T1.getRoot().getHeight() -
                             T2.getRoot().getHeight()), T1.concat(T2))
        T3 = AVLTreeList()
        T4 = AVLTreeList()
        for i in range(10):
            T4.append(i)
        for i in range(5):
            T3.append(i)
        self.assertEqual(abs(T3.getRoot().getHeight() -
                             T4.getRoot().getHeight()), T3.concat(T4))

    ### TESTING SPLIT ###
    def check_root(self, tree):
        if not tree.empty():
            self.assertIsNone(tree.getRoot().getParent())

    def check_split(self, lst, res, i):
        self.assertEqual(lst[i], res[1])
        L1 = lst[:i]
        L2 = lst[i+1:]

        ##checks values##
        self.assertEqual(res[0].listToArray(), L1)
        self.compare_with_list_by_retrieve(res[0], L1)
        self.compare_with_list_by_in_order(res[0], L1)
        self.assertEqual(res[2].listToArray(), L2)
        self.compare_with_list_by_retrieve(res[2], L2)
        self.compare_with_list_by_in_order(res[2], L2)

        ##checks fields##
        self.check_first(res[0], L1)
        self.check_last(res[0], L1)
        self.in_order(res[0], res[0].getRoot(), self.check_family)
        self.in_order(res[0], res[0].getRoot(), self.check_height)
        self.in_order(res[0], res[0].getRoot(), self.check_size)
        self.in_order(res[0], res[0].getRoot(), self.check_BF)
        self.check_root(res[0])

        self.check_first(res[2], L2)
        self.check_last(res[2], L2)
        self.in_order(res[2], res[2].getRoot(), self.check_family)
        self.in_order(res[2], res[2].getRoot(), self.check_height)
        self.in_order(res[2], res[2].getRoot(), self.check_size)
        self.in_order(res[2], res[2].getRoot(), self.check_BF)
        self.check_root(res[2])

    def test_num_of_balnce_ops(self):
        T = AVLTreeList()
        self.assertEqual(T.append(3), 0)
        self.assertEqual(T.insert(0, 1), 0)
        self.assertEqual(T.insert(1, 2), 2)

    # def test_successor_and_predeccessor(self):
    #     T = AVLTreeList()
    #     T.append(0)
    #     T.append(1)

    #     self.assertEqual(T.getSuccessorOf(T.getRoot()).getValue(), 1)
    #     self.assertEqual(T.getSuccessorOf(
    #         T.getRoot().getRight()), None)
    #     self.assertEqual(T.getPredecessorOf(
    #         T.getRoot().getRight()).getValue(), 0)


if __name__ == '__main__':
    unittest.main()
