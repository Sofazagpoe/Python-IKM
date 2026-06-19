class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        node = Node(value)
        if not self.top:
            self.top = node
        else:
            node.next = self.top
            self.top = node

    def pop(self):
        if self.top is None:
            raise IndexError("Ошибка. Стек пуст, извлекать нечего.")
        result = self.top
        self.top = self.top.next
        return result

    def is_empty(self):
        return self.top is None


def evaluate(expression):
    expr = expression.replace(" ", "")

    num_stack = Stack()
    op_stack = Stack()

    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isdigit():
            num = 0
            while i < n and expr[i].isdigit():
                num = num * 10 + int(expr[i])
                i += 1

            num_stack.push(num)
            continue

        elif ch == 'm' or ch == 'M':
            op_stack.push(ch)
            i += 1
            continue

        elif ch == '(' or ch == ',':
            i += 1
            continue

        elif ch == ')':
            try:
                b_node = num_stack.pop()
                a_node = num_stack.pop()
                op_node = op_stack.pop()
            except IndexError:
                raise ValueError("Ошибка. Нету операндов или операторов.")

            a = a_node.data
            b = b_node.data
            op = op_node.data

            if op == 'm':
                result = min(a, b)
            else:
                result = max(a, b)
            num_stack.push(result)
            i += 1
            continue

        else:
            raise ValueError(f"Недопустимый символ: '{ch}'")

    if num_stack.is_empty():
        raise ValueError("Недопустимое выражение: нет результата")

    result_node = num_stack.pop()
    if not num_stack.is_empty():
        raise ValueError("Недопустимое выражение: стек содержит более одного результата.")
    return result_node.data

def show_menu():
    print("\n" + "=" * 50)
    print("   КАЛЬКУЛЯТОР ВЫРАЖЕНИЙ С min И max")
    print("=" * 50)
    print("1. Ввести выражение и вычислить")
    print("2. Показать примеры выражений")
    print("3. Выход")
    print("=" * 50)

def show_examples():
    examples = [
        ("M(15,m(16,8))", 15),
        ("m(M(8,9),m(1,2))", 1),
        ("M(5,m(6,M(3,8)))", 6),
        ("m(10,20)", 10),
        ("M(10,20)", 20),
        ("M(m(5,3),M(7,2))", 7),
        ("m(100,200)", 100),
        ("M(100,200)", 200),
    ]

    print("\n--- Примеры выражений ---")
    for expr, expected in examples:
        try:
            result = evaluate(expr)
            status = "✓" if result == expected else "✗"
            print(f"  {expr} = {result} (ожид. {expected}) {status}")

        except Exception as e:
            print(f"  {expr} -> ОШИБКА: {e}")
    print("-------------------------------------")

def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            expr = input("\nВведите выражение (без пробелов): ").strip()
            if not expr:
                print("Ошибка: выражение не может быть пустым.")
                continue
            try:
                result = evaluate(expr)
                print(f"\nРезультат: {result}")
            except ValueError as e:
                print(f"\nОшибка вычисления: {e}")
            except Exception as e:
                print(f"\nНепредвиденная ошибка: {e}")

        elif choice == "2":
            show_examples()

        elif choice == "3":
            print("\nДо свидания!")
            break

        else:
            print("\nОшибка: неверный пункт меню. Выберите 1, 2 или 3.")

if __name__ == "__main__":
    main()