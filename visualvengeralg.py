import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D 

# Новая матрица стоимостей
cost_matrix = np.array([
    [5, 3, 2],
    [6, 3, 4],
    [7, 9, 5]
])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Венгерский алгоритм с покрытием линиями", fontsize=16)

def reduce_rows(matrix):
    return matrix - matrix.min(axis=1, keepdims=True)

def reduce_cols(matrix):
    return matrix - matrix.min(axis=0, keepdims=True)

def find_assignment(matrix):
    return [(0, 2), (1, 1)]  # A→Z, B→Y

def draw_coverage(ax, matrix, covered_rows, covered_cols):
    """Рисует линии покрытия на матрице"""
    for i in covered_rows:
        ax.axhline(i - 0.5, color='green', linestyle='--', linewidth=2)
    for j in covered_cols:
        ax.axvline(j - 0.5, color='blue', linestyle='--', linewidth=2)

def update(frame):
    ax1.clear()
    ax2.clear()
    
    if frame == 0:
        ax1.set_title("1. Исходная матрица")
        ax1.imshow(cost_matrix, cmap="Blues")
        for i in range(3):
            for j in range(3):
                ax1.text(j, i, cost_matrix[i, j], ha="center", va="center", color="red")
    
    elif frame == 1:
        reduced_rows = reduce_rows(cost_matrix)
        ax1.set_title("2. После редукции строк")
        ax1.imshow(reduced_rows, cmap="Blues")
        for i in range(3):
            for j in range(3):
                ax1.text(j, i, reduced_rows[i, j], ha="center", va="center", color="red")
    
    elif frame == 2:
        reduced = reduce_cols(reduce_rows(cost_matrix))
        ax1.set_title("3. После редукции столбцов")
        ax1.imshow(reduced, cmap="Blues")
        for i in range(3):
            for j in range(3):
                ax1.text(j, i, reduced[i, j], ha="center", va="center", color="red")
    
    elif frame == 3:
        reduced = reduce_cols(reduce_rows(cost_matrix))
        ax1.set_title("4. Покрытие линиями")
        ax1.imshow(reduced, cmap="Blues")
        for i in range(3):
            for j in range(3):
                ax1.text(j, i, reduced[i, j], ha="center", va="center", color="red")
        draw_coverage(ax1, reduced, [0], [1])
    
    elif frame == 4:
        reduced = reduce_cols(reduce_rows(cost_matrix))
        ax1.set_title("5. Оптимальное назначение")
        ax1.imshow(reduced, cmap="Blues")
        assignment = find_assignment(reduced)
        for i, j in assignment:
            ax1.add_patch(Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor="red", lw=3))
    
    # Визуализация графа
    workers = ["A", "B", "C"]
    jobs = ["X", "Y", "Z"]
    
    for i, worker in enumerate(workers):
        ax2.scatter(0, i, s=500, c="skyblue")
        ax2.text(0, i, worker, ha="center", va="center")
    
    for j, job in enumerate(jobs):
        ax2.scatter(1, j, s=500, c="lightgreen")
        ax2.text(1, j, job, ha="center", va="center")
    
    for i in range(3):
        for j in range(3):
            ax2.plot([0, 1], [i, j], "gray", alpha=0.3)
            if frame >= 4 and (i, j) in [(0,2), (1,1)]:
                ax2.plot([0, 1], [i, j], "red", lw=2)
    
    if frame == 3:
        ax2.set_title("Покрытие в графе")
        ax2.scatter([0, 1], [2, 0], s=700, facecolors='none', edgecolors='orange', linewidths=2)

ani = FuncAnimation(fig, update, frames=5, interval=1500)
plt.tight_layout()
ani.save("hungarian_with_coverage.gif", writer="pillow", fps=1)
plt.show()