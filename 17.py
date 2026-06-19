import os

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.letters = 0
        self.has_letter = False


class Tree:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def build(self, n, adj, letters):
        for i in range(1, n + 1):
            node = Node(i)
            node.letters = letters[i]
            node.has_letter = (letters[i] > 0)
            self.nodes[i] = node

        if n < 1:
            return

        self.root = self.nodes[1]
        stack = [1]
        parent = {1: None}

        while stack:
            v = stack.pop()
            for nb in adj[v]:
                if nb != parent.get(v):
                    parent[nb] = v
                    self.nodes[v].children.append(self.nodes[nb])
                    stack.append(nb)

    def compute_apologies(self):
        if self.root is None:
            return 0

        order = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            order.append(node)
            for child in node.children:
                stack.append(child)

        has_in_subtree = {}
        for node in reversed(order):
            total = node.has_letter

            for child in node.children:
                total = total or has_in_subtree[child]
            has_in_subtree[node] = total

        if not any(has_in_subtree[node] for node in self.nodes.values()):
            return 0

        edges = 0
        max_depth = 0
        stack = [(self.root, 0)]

        while stack:
            node, depth = stack.pop()
            if node.has_letter and depth > max_depth:
                max_depth = depth

            for child in node.children:
                if has_in_subtree[child]:
                    edges += 1
                    stack.append((child, depth + 1))
        return edges - max_depth


def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("Файл пуст")

    n = int(lines[0])
    adjacency = [[] for _ in range(n + 1)]
    letters = [0] * (n + 1)

    for i in range(1, n + 1):
        parts = list(map(int, lines[i].split()))
        if not parts:
            continue

        ni = parts[0]
        li = parts[1]
        letters[i] = li
        neighbors = parts[2:2 + ni]
        for nb in neighbors:
            adjacency[i].append(nb)

    return n, adjacency, letters


def solve(filename):
    n, adjacency, letters = read_data(filename)
    tree = Tree()
    tree.build(n, adjacency, letters)
    return tree.compute_apologies()


def main():
    while True:
        print("\n" + "=" * 50)
        print("  МУДРЫЙ ТРИТОН - ПОЧТАЛЬОН ЛУКОМОРЬЯ")
        print("=" * 50)
        print("1. Загрузить данные из файла и вычислить результат")
        print("2. Показать пример входного файла")
        print("3. Выйти")
        print("=" * 50)
        choice = input("Выберите действие (1-3): ").strip()

        if choice == '1':
            filename = input("Введите имя файла (по умолчанию input.txt): ").strip()
            if not filename:
                filename = "input.txt"

            if not os.path.exists(filename):
                print(f"Ошибка: файл '{filename}' не найден.")
                continue

            try:
                result = solve(filename)
                print(f"\nРезультат: минимальное количество извинений = {result}")
            except Exception as e:
                print(f"Ошибка при обработке файла: {e}")

        elif choice == '2':
            print("\nПример входного файла (сохраните как input.txt):")
            print("5")
            print("3 2 2 5 4")
            print("1 1 1")
            print("1 1 4")
            print("2 2 3 1")
            print("1 3 1")
            print("\nОжидаемый выход: 2")

        elif choice == '3':
            print("До свидания!")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")


if __name__ == "__main__":
    main()