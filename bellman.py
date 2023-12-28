import sys
import random
import time
from typing import List

INFTY = sys.maxsize
M1 = None
M2 = None
N = 0
nodes = []
st = 0
inf = 2000000000
Emax = 1000
edge = []


class Edges:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w


def generation():
    global M1, M2, N, nodes
    naprav = 0

    print("\n Укажите размер матрицы N*N: ")

    # N = int(input("--> "))

    k = True
    while k:
        N = input("--> ")
        if N.isdigit() and int(N) >= 1:
            k = False
        else:
            print(f"Введите целое число больше нуля...")
    N = int(N)

    print(" Ориентированный граф?")
    print("\n Да - 1 ")
    print(" Нет - 2")
    # c = 2
    # c = input("--> ")

    k = True
    while k:
        c = input("--> ")
        if c.isdigit() and (int(c) == 1 or int(c) == 2):
            k = False
        else:
            print(f"Введите 1, если да, 2, если нет...")
    c = int(c)

    print("\n")
    if str(c) == "1":
        naprav = 1

    M1 = [[0] * N for _ in range(N)]
    nodes = [0] * N

    random.seed()
    for i in range(N):
        M1[i][i] = 0
        for j in range(i + 1, N):
            ch = random.randint(0, 9)
            ch2 = random.randint(0, 99)
            if ch < 7:
                if ch2 < 1:
                    ch = -ch
                M1[i][j] = ch
            else:
                M1[i][j] = 0
            M1[j][i] = M1[i][j]

    M2 = [[0] * N for _ in range(N)]

    for i in range(N):
        M2[i][i] = 0
        for j in range(N):
            ch = random.randint(0, 14)
            ch2 = random.randint(0, 99)
            if ch < 12:
                if ch > 9:
                    ch = ch - 6
                if ch2 < 1:
                    ch = -ch
                M2[i][j] = ch
            else:
                M2[i][j] = 0

    if naprav == 1:
        for i in range(N):
            for j in range(N):
                M1[i][j] = M2[i][j]

    for i in range(N - 1, 0, -1):
        del M2[i]


def bellman_ford():
    global M1, N, nodes, st, inf, Emax, edge

    foutе = open("bellman_ford.txt", "a")

    for i in range(N):
        nodes[i] = inf

    parent = [-1] * N
    nodes[st] = 0

    for i in range(N - 1):
        change = False

        for i in range(len(edge)):
            if nodes[edge[i].u] + edge[i].w < nodes[edge[i].v]:
                nodes[edge[i].v] = max(-inf, nodes[edge[i].u] + edge[i].w)
                parent[edge[i].v] = edge[i].u
                change = True

        if not change:
            break

    for i in range(N):
        if nodes[i] == inf:
            print(f"\n {st + 1} -> {i + 1} = Путь отсутствует ")
            foutе.write(f"\n {st + 1} -> {i + 1} = Путь отсутствует")
        else:
            print(f"\n {st + 1} -> {i + 1} = {nodes[i]}", end=" ")
            foutе.write(f"\n {st + 1} -> {i + 1} = {nodes[i]} ")

            if nodes[i] >= 0 and nodes[i] < 10:
                print(" ", end=" ")

            path = []
            cur = i
            while cur != -1:
                for i2 in range(len(path)):
                    if cur == path[i2] and len(path) > 1:
                        path.append(cur)
                        print(" (Отрицательный цикл)")
                        foutе.write(" (Отрицательный цикл)")
                        return
                path.append(cur)
                cur = parent[cur]

            path.reverse()
            print(" (", end=" ")
            foutе.write(" ( ")
            for i in range(len(path)):
                if (i + 1) != len(path):
                    print(f"{path[i] + 1} -> ", end=" ")
                    foutе.write(f"{path[i] + 1} ->  ")
                else:
                    print(f"{path[i] + 1}", end=" ")
                    foutе.write(f"{path[i] + 1} ")
            print(")", end=" ")
            foutе.write(") ")
    foutе.write(f"\n\n\n -------------------------- ")


def main():
    global M1, M2, N, nodes, st, inf, Emax, edge

    fout = open("bellman_ford.txt", "a")

    if not fout:
        print("\n Ошибка открытия файла")
        return sys.exit()

    fout.write("\n\n\n")

    print("\n Выберете способ ввода графа:")
    print(" 1 - вручную")
    print(" 2 - прочитать из файла input.txt")
    print(" 3 - случайная генерация")

    c = input("--> ")

    if c == "1":
        # print("\n Количество вершин > ")
        # N = int(input("\n Количество вершин > "))

        k = True
        while k:
            N = input("\n Количество вершин > ")
            if N.isdigit() and int(N) >= 1:
                k = False
            else:
                print("Количество вершин должно быть только целым числом\nВведите число вершин еще раз...")
        N = int(N)

        nodes = [0] * N

        M1 = [[0] * N for _ in range(N)]

        e = 0
        for i in range(N):
            for j in range(N):
                print(f" Вес {i + 1} -> {j + 1} = ", end=" ")
                # w = int(input())

                k = True
                while k:
                    w = input()
                    try:
                        int(w)
                        k = False
                    except:
                        print(
                            "Вес должен быть только целым полпжительным или отрицательным числом\nВведите вес еще раз...")
                w = int(w)

                M1[i][j] = 0
                if w != 0:
                    edge.append(Edges(i, j, w))
                    M1[i][j] = w
                    e += 1

        print("\n")
    elif c == "2":
        try:
            fin = open("input.txt", "r")
        except FileNotFoundError:
            print("\n\n Ошибка открытия файла")
            print("\n Проверьте существование файла input.txt")
            print("\n Для корректной работы программы файл должен быть заполнен в таком виде:")
            print("\n Первая строка - кол-во вершин")
            print("\n Начиная со второй - матрица смежности")
            print("\n\n Пример заполнения:")
            print("\n 3 ")
            print("\n 0 8 0 ")
            print("\n 3 0 0 ")
            print("\n 4 0 0\n ")

            fout.close()
            fout = open("input.txt", "w")
            fout.close()
            return

        print("\n\n Файл открыт")

        N = int(fin.readline())

        nodes = [0] * N
        M1 = [[0] * N for _ in range(N)]

        for i in range(N):
            line = fin.readline()
            for j, val in enumerate(line.split()):
                M1[i][j] = int(val)

        fin.close()
        # print("из файла: ", M1)
        e = 0
        for i in range(N):
            for j in range(N):
                if M1[i][j] != 0:
                    edge.append(Edges(i, j, M1[i][j]))
                    e += 1

    elif c == "3":
        # print("\n")
        generation()
        e = 0
        for i in range(N):
            for j in range(N):
                if M1[i][j] != 0:
                    edge.append(Edges(i, j, M1[i][j]))
                    e += 1

    else:
        main()

    print("    ", end=" ")
    fout.write("    ")

    for i in range(N):
        print(f"[{i + 1}] ", end=" ")
        fout.write(f"[{i + 1}] ")

    for i in range(N):
        print(f"\n[{i + 1}]", end=" ")
        fout.write(f"\n[{i + 1}]")

        for j in range(N):
            if (i + 1) < 10:
                if M1[i][j] < 0:
                    print('\b', end=" ")

                if j < 10:
                    print(f"{M1[i][j]:3d} ", end=" ")
                    fout.write(f"{M1[i][j]:3d} ")
                else:
                    print(f" {M1[i][j]:3d} ", end=" ")
                    fout.write(f" {M1[i][j]:3d} ")
            elif (i + 1) < 100:
                if j == 0:
                    print(f" {M1[i][j]}", end=" ")
                    fout.write(f" {M1[i][j]}")
                elif j < 10:
                    print(f"   {M1[i][j]}", end=" ")
                    fout.write(f"   {M1[i][j]}")
                else:
                    print(f"    {M1[i][j]}", end=" ")
                    fout.write(f"    {M1[i][j]}")

    print("\n\n Стартовая вершина > ", end=" ")
    # st = int(input())

    k = True
    while k:
        st = input()
        if st.isdigit() and 1 <= int(st) <= N:
            k = False
        else:
            print(f"Введите целое число в диапозоне от 1 до {N}...")
    st = int(st)

    fout.write(f"\n\n Стартовая вершина > {st}")
    st -= 1
    print("\n\n Список кратчайших путей:")
    fout.write("\n Список кратчайших путей:")
    fout.close()

    bellman_ford()

    for i in range(N - 1, 0, -1):
        del M1[i]

    del M1


def titulniyList():
    print("\n Министерство науки и высшего образования Российской Федерации")
    print(" Пензенский государственный университет")
    print(" Кафедра «Вычислительная кафедра»\n")
    print(" КУРСОВОЙ ПРОЕКТ")
    print(" по дисциплине:\n ЛОГИКА И ОСНОВЫ АЛГОРИТМИЗАЦИИ В ИНЖЕНЕРНЫХ ЗАДАЧАХ")
    print(" тема проекта:\n Реализация алгоритма Форда Беллмана\n\n")
    print(" Выполнил:\n студент группы 22ВВВ2\n Демини М.С. \n\n")
    print(" Принял:\n Акифьев И.В.\n\n Пенза 2023\n")


def wanna_more():  # продолжение после окончания рассчетов
    k = True
    while k:
        todo = input("\n\nПродолжаем Форда?\n 1 - да\n 2 - нет\n -> ")
        if todo.isdigit() and (int(todo) == 1 or int(todo) == 2):
            k = False
        else:
            print(f"Введите целое число: '1' или '2'...")
    todo = int(todo)
    if todo == 1:
        main()
    else:
        print("\n\nЗавершение работы...\n\n...MaxSDemin ©️2023...")
        return False
    return True


if __name__ == "__main__":
    titulniyList()
    main()
    while wanna_more():
        pass
