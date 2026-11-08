"""
Визуализация работы алгоритма A* на сетке с препятствиями.
Сохраняет анимацию в images/astar_demo.gif.
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

from astar import Node, astar

# --- 1. Создаём сетку 20x20 ---
ROWS, COLS = 20, 20
grid = [[Node(x, y, walkable=True) for y in range(COLS)] for x in range(ROWS)]

# Добавляем препятствия (стену)
obstacles = [
    # Вертикальная стена с проходами
    (x, 10) for x in range(2, 18) if x not in (5, 14)
]
# Горизонтальный "забор"
obstacles += [(12, y) for y in range(15, 20)]

for (x, y) in obstacles:
    grid[x][y].walkable = False

# Старт и финиш
start = grid[0][0]
goal = grid[19][19]

# --- 2. Запускаем A* ---
path, visited, history = astar(grid, start, goal)

if path is None:
    print("Путь не найден!")
    exit()

print(f"Путь найден, длина: {len(path)}")
print(f"Посещено узлов: {len(visited)}")

# --- 3. Функция для отрисовки одного кадра ---
def draw_frame(step, fig, ax, last_frame=False):
    ax.clear()
    # Сетка
    ax.set_xlim(-0.5, COLS - 0.5)
    ax.set_ylim(ROWS - 0.5, -0.5)
    ax.set_xticks(np.arange(0, COLS, 1))
    ax.set_yticks(np.arange(0, ROWS, 1))
    ax.grid(True, color='lightgray', linewidth=0.5)
    ax.set_aspect('equal')

    # Препятствия (чёрные)
    for (x, y) in obstacles:
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='black'))

    # Закрытые узлы (серые)
    closed = history[step]['closed']
    for (x, y) in closed:
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='#CCCCCC', alpha=0.6))

    # Открытые узлы (оранжевые)
    open_list = history[step]['open']
    for (x, y) in open_list:
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='#FFA500', alpha=0.7))

    # Текущий узел (жёлтый)
    (cx, cy) = history[step]['current']
    ax.add_patch(plt.Rectangle((cy - 0.5, cx - 0.5), 1, 1, color='yellow'))

    # Старт (зелёный) и финиш (красный)
    ax.add_patch(plt.Circle((start.y, start.x), 0.35, color='green', zorder=5))
    ax.add_patch(plt.Circle((goal.y, goal.x), 0.35, color='red', zorder=5))

    # Финальный путь (синий)
    if last_frame:
        for (x, y) in path:
            ax.add_patch(plt.Rectangle((y - 0.4, x - 0.4), 0.8, 0.8, color='#1f77b4', alpha=0.8))
        ax.set_title('A*: путь найден', fontsize=14)
    else:
        ax.set_title(f'A*: шаг {step + 1} из {len(history)}', fontsize=14)

    ax.set_xticklabels([])
    ax.set_yticklabels([])


# --- 4. Рисуем и сохраняем GIF ---
os.makedirs('images', exist_ok=True)
frames = []

# Уменьшаем количество кадров (каждый 3-й), чтобы GIF не был огромным
step_indices = list(range(0, len(history), 3)) + [len(history) - 1]

for i, step in enumerate(step_indices):
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_frame(step, fig, ax, last_frame=(step == len(history) - 1))
    fig.tight_layout()

    # Сохраняем во временный PNG
    tmp_path = f'images/tmp_{i:03d}.png'
    fig.savefig(tmp_path, dpi=80)
    frames.append(imageio.imread(tmp_path))
    plt.close(fig)

# Собираем GIF
gif_path = 'images/astar_demo.gif'
imageio.mimsave(gif_path, frames, duration=0.15)
print(f"GIF сохранён: {gif_path}")

# Удаляем временные PNG
for i in range(len(step_indices)):
    os.remove(f'images/tmp_{i:03d}.png')

# --- 5. Отдельный финальный PNG для README ---
fig, ax = plt.subplots(figsize=(8, 8))
draw_frame(len(history) - 1, fig, ax, last_frame=True)
fig.tight_layout()
png_path = 'images/astar_result.png'
fig.savefig(png_path, dpi=100)
plt.close(fig)
print(f"Финальная картинка сохранена: {png_path}")
