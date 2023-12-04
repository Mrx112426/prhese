from dataclasses import dataclass
import random
from typing import TextIO


@dataclass
class Student:
    name: str
    group_number: str
    course: int
    age: int
    average_grade: float

    def key(self) -> float:
        return self.average_grade

    def __str__(self) -> str:
        return f"Student({self.name}, {self.group_number}, {self.course}, {self.age}, {self.average_grade})"


class Node:
    def __init__(self, student: Student):
        self.student = student
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self._root = None

    def is_empty(self) -> bool:
        """Проверяет, пустое ли дерево."""
        return self._root is None

    def __height(self, node: Node) -> int:
        """Возвращает высоту узла (рекурсивно)."""
        if node is None:
            return 0
        return node.height

    def __bfactor(self, node: Node) -> int:
        """Вычисляет разницу высот правого и левого поддеревьев."""
        return self.__height(node.right) - self.__height(node.left)

    def __update_height(self, node: Node) -> None:
        """Обновляет высоту узла."""
        left_height = self.__height(node.left)
        right_height = self.__height(node.right)
        node.height = max(left_height, right_height) + 1

    def __rotate_right(self, node: Node) -> Node:
        """Поворот вправо вокруг узла node."""
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self.__update_height(node)
        self.__update_height(left_child)
        return left_child

    def __rotate_left(self, node: Node) -> Node:
        """Поворот влево вокруг узла node."""
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self.__update_height(node)
        self.__update_height(right_child)
        return right_child

    def __balance(self, node: Node) -> Node:
        """Балансировка узла node."""
        self.__update_height(node)
        if self.__bfactor(node) >= 2:
            if self.__bfactor(node.right) < 0:
                node.right = self.__rotate_right(node.right)
            return self.__rotate_left(node)
        if self.__bfactor(node) <= -2:
            if self.__bfactor(node.left) > 0:
                node.left = self.__rotate_left(node.left)
            return self.__rotate_right(node)
        return node

    def __insert(self, node: Node, student: Student) -> Node:
        """Рекурсивно вставляет узел в дерево и балансирует его."""
        if node is None:
            return Node(student)
        if student.key() < node.student.key():
            node.left = self.__insert(node.left, student)
        else:
            node.right = self.__insert(node.right, student)
        return self.__balance(node)

    def insert(self, student: Student) -> None:
        """Вставляет студента в дерево и балансирует его."""
        self._root = self.__insert(self._root, student)

    def __find_minimum(self, node: Node) -> Node:
        """Находит узел с минимальным ключом (самый левый узел)."""
        current_node = node.left
        if current_node is None:
            return node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def __remove_minimum(self, node: Node) -> Node:
        """Удаляет узел с минимальным ключом из поддерева и балансирует его."""
        if node.left is None:
            return node.right
        node.left = self.__remove_minimum(node.left)
        return self.__balance(node)

    def __remove(self, node: Node, key: float) -> Node:
        """Рекурсивно удаляет узел с ключом key и балансирует дерево."""
        if node is None:
            return None
        if key < node.student.key():
            node.left = self.__remove(node.left, key)
        elif key > node.student.key():
            node.right = self.__remove(node.right, key)
        else:
            left_child = node.left
            right_child = node.right
            node = None
            if right_child is None:
                return left_child
            min_node = self.__find_minimum(right_child)
            min_node.right = self.__remove_minimum(right_child)
            min_node.left = left_child
            return self.__balance(min_node)
        return self.__balance(node)

    def remove(self, key: float) -> None:
        """Удаляет студента с указанным ключом и балансирует дерево."""
        if self.is_empty():
            raise Exception("Tree is empty")
        self._root = self.__remove(self._root, key)

    def find(self, key: float) -> tuple[Student, bool]:
        """Находит студента по ключу."""
        if self.is_empty():
            return None, False
        current_node = self._root
        while current_node is not None:
            if key < current_node.student.key():
                current_node = current_node.left
            elif key > current_node.student.key():
                current_node = current_node.right
            else:
                return current_node.student, True
        return None, False

    def minimum(self) -> Student:
        """Находит студента с минимальным ключом (самый левый)."""
        if self.is_empty():
            raise Exception("Tree is empty")
        current_node = self._root
        while current_node.left is not None:
            current_node = current_node.left
        return current_node.student

    def maximum(self) -> Student:
        """Находит студента с максимальным ключом (самый правый)."""
        if self.is_empty():
            raise Exception("Tree is empty")
        current_node = self._root
        while current_node.right is not None:
            current_node = current_node.right
        return current_node.student

    def symmetric_traversal(self, func: callable) -> None:
        """Выполняет симметричный обход дерева и применяет функцию func к каждому узлу."""
        def symmetric_traversal_recursive(node):
            if node is not None:
                symmetric_traversal_recursive(node.left)
                func(node.student)
                symmetric_traversal_recursive(node.right)

        symmetric_traversal_recursive(self._root)

    def print_tree(self) -> None:
        """Выводит структуру дерева на экран."""
        if self.is_empty():
            print("Tree is empty")
            return
        self.__print_tree_recursive(self._root, "", True)

    def __print_tree_recursive(self, node: Node, prefix: str, is_tail: bool) -> None:
        """Рекурсивно выводит структуру дерева."""
        if node.right is not None:
            new_prefix = prefix + ("│   " if is_tail else "    ")
            self.__print_tree_recursive(node.right, new_prefix, False)
        print(prefix + ("└── " if is_tail else "┌── ") + str(node.student))
        if node.left is not None:
            new_prefix = prefix + ("    " if is_tail else "│   ")
            self.__print_tree_recursive(node.left, new_prefix, True)

    def save_to_file(self, file_path: str) -> None:
        """Сохраняет состояние дерева в файл."""
        with open(file_path, "w") as file:
            self._save_to_file_recursive(self._root, file)

    def _save_to_file_recursive(self, node: Node, file: TextIO) -> None:
        """Рекурсивно сохраняет узлы дерева в файл."""
        if node is not None:
            file.write(
                f"{node.student.name},{node.student.group_number},{node.student.course},{node.student.age},{node.student.average_grade}\n")
            self._save_to_file_recursive(node.left, file)
            self._save_to_file_recursive(node.right, file)

    def load_from_file(self, file_path: str) -> None:
        """Загружает данные из файла и создает дерево."""
        with open(file_path, "r") as file:
            lines = file.readlines()
            students = []
            for line in lines:
                parts = line.strip().split(',')
                name, group_number, course, age, average_grade = parts
                student = Student(name, group_number, int(course), int(age), float(average_grade))
                students.append(student)

            self._root = None
            for student in students:
                self.insert(student)


if __name__ == '__main__':
    students = [
        Student("Умар", "4217", 2, 19, 97),
        Student("Дима", "4217", 2, 19, 5),
        Student("Александр", "4217", 3, 19, 12),
        Student("Шерзод", "4217", 2, 19, 47),
        Student("Никита", "4217", 2, 19, 91),
        Student("Лиза", "4217", 2, 19, 65),
        Student("Нефорочек", "4217", 2, 19, 10),
        Student("Настя", "4217", 2, 19, 86),
        Student("Наташа", "4217", 2, 19, 76),
        Student("Влад Лайхтман", "4217", 2, 19, 44),
    ]

    tree = AVLTree()
    for student in students:
        tree.insert(student)

    print("----- Find ------")
    key_to_find = students[0].average_grade  # Пример: поиск по средней оценке студента Max
    found_student, found = tree.find(key_to_find)
    if found:
        print(f"Found student with key value {key_to_find}: {found_student}")
    else:
        print(f"Student with key value {key_to_find} not found")

    print("----- Max key ------")
    max_student = tree.maximum()
    print(f"Student with max key value: {max_student}")

    print("----- Min key ------")
    min_student = tree.minimum()
    print(f"Student with min key value: {min_student}")

    print("----- Remove ------")
    key_to_remove = students[1].average_grade  # Пример: удаление студента Alex
    print(f"Remove student with key value: {key_to_remove}")
    tree.remove(key_to_remove)
    tree.print_tree()

    # Сохраняем дерево в файл students.txt
    tree.save_to_file("students.txt")

"""
if __name__ == '__main__':
    # Создаем пустое дерево
    tree = AVLTree()

    # Загружаем данные из файла "students.txt" в дерево
    tree.load_from_file("students.txt")

    # Теперь дерево содержит данные, считанные из файла

    # Выполним симметричный обход для вывода данных на экран
    print("----- Data Loaded From File ------")
    tree.symmetric_traversal(lambda student: print(student))
"""