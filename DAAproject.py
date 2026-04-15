import heapq
import tkinter as tk
from tkinter import ttk

graph = {
    "Entrance": [("Reception", 2), ("Emergency", 3)],
    "Reception": [("Entrance", 2), ("OPD", 2), ("Pharmacy", 4)],
    "Emergency": [("Entrance", 3), ("ICU", 2), ("Radiology", 5)],  
    "OPD": [("Reception", 2), ("Lab", 2), ("Ward A", 4)],
    "Pharmacy": [("Reception", 4), ("Ward B", 3), ("Billing", 2)],
    "ICU": [("Emergency", 2), ("Ward B", 2), ("OT", 3)],
    "Radiology": [("Emergency", 5), ("Lab", 2), ("MRI", 2)],
    "Lab": [("OPD", 2), ("Radiology", 2), ("Ward A", 3), ("MRI", 3)],  
    "Ward A": [("OPD", 4), ("Lab", 3), ("Ward B", 2)],
    "Ward B": [("Pharmacy", 3), ("ICU", 2), ("Ward A", 2), ("Billing", 3)],
    "OT": [("ICU", 3)],
    "MRI": [("Radiology", 2), ("Lab", 3)],  
    "Billing": [("Pharmacy", 2), ("Ward B", 3), ("Exit", 4)],
    "Exit": [("Billing", 4)]
}

positions = {

    "Entrance": (50, 250),
    "Reception": (150, 150),
    "Emergency": (150, 350),


    "OPD": (300, 100),
    "Pharmacy": (300, 250),
    "ICU": (300, 400),


    "Radiology": (450, 300),
    "MRI": (550, 350),
    "Lab": (450, 150),


    "Ward A": (650, 100),
    "Ward B": (650, 250),
    "OT": (650, 400),

    "Billing": (800, 250),
    "Exit": (900, 250)
}

def dijkstra(graph, start, end=None):
    pq = [(0, start)]
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    parent = {node: None for node in graph}

    while pq:
        d, node = heapq.heappop(pq)

        if d > dist[node]:
            continue

        if node == end:
            break

        for neigh, w in graph[node]:
            new_d = d + w
            if new_d < dist[neigh]:
                dist[neigh] = new_d
                parent[neigh] = node
                heapq.heappush(pq, (new_d, neigh))

    return dist, parent


def get_path(parent, end):
    path = []
    while end:
        path.append(end)
        end = parent[end]
    return path[::-1]

root = tk.Tk()
root.title("🏥 Hospital Navigation System")
root.geometry("950x650")
root.configure(bg="#f0f8ff")

title = tk.Label(root, text="Hospital Route Finder",
                 font=("Arial", 20, "bold"),
                 bg="#f0f8ff", fg="#2c3e50")
title.pack(pady=10)

control_frame = tk.Frame(root, bg="#f0f8ff")
control_frame.pack(pady=10)

start_var = tk.StringVar()
end_var = tk.StringVar()

ttk.Label(control_frame, text="Select Source:").grid(row=0, column=0, padx=10)
start_menu = ttk.Combobox(control_frame, textvariable=start_var,
                          values=list(graph.keys()), state="readonly")
start_menu.grid(row=0, column=1, padx=10)

ttk.Label(control_frame, text="Select Destination:").grid(row=0, column=2, padx=10)
end_menu = ttk.Combobox(control_frame, textvariable=end_var,
                        values=list(graph.keys()), state="readonly")
end_menu.grid(row=0, column=3, padx=10)

canvas = tk.Canvas(root, width=1000, height=500,
                   bg="white",
                   highlightthickness=2,
                   highlightbackground="#3498db")
canvas.pack(pady=10)

def draw_map(path=None):
    canvas.delete("all")


    for node in graph:
        for neigh, _ in graph[node]:
            x1, y1 = positions[node]
            x2, y2 = positions[neigh]
            canvas.create_line(x1, y1, x2, y2, fill="#bdc3c7", width=2)

    if path:
        for i in range(len(path) - 1):
            x1, y1 = positions[path[i]]
            x2, y2 = positions[path[i + 1]]
            canvas.create_line(x1, y1, x2, y2, width=5, fill="#e74c3c")


    for node, (x, y) in positions.items():
        canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="#3498db")
        canvas.create_text(x, y, text=node,
                           font=("Arial", 8, "bold"), fill="white")

draw_map()

def find_path():
    start = start_var.get()
    end = end_var.get()
    if not start or not end:
        result_label.config(text="⚠ Please select both source and destination")
        return
    dist, parent = dijkstra(graph, start, end)
    path = get_path(parent, end)
    draw_map(path)
    result_label.config(
        text=f"Shortest Path: {' → '.join(path)}   |   Distance: {dist[end]} units"
    )
btn = tk.Button(root, text="Find Shortest Path",
                command=find_path,
                bg="#27ae60", fg="white",
                font=("Arial", 12, "bold"),
                padx=10, pady=5)
btn.pack(pady=10)
result_label = tk.Label(root, text="",
                        font=("Arial", 12),
                        bg="#f0f8ff", fg="#2c3e50")
result_label.pack()
root.mainloop()