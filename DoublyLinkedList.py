class Node:
    """
    Linked list element class.
    """
    def __init__(self, value=None, prev=None, next=None):
        self.val = value
        self.prev = prev
        self.next = next


class DLinkedList:
    """
    Linked list class, whose elements are an instance of the Node class.
    :param root: 1st element of Linked List
    :param end: last element of Linked List
    """
    def __init__(self, *values):
        self.root = None
        self.end = None
        self._length = 0
        for i in values:
            self.addAtTail(i)

    def _get(self, index):
        """
        Get the index-th node in the linked list.
        """
        if index >= len(self):
            raise IndexError
        if index == 0:
            return self.root
        if index == len(self) - 1:
            return self.end
        if index < 0:
            if abs(index) > len(self):
                raise IndexError
            index += len(self)
        temp = None
        if index <= len(self) // 2:
            temp = self.root
            for i in range(index):
                temp = temp.next
        else:
            temp = self.end
            for i in range(len(self) - index - 1):
                temp = temp.prev
        return temp

    def addAtHead(self, val, *values):
        """
        Add a node(s) of value(s) val(values) before the first element of the linked list.
        :param val: node value
        :param values: additional values
        :return:
        """
        for i in values[::-1]:
            self.addAtHead(i)
        if not self.root:
            self.root = Node(val)
            self.end = self.root
        else:
            node = Node(val, None, self.root)
            self.root.prev = node
            self.root = node
        self._length += 1

    def addAtTail(self, val, *values):
        """
        Append a node(s) of value(s) val(values) to the last element of the linked list.
        :param val: node value
        :param values: additional values
        :return:
        """
        if not self.end:
            self.addAtHead(val)
        else:
            self.end.next = Node(val, self.end)
            self.end = self.end.next
            self._length += 1
        for i in values:
            self.addAtTail(i)

    def addAtIndex(self, index, val, *values):
        """
        Add a node(s) of value(s) val(values) before the index-th node in the linked list. If index equals to the length
        of linked list, the node will be appended to the end of linked list.
        :param index: node index
        :param val: node value
        :param values: additional values
        :return:
        """
        if index == 0:
            self.addAtHead(val, *values)
        elif index == len(self):
            self.addAtTail(val, *values)
        elif 0 < index < len(self):
            temp = self._get(index - 1)
            node = Node(val, temp, temp.next)
            temp.next = node
            node.next.prev = node
            self._length += 1
        else:
            raise IndexError

    def deleteAtIndex(self, index):
        """
        Delete the index-th node in the linked list, if the index is valid.
        :param index: node index
        :return:
        """
        if 0 <= index < len(self):
            if len(self) == 1:
                self.root = None
                self.end = None
            elif index == 0:
                self.root = self.root.next
                self.root.prev = None
            elif index == len(self) - 1:
                self.end = self.end.prev
                self.end.next = None
            else:
                temp = self._get(index - 1)
                temp.next = temp.next.next
                temp.next.prev = temp
            self._length -= 1
        else:
            raise IndexError

    def popRoot(self):
        """
        Remove the first node in the linked list and return its value.
        :return value: 1st node value
        """
        if len(self) == 0:
            return None
        res = self.root.val
        self.deleteAtIndex(0)
        return res

    def popEnd(self):
        """
        Remove the last node in the linked list and return its value.
        :return value: last node value
        """
        if len(self) < 2:
            return self.popRoot()
        res = self.end.val
        self.deleteAtIndex(len(self) - 1)
        return res

    def __len__(self):
        return self._length

    def __iter__(self):
        for i in range(len(self)):
            yield (self._get(i)).val

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = 0 if not item.start else item.start
            stop = len(self) if not item.stop else item.stop
            step = 1 if not item.step else item.step
            if step < 0:
                start, stop = stop, start
                start -= 1
                stop -= 1
            return [(self._get(i)).val for i in range(start, stop, step)]
        return (self._get(item)).val

    def __setitem__(self, key, value):
        (self._get(key)).val = value

    def __reversed__(self):
        return DLinkedList([i for i in self[::-1]])

    def __contains__(self, item):
        temp = self.root
        while temp and temp.val != item:
            temp = temp.next
        return temp is not None

    def __str__(self):
        return ' -- '.join(str(i) for i in self)