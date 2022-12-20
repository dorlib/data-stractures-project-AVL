class I_strict_attributes(object):
    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.__dict__[name]
        else:
            raise AttributeError(f"list has no attribute {name}")
    
    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            self.__dict__[name] = value
        else:
            raise AttributeError(f"list has no attribute {name}")

class I_list(I_strict_attributes):
    def __init__(self, iterable = None):
        self.__dict__["len"] = 0
        if iterable != None:
            for i, item in enumerate(iterable):
                self.insert(i, item)

    def __getitem__(self, index):
        return self.retrieve(index)
    
    def __len__(self):
        return self.len

    def __iter__(self):
        for i in range(len(self)):
            yield self.retrieve(i)

    def length(self):
        return len(self)

    def retrieve(self, index):
        if index >= self.len or index < 0:
            raise IndexError(f"cannot retrieve from {index} because list has length {self.len}")

    def insert(self, index, value):
        if index > self.len or index < 0:
            raise IndexError(f"cannot insert at {index} because list has length {len(self)}")
    
    def delete(self, index):
        if index >= self.len or index < 0:
            raise IndexError(f"cannot delete at {index} because list has length {len(self)}")


class dynamic_array(I_list):
    def __init__(self, iterable = None):
        self.__dict__["maxlen"] = 10
        self.__dict__["array"] = [None for i in range(10)]
        super().__init__(iterable)
    
    def __repr__(self):
        return f"array: {list(self)}"

    def insert(self, index, value):
        super().insert(index, value)
        if self.len == self.maxlen:
            self.enlarge_array()
        self.array[index] = value
        self.len += 1
        

    def enlarge_array(self):
        self.maxlen += self.maxlen
        old = self.array
        new = [old[i] if i<len(old) else None for i in range(self.maxlen)]
        self.array = new

    def delete(self, index):
        super().delete(index)
        if index == self.len - 1:
            self.len -= 1
            return
        for i in range(index, self.len - 1):
            self.array[i] = self.array[i+1]
        self.len -= 1
    
    def retrieve(self, index):
        super().retrieve(index)
        return self.array[index]


class linked_list(I_list):
    class l_node(I_strict_attributes):
        def __init__(self, value, next = None) -> None:
            self.__dict__["value"] = value
            self.__dict__["next"] = next

        def __getattribute__(self, name):
            if name == "isVirtual":
                return self.is_virtual()
            elif name == "isReal":
                return not self.is_virtual()
            elif name == "isEmpty":
                return self.is_empty()
            else:
                return object.__getattribute__(self, name)
        def __repr__(self) -> str:
            return f"({self.value})"
        @staticmethod
        def virtual():
            return linked_list.l_node(None)
        
        def is_virtual(self):
            return self.value == None and self.next == None
        
        def is_empty(self):
            return self.value == None and self.next != None

        def delete(self):
            self.value = None
        
        def delete_next(self):
            node_to_delete = self.next
            self.next = node_to_delete.next

        def insert_after(self, value):
            old_next = self.next
            self.next = linked_list.l_node(value, next=old_next)

    def __init__(self, iterable = None) -> None:
        self.__dict__["start"] = linked_list.l_node.virtual()
        self.__dict__["end"] = self.start
        self.end.next = linked_list.l_node.virtual()
        super().__init__(iterable)

    def __repr__(self):
        st = ""
        for i in self:
            st += f"{i}->"
        return st[:-2]

    def insert(self, index, value):
        super().insert(index, value)
        if index == 0:
            if self.start.isEmpty:
                self.start.value = value
            else:
                self.start = linked_list.l_node(value, self.start)
        elif index == len(self):
            self.end.insert_after(value)
            self.end = self.end.next
        else:
            one_before = self.retrieve(index - 1)
            one_before.insert_after(value)
        self.len += 1

    def retrieve(self, index): 
        super().retrieve(index)
        node = self.start
        i = 0
        while i < index and node.isReal:
            if node.next.isEmpty:
                node.delete_next()
                continue
            node = node.next
            i += 1
        return node
    
    def delete(self, index):
        super().delete(index)
        if index == 0:
            self.start = self.start.next
            self.len -= 1
            return
        else:
            node_before = self.retrieve(index - 1)
            node_before.delete_next()
            self.len -= 1

    def __iter__(self):
        node = self.start
        while node.isReal:
            if node.isEmpty:
                node = node.next
                continue
            yield node
            node = node.next