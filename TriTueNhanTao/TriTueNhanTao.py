import heapq
import math
import time
from typing import List, Tuple, Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SIZE = 50
MIN_HEIGHT = 0
MAX_HEIGHT = 1000
START = (0, 0)
GOAL = (SIZE - 1, SIZE - 1)


def generate_terrain(size: int = SIZE, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, size)
    y = np.linspace(0, 1, size)
    X, Y = np.meshgrid(x, y)

    base = (
        250
        + 180 * np.sin(2 * np.pi * X)
        + 140 * np.cos(3 * np.pi * Y)
        + 90 * np.sin(4 * np.pi * (X + Y))
    )
    noise = rng.normal(0, 80, size=(size, size))
    terrain = base + noise
    return np.clip(terrain, MIN_HEIGHT, MAX_HEIGHT).astype(float)


def move_cost(terrain: np.ndarray, current: Tuple[int, int], nxt: Tuple[int, int]) -> float:
    curr_h = terrain[current]
    next_h = terrain[nxt]
    diff = abs(next_h - curr_h)
    if next_h > curr_h:
        return diff * 2.0
    if next_h < curr_h:
        return diff * 0.5
    return 1.0


def neighbors(pos: Tuple[int, int], size: int) -> List[Tuple[int, int]]:
    r, c = pos
    results = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                results.append((nr, nc))
    return results


def heuristic_euclidean(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    r, c = pos
    gr, gc = goal
    return math.hypot(gr - r, gc - c)


def heuristic_manhattan(pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
    r, c = pos
    gr, gc = goal
    return abs(gr - r) + abs(gc - c)


def heuristic_custom(pos: Tuple[int, int], goal: Tuple[int, int], terrain: np.ndarray) -> float:
    r, c = pos
    gr, gc = goal
    horizontal = math.hypot(gr - r, gc - c)
    vertical_gap = abs(terrain[gr, gc] - terrain[r, c])
    return max(0.5 * horizontal, 0.5 * vertical_gap)


def astar(
    terrain: np.ndarray,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic_name: str,
) -> Dict[str, object]:
    start_time = time.perf_counter()
    open_heap: List[Tuple[float, float, int, int, int]] = []
    counter = 0
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    closed: set = set()

    def h(pos: Tuple[int, int]) -> float:
        if heuristic_name == "euclidean":
            return heuristic_euclidean(pos, goal)
        if heuristic_name == "manhattan":
            return heuristic_manhattan(pos, goal)
        return heuristic_custom(pos, goal, terrain)

    heapq.heappush(open_heap, (h(start), 0.0, counter, start[0], start[1]))

    expanded = 0
    while open_heap:
        f_cost, g_cost, _, r, c = heapq.heappop(open_heap)
        pos = (r, c)
        if pos in closed:
            continue
        if g_cost != g_score.get(pos, float("inf")):
            continue
        if pos == goal:
            path = []
            cur = pos
            while cur in parent:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            total_cost = 0.0
            for i in range(1, len(path)):
                total_cost += move_cost(terrain, path[i - 1], path[i])
            elapsed = time.perf_counter() - start_time
            return {
                "name": heuristic_name,
                "path": path,
                "cost": total_cost,
                "expanded": expanded,
                "time": elapsed,
                "steps": len(path) - 1,
            }

        closed.add(pos)
        expanded += 1
        for nxt in neighbors(pos, terrain.shape[0]):
            if nxt in closed:
                continue
            new_g = g_score.get(pos, float("inf")) + move_cost(terrain, pos, nxt)
            if new_g < g_score.get(nxt, float("inf")):
                g_score[nxt] = new_g
                parent[nxt] = pos
                counter += 1
                heapq.heappush(open_heap, (new_g + h(nxt), new_g, counter, nxt[0], nxt[1]))

    return {
        "name": heuristic_name,
        "path": [],
        "cost": float("inf"),
        "expanded": expanded,
        "time": time.perf_counter() - start_time,
        "steps": 0,
    }


def plot_results(terrain: np.ndarray, results: List[Dict[str, object]]) -> None:
    cmap = plt.get_cmap("coolwarm")
    fig = plt.figure(figsize=(16, 8))

    ax1 = fig.add_subplot(121)
    img = ax1.imshow(terrain, cmap=cmap, origin="lower")
    fig.colorbar(img, ax=ax1, label="Độ cao (m)")
    ax1.set_title("Bản đồ địa hình và đường đi")
    ax1.set_xlabel("Cột")
    ax1.set_ylabel("Hàng")

    ax1.scatter(START[1], START[0], color="green", s=90, label="Start")
    ax1.scatter(GOAL[1], GOAL[0], color="black", s=90, label="Goal")

    colors = ["red", "lime", "blue"]
    for result, color in zip(results, colors):
        path = result["path"]
        if not path:
            continue
        rows = [p[0] for p in path]
        cols = [p[1] for p in path]
        ax1.plot(cols, rows, color=color, linewidth=1.8, label=result["name"])
        ax1.scatter(cols[-1], rows[-1], color=color, s=50)
    ax1.legend()

    ax2 = fig.add_subplot(122, projection="3d")
    rows, cols = np.indices(terrain.shape)
    ax2.plot_surface(rows, cols, terrain, cmap=cmap, alpha=0.85, edgecolor="none")
    ax2.set_title("Mô hình 3D của địa hình")
    ax2.set_xlabel("Hàng")
    ax2.set_ylabel("Cột")
    ax2.set_zlabel("Độ cao (m)")

    for result, color in zip(results, colors):
        path = result["path"]
        if not path:
            continue
        rows_path = [p[0] for p in path]
        cols_path = [p[1] for p in path]
        heights = [terrain[r, c] for r, c in path]
        ax2.plot(rows_path, cols_path, heights, color=color, linewidth=1.5)

    plt.tight_layout()
    plt.savefig("terrain_paths.png", dpi=220)
    plt.close(fig)


def print_summary(results: List[Dict[str, object]]) -> None:
    print("\nKết quả so sánh các heuristic")
    print("-" * 90)
    print(f"{'Heuristic':<15} {'Chi phí':<12} {'Số bước':<10} {'Số nút mở rộng':<16} {'Thời gian (s)':<14}")
    print("-" * 90)
    for result in results:
        print(
            f"{result['name']:<15} {result['cost']:>10.2f} {result['steps']:>8} {result['expanded']:>16} {result['time']:>14.6f}"
        )
    best_cost = min(results, key=lambda item: item["cost"])
    fastest = min(results, key=lambda item: item["time"])
    least_expanded = min(results, key=lambda item: item["expanded"])
    print("-" * 90)
    print(f"Tiết kiệm năng lượng nhất: {best_cost['name']} (chi phí {best_cost['cost']:.2f})")
    print(f"Nhanh nhất: {fastest['name']} ({fastest['time']:.6f}s)")
    print(f"Cân bằng tốt nhất: {least_expanded['name']} ({least_expanded['expanded']} nút mở rộng)")


def main() -> None:
    terrain = generate_terrain()
    results = []
    for name in ["euclidean", "manhattan", "custom"]:
        result = astar(terrain, START, GOAL, name)
        results.append(result)

    print_summary(results)
    plot_results(terrain, results)
    print("\nĐã lưu hình minh họa vào terrain_paths.png")


if __name__ == "__main__":
    main()
