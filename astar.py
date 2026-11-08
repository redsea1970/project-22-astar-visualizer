"""
Учебный проект: визуализация алгоритма A*.
Pet-project по алгоритмам поиска пути.

Алгоритм A* ищет кратчайший путь на сетке с препятствиями,
используя эвристику (манхэттенское расстояние).
"""
import heapq


class Node:
    """Узел сетки."""
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        # Стоимость пути от старта до узла (g), эвристика (h), сумма (f = g + h)
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None

    def __lt__(self, other):
        # Для работы heapq: сравнение по f, при равенстве — по h
        return (self.f, self.h) < (other.f, other.h)


def heuristic(a, b):
    """Манхэттенское расстояние (для сетки без диагоналей)."""
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_neighbors(grid, node):
    """Возвращает проходимых соседей (4-связность: вверх/вниз/влево/вправо)."""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])
    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny].walkable:
            neighbors.append(grid[nx][ny])
    return neighbors


def astar(grid, start, goal):
    """
    Возвращает:
    - path: список узлов от start до goal (включая оба конца) или None, если путь не найден
    - visited: множество посещённых узлов (для визуализации)
    - history: список снимков состояния (открытый/закрытый списки) для анимации
    """
    start.g = 0
    start.f = heuristic(start, goal)
    open_set = [start]
    closed_set = set()
    # Для отслеживания, был ли узел уже добавлен в open_set
    open_set_hash = {start}

    history = []

    while open_set:
        current = heapq.heappop(open_set)
        open_set_hash.discard(current)

        # Сохраняем снимок для анимации
        history.append({
            'current': (current.x, current.y),
            'open': [(n.x, n.y) for n in open_set],
            'closed': [(n.x, n.y) for n in closed_set],
            'path': reconstruct_path(current),
        })

        if current is goal:
            path = reconstruct_path(goal)
            return path, closed_set, history

        closed_set.add(current)

        for neighbor in get_neighbors(grid, current):
            if neighbor in closed_set:
                continue
            tentative_g = current.g + 1  # стоимость перехода = 1

            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, neighbor)
                    open_set_hash.add(neighbor)

    return None, closed_set, history


def reconstruct_path(node):
    """Восстанавливает путь от текущего узла до старта."""
    path = []
    while node is not None:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]
