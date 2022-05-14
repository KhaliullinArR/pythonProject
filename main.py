import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue
from collections import deque


class MyGraph:
    def __init__(self):
        self.graph_mat = []
        self.G = nx.Graph()
        self.per_nodes = None

    def readGraph(self, fname):
        f = open(fname, "r")

        temp = []
        while True:
            s = f.read(1)
            if s == '':
                self.graph_mat.append(temp.copy())
                temp.clear()
                break
            if s != '\n' and s != ' ':
                temp.append(int(s))
            if s == '\n':
                self.graph_mat.append(temp.copy())
                temp.clear()
        f.close()
        g = np.array(self.graph_mat)
        if (not (np.all(g == g.T))):
            print('Матрица не симметричная, введите другую или исправьте существующую!')
            self.graph_mat = []
        else:
            t = len(graph.graph_mat)

            for i in range(t):
                self.G.add_node(i)

            for i in range(t):
                for j in range(t):
                    if (graph.graph_mat[i][j] == 1) and (i != j):
                        self.G.add_edge(i, j)

    def viewGraph(self):
        nx.draw(self.G, with_labels=True, node_size=600, font_size=20, font_color='Orange', node_shape='D')
        plt.show()

    def viewPeripheralNodes(self):
        if self.per_nodes is None:
            self.getPeripheralNodes()
        node_colors = ['#1f78b4' if i not in self.per_nodes else 'red' for i in self.G.nodes()]
        nx.draw(self.G, with_labels=True, node_size=600, font_size=20, font_color='Orange', node_shape='D',
                node_color=node_colors)
        plt.show()

    def viewPeripheralPath(self, vk, vn):
        a = self.getPeripheralPath(vk, vn)
        b = []
        if len(a) == 0:
            print('Пути через заданные вершины не существует.')
            return
        for i in range(len(a) - 1):
            temp = (a[i], a[i + 1])
            b.append(temp)

        for e in self.G.edges():
            self.G[e[0]][e[1]]['color'] = 'black'

        for i in b:
            self.G.edges[i[0], i[1]]['color'] = 'red'

        edge_colors = nx.get_edge_attributes(self.G, 'color')
        if self.per_nodes is None:
            self.getPeripheralNodes()
        node_colors = ['#1f78b4' if i not in self.per_nodes else 'red' for i in self.G.nodes()]
        node_colors[vk] = '#00ff61'
        node_colors[vn] = '#00ff61'
        nx.draw(self.G, with_labels=True, node_size=600, font_size=20, node_shape='D',
                node_color=node_colors, edge_color=edge_colors.values())
        plt.show()

    def getPeripheralPath(self, vk, vn):
        self.getPeripheralNodes()
        path = []
        n = len(self.graph_mat)
        M = [0 for h in range(n)]
        st = deque()
        st.append(vn)
        M[vn] = 1
        ks = 0
        L = 0
        while (ks >= 0):
            v = st[len(st) - 1]
            Pr = 0
            for j in range(L, n):
                if self.graph_mat[v][j] == 1:
                    if j == vk:
                        if vk in self.per_nodes or True in [True if y in self.per_nodes else False for y in st]:
                            st.append(vk)
                            path = [el for el in st]
                            return path
                    else:
                        if M[j] == 0:
                            Pr = 1
                            break
            if Pr == 1:
                ks = ks + 1
                st.append(j)
                L = 0
                M[j] = 1
            else:
                L = v + 1
                M[v] = 0
                st.pop()
                ks = ks - 1
        return path

    def getPeripheralNodes(self):
        if self.per_nodes is not None:
            return self.per_nodes
        else:
            n = len(self.graph_mat)
            d = {}
            for i in range(n):
                i_paths = []
                for j in range(n):
                    temp = self.findShortestPath(i, j)
                    i_paths.append(temp)
                max = 0
                for arr in i_paths:
                    if arr[1] > max:
                        max = arr[1]
                temp = []
                for arr in i_paths:
                    if (arr[1] == max):
                        temp.append(arr)
                d[i] = temp

            d_max = 0
            for a in d.values():
                if a[0][1] > d_max:
                    d_max = a[0][1]
            d_copy = {}
            for k in d.keys():
                if d[k][0][1] == d_max:
                    d_copy[k] = d[k]
        self.per_nodes = d_copy.keys()
        return self.per_nodes

    def findShortestPath(self, vk, vn):
        if vk == vn:
            return vn, 0
        n = len(self.graph_mat)
        path = []
        M = [-1 for i in range(n)]
        F = -1
        R = -1
        R = R + 1
        Q = Queue()
        Q.put(vk)
        M[vk] = n + 1
        while F != R:
            F += 1
            v = Q.get()
            for j in range(n):
                if self.graph_mat[v][j] == 1:
                    if j == vn:
                        path.append(vn)
                        while v != n + 1:
                            path.append(v)
                            v = M[v]
                        return path, len(path)
                    if M[j] == -1:
                        R += 1
                        Q.put(j)
                        M[j] = v
        return path, len(path)


graph = MyGraph()
graph.readGraph("graph.txt")
graph.viewPeripheralNodes()
print('Введите номера вершин, через которые должен проходить путь:')
a = int(input())
b = int(input())
graph.viewPeripheralPath(a, b)
