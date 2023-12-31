from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

@dataclass
class Car:
    make: str
    VIN: str
    engine_capacity: float
    price: float
    average_speed: float

    def __str__(self) -> str:
        return f"Car: {self.make}, VIN: {self.VIN}, Engine Capacity: {self.engine_capacity}, Price: {self.price}, Average Speed: {self.average_speed}"
@dataclass
class DoublyNode(Generic[T]):
    data: T
    next_ptr: Optional['DoublyNode[T]'] = None
    prev_ptr: Optional['DoublyNode[T]'] = None

class IndexOutRangeException(Exception):
    pass


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self._length: int = 0
        self._head: Optional[DoublyNode[T]] = None
        self._tail: Optional[DoublyNode[T]] = None

    def insertion_sort_by_vin(self) -> None:
        for i in range(1, self._length):
            temp = self.get(i)
            it = i
            while it > 0 and self.get(it - 1).VIN > temp.VIN:
                self.get(it).VIN, self.get(it - 1).VIN = self.get(it - 1).VIN, temp.VIN
                it -= 1

    def bubble_sort_by_average_speed(self) -> None:
        def swap(node1: 'DoublyNode[T]', node2: 'DoublyNode[T]') -> None:
            node1.data, node2.data = node2.data, node1.data

        for i in range(self._length):
            node = self._head
            for j in range(0, self._length - i - 1):
                if node.data.average_speed < node.next_ptr.data.average_speed:
                    swap(node, node.next_ptr)
                node = node.next_ptr
    def get_size(self) -> int:
        return self._length

    def _check_range(self, index: int) -> bool:
        if index >= self._length or index < 0:
            return False
        return True

    def is_empy(self) -> bool:
        return self._length == 0

    def push_tail(self, data: T) -> None:
        node = DoublyNode[T](data, None)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        self._tail.next_ptr = node
        node.prev_ptr = self._tail
        self._tail = node
        self._length += 1

    def push_head(self, data: T) -> None:
        node = DoublyNode[T](data)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        node.next_ptr = self._head
        self._head.prev_ptr = node
        self._head = node
        self._length += 1

    def insert(self, index: int, data: T) -> None:
        ok: bool = self._check_range(index)
        if not ok:
            raise IndexOutRangeException("-_-")

        if index == 0:
            self.push_head(data)
            return
        elif index == self._length - 1:
            self.push_tail(data)
            return

        node = self._head
        for i in range(0, index):
            node = node.next_ptr

        insert_node = DoublyNode[T](data)
        insert_node.next_ptr = node
        node.prev_ptr.next_ptr = insert_node
        insert_node.prev_ptr = node.prev_ptr
        node.prev_ptr = insert_node
        self._length += 1

    def get(self, index: int) -> T:
        ok: bool = self._check_range(index)
        if not ok:
            raise IndexOutRangeException("-_-")

        if index == 0:
            return self._head.data
        if index == self._length - 1:
            return self._tail.data

        node = self._head
        for i in range(0, index):
            node = node.next_ptr
        return node.data

    def remove(self, index: int) -> bool:
        ok: bool = self._check_range(index)
        if not ok:
            return False

        if index == 0:
            node = self._head
            self._head = node.next_ptr
            self._head.prev_ptr = None
            del node
            self._length -= 1
            return True

        node = self._head
        for i in range(0, index - 1):
            node = node.next_ptr

        if index == self._length - 1:
            self._tail.prev_ptr = None
            self._tail = node
            self._tail.next_ptr = None
            self._length -= 1
            return True

        delete_node = node.next_ptr
        node.next_ptr = delete_node.next_ptr
        node.next_ptr.prev_ptr = delete_node.prev_ptr
        self._length -= 1
        return True

    def for_each(self, func: Callable[[T], None]):
        node = self._head
        func(node.data)
        while node.next_ptr is not None:
            node = node.next_ptr
            func(node.data)

    def reverse_for_each(self, func: Callable[[T], None]):
        node = self._tail
        func(node.data)
        while node.prev_ptr is not None:
            node = node.prev_ptr
            func(node.data)

    def __str__(self) -> str:
        my_str: str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Current state: [{my_str}]"

if __name__ == '__main__':
    def print_list(data: T):
        print(data)

    doubly_linked_list = DoublyLinkedList[Car]()
    print(doubly_linked_list)

    # Пример заполнения списка автомобилей
    cars = [Car("Toyota", "12345", 2.0, 25000.0, 120.0),
            Car("Honda", "54321", 1.8, 22000.0, 130.0),
            Car("Ford", "98765", 2.5, 28000.0, 110.0),
            Car("Chevrolet", "67890", 2.4, 26000.0, 115.0),
            Car("Volkswagen", "23456", 1.6, 20000.0, 140.0)]
    for car in cars:
        doubly_linked_list.push_tail(car)

    print("Before sorting by VIN:")
    doubly_linked_list.for_each(print_list)

    doubly_linked_list.insertion_sort_by_vin()
    print("\nAfter sorting by VIN:")
    doubly_linked_list.for_each(print_list)

    doubly_linked_list.bubble_sort_by_average_speed()
    print("\nAfter sorting by average speed:")
    doubly_linked_list.for_each(print_list)