# data-stractures-project-AVL

This is the first programming project in data structures course. </br>
In this project we will implement an ADT of a List while using an AVL tree. </br>

- [AVL Node class](#AVL-Node-Class)
    - [functions & time complexity table](#AVLNode-functions-&-time-complexity)
- [AVL Tree List class](#AVL-Tree-List-Class)
    - [functions & time complexity table](#AVLTreeList-functions-&-time-complexity)
- [Contributing](#Contributing)    
- [Maintainers](#maintainers)
## AVL Node Class


### AVLNode functions & time complexity

| Function     | Description                                                                             | Time Complexity | 
|:-------------|:----------------------------------------------------------------------------------------|:----------------|
| getHeight()  | Returns the height field of self.                                                       | O(1)            |
| getValue()   | Returns the value field of self.                                                        | O(1)            |
| getLeft()    | Returns the left child of self. if self is a leaf, his children will be virtual nodes.  | O(1)            |
| getRight()   | Returns the right child of self. if self is a leaf, his children will be virtual nodes. | O(1)            |
| getParent()  | Returns the parent of self. if self is the root, returns None.                          | O(1)            |
| setHeight()  | Sets the height of self.                                                                | O(1)            |
| setValue()   | Sets the value of self.                                                                 | O(1)            |
| setLeft()    | Sets the left child self node without rebalance.                                        | O(1)            | 
| setRight()   | Sets the right child self node without rebalance.                                       | O(1)            |
| setParent()  | Sets the parent of self and update the parent node.                                     | O(1)            |
| isRealNode() | Returns whether self is not a virtual node.                                             | O(1)            |

## AVL Tree List Class

AVL Tree List include the implementation of the list's functionality and the methods that the user will use.
Behind the scenes the list is an AVL Tree which is not a BST but a ranked tree.
The tree itself is implemented using the function in the AVLNode class.


### AVLTreeList functions & time complexity

| Function      | Description                                                                                                                                | Time Complexity | 
|:--------------|:-------------------------------------------------------------------------------------------------------------------------------------------|:----------------|
| empty()       | Returns true if and only if the list is empty.                                                                                             | O(1)            |
| retrieve(i)   | Returns the value of the i'th element in the list if exist, if not, returns None.                                                          | O(log(n))       |
| insert(i,s)   | Inserts the value s in index i if there are at least i element in the list and Return num of rotations made while fixing the AVL.          | O(log(n))       |
| delete(i)     | Removes the i'th element from the list if exists and Return num of rotations made while fixing the AVL or -1 if the element doesn't exist. | O(log(n))       |
| first()       | Returns the value of the first element in the list and or None if it's empty.                                                              | O(1)            |
| last()        | Returns the value of the last element in the list and or None if it's empty.                                                               | O(1)            |
| listToArray() | Returns an array with of the list's elements in the index order, or empyy array if the list is empty.                                      | O(n)            |
| length()      | Returns the number of elements in the list.                                                                                                | O(1)            | 
| permutation() | Returns new list with the same elements in random order.                                                                                   | O(n*log(n))     |
| sort()        | Returns new list with the same elements in sorted order.                                                                                   | O(n*log(n))     |
| concat(lst)   | Concats lst to the end of the list and returns the absulute value of the height difference between the list and lst.                       | O(log(n))       |
| search(vals)  | Returns the first index of the element with the given value in the list or -1 if it doesnt exist.                                          | O(n)            |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

### How To Contribute

1. Fork the repository to your own Github account.
2. Clone the project to your machine.
3. Create a branch locally with a succinct but descriptive name.
4. Commit changes to the branch.
5. Following any formatting and testing guidelines specific to this repo.
6. Push changes to your fork.
7. Open a Pull Request in my repository.

## Creators / Maintainers

- Dor Liberman ([dorlib](https://github.com/dorlib))
- Afik Ben Shimol ([AfikBenShimol](https://github.com/AfikBenShimol))

If you have any questions or feedback, I would be glad if you will contact me via mail.

<p align="left">
  <a href="dorlibrm@gmail.com"> 
    <img alt="Connect via Email" src="https://img.shields.io/badge/Gmail-c14438?style=flat&logo=Gmail&logoColor=white" />
  </a>
</p>

This project was created for educational purposes, for personal and open-source use.

If you like my content or find my code useful, give it a :star:

