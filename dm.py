import tkinter as tk
import numpy as np
import math
import matplotlib
from pyparsing import col
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx


class Table:
     
    def __init__(self, frame, dim):
        for i in range(dim):
            for j in range(dim):
                if (i == 0):
                    self.v = tk.Label(frame, text=f'V{j + 1}')
                    self.v.grid(row=i+1, column=j + 1)
                    widgets_for_destroying.append(self.v)

                self.var = tk.IntVar()
                self.e = tk.Checkbutton(frame, variable=self.var)
                widgets_for_destroying.append(self.e)
                fields[i][j] = self.var

                if (j == 0):
                    self.v = tk.Label(frame, text=f'V{i + 1}')
                    self.v.grid(row=i + 2, column=j)
                    widgets_for_destroying.append(self.v)

                self.e.grid(row=i + 2, column=j + 1, sticky='e')


def getMatrixMinor(m, i, j):
    return np.array( [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])] )


def read_data():
    graph = {}
    ways_to_vertex = {}
    for n in range(dim):
        for m in range(dim):
            state = fields[n][m].get() 
            if state:
                if m in ways_to_vertex.keys():
                    ways_to_vertex[m] += 1
                else:
                    ways_to_vertex[m] = 1

                if n in graph.keys():
                    if m not in graph[n]:
                        graph[n].append(m)
                else:
                    graph[n] = [m]

    a = [ [ 1 if (i in graph.keys() and j in graph[i]) else 0 for j in range(dim) ] for i in range(dim) ]
    d = [ [ 0 if (i != j or j not in ways_to_vertex.keys()) else ways_to_vertex[j] for j in range(dim) ] for i in range(dim) ]
    b = [ [d[i][j] - a[i][j] for j in range(dim)] for i in range(dim) ]

    return (graph, b, d)


def draw_graph(g, G, pos, cnt, label_dict, color_map, main_graph_frame):
    # graph_frame = tk.Frame(second_frame)
    graph_frame = tk.Frame(main_graph_frame)
    graph_frame.grid(row = 4 + cnt // 3, column = cnt % 3, pady=10, padx=10, sticky="w")

    # widgets_for_destroying.append(graph_frame)

    G.add_edges_from(g)

    f = plt.figure(figsize=(3.5, 3.5))
    a = f.add_subplot(111)
    plt.axis('off')

    nx.draw_networkx(G, pos, ax=a, node_color=color_map, node_size=600, with_labels=True, labels=label_dict)

    canvas = FigureCanvasTkAgg(f, master=graph_frame)
    canvas.draw()
        
    canvas.get_tk_widget().pack()

    G.remove_edges_from(g)


def product(a, index, item):
    for i in a[index]:
        try:
            item.pop(index)
        except:
            pass
        item.append(i)
        if (index == len(a) - 1):
            res.append(item.copy())
        else:
            product(a, index + 1, item.copy())


def check_tree(tree):
    global dim
    vertex = [0] * dim

    for d in tree:
        vertex[d[0]] = 1; vertex[d[1]] = 1
        if (d[1], d[0]) in tree:
            return False

    if 0 in vertex:
        return False
    return True


def find_all_grandtress(graph, ker):
    colours = []
    for i in range(dim):
        colours.append([])

    for u in graph.keys():
        for v in graph[u]: 
            colours[v].append((u, v))

    colours.pop(ker)
    global res
    res = []
    product(colours, 0, [])

    for i in range(len(res) - 1, -1, -1):
        if not check_tree(res[i]):
            res.pop(i)


    G = nx.DiGraph()
    for d in range(dim):
        G.add_node(d)
    pos = nx.shell_layout(G)

    label_dict = {}
    for d in range(dim):
        label_dict[d] = f"V{d + 1}"


    main_graph_frame = tk.Frame(second_frame)
    main_graph_frame.grid(row=3, column=0, padx=300, pady=5)
    widgets_for_destroying.append(main_graph_frame)

    color_map = get_color_map(ker)
    cnt = 0
    for r in res:
        draw_graph(r, G, pos, cnt, label_dict, color_map, main_graph_frame)
        cnt += 1


def get_color_map(ker):
    color_map = []
    for d in range(dim):
        if d == ker:
            color_map.append('#ffa6d0')
        else:
            color_map.append('#99ccff')
    return color_map


def search_grandtrees(graph, b, d):
    for i in range(dim):
        if d[i][i] == 0:
            b_det = math.ceil(np.linalg.det(getMatrixMinor(b, i, i)))
            
            answer_frame = tk.Frame(second_frame)
            answer_frame.grid(row=2, column=0)
            widgets_for_destroying.append(answer_frame)
            answer_label = tk.Label(answer_frame, text=f"Ответ: из вершины V{i + 1} ориентированного графа можно построить {b_det} прадеревьев:", font="Arial 20")
            answer_label.grid(row=0, column=0)
            
            find_all_grandtress(graph, i)
            break
        

def main_algo():
    read_data_btn['state'] = 'disabled'
    graph, b, d = read_data() 
    search_grandtrees(graph, b, d)


def destroy_widgets():
    for w in widgets_for_destroying:
        w.destroy()

    vertex_cnt_btn['state'] = 'normal'


def matrix_builder():
    vertex_cnt_btn['state'] = 'disabled'
    global dim
    dim = int(vertex_cnt_input.get())
    t = Table(tabel_frame, dim)
    
    global read_data_btn
    read_data_btn = tk.Button(tabel_frame, text="Получить ответ", command=main_algo, font="Arial 15")
    read_data_btn.grid(row=200, column=200)
    widgets_for_destroying.append(read_data_btn)


def main():
    global vertex_cnt_btn
    global vertex_cnt_input
    global tabel_frame
    global fields
    global root
    global widgets_for_destroying; widgets_for_destroying = []
    global tabel_frame
    
    global second_frame
    global main_frame
    global main_canvas

    fields = []
    for _ in range(50):
        fields.append([0] * 50)
    
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    main_canvas = tk.Canvas(main_frame)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    y_scrollbar = tk.Scrollbar(main_frame,orient=tk.VERTICAL,command=main_canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    second_frame = tk.Frame(main_canvas)

    second_frame.bind("<Configure>", lambda event: main_canvas.configure(scrollregion = main_canvas.bbox(tk.ALL)))
    main_canvas.configure(yscrollcommand=y_scrollbar.set)
    main_canvas.create_window((0,0), window = second_frame, anchor = tk.N + tk.W)

    vertex_cnt_frame = tk.Frame(second_frame)
    vertex_cnt_frame = tk.Frame(second_frame)
    vertex_cnt_frame.grid(row=0, sticky='w')

    vertex_cnt_label = tk.Label(vertex_cnt_frame, text="Количество вершин в графе:", font="Arial 20")
    vertex_cnt_label.grid(row=0, column=0, pady=10, padx=15)

    vertex_cnt_input = tk.Entry(vertex_cnt_frame, font="Arial 20", width="7")
    vertex_cnt_input.grid(row=0, column=1, pady=10)

    vertex_cnt_btn = tk.Button(vertex_cnt_frame, text="Ок", command=matrix_builder, font="Arial 15") 
    vertex_cnt_btn.grid(row=0, column=2, padx=15)

    vertex_refresh_btn = tk.Button(vertex_cnt_frame, text="Перезагрузить", command=destroy_widgets, font="Arial 15") 
    vertex_refresh_btn.grid(row=0, column=3, padx=15)

    tabel_frame = tk.Frame(second_frame)
    tabel_frame.grid(row=1, pady=10, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()