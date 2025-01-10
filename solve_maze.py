#!/usr/bin/env python3

import argparse
from PIL import Image
import numpy as np
import heapq
import os


def crop_whitespace_from_grid(grid):
    row_proportions = np.mean(grid == 1, axis=1)
    col_proportions = np.mean(grid == 1, axis=0)

    valid_rows = np.where(row_proportions < 0.9)[0]
    valid_cols = np.where(col_proportions < 0.9)[0]

    if len(valid_rows) == 0 or len(valid_cols) == 0:
        raise ValueError("The maze seems to be empty or invalid. Please check the input image.")

    cropped_grid = grid[valid_rows.min():valid_rows.max() + 1, valid_cols.min():valid_cols.max() + 1]
    return cropped_grid


def get_neighbors(pos, maze):
    rows, cols = maze.shape
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    for d in directions:
        neighbor = (pos[0] + d[0], pos[1] + d[1])
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor] == 1:
            neighbors.append(neighbor)
    return neighbors


def astar(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, maze):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    raise ValueError("No path found from start to goal.")


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path[::-1]


def mark_red_path(maze, path):
    rgb_maze = np.stack((maze * 255,) * 3, axis=-1).astype(np.uint8)
    for pos in path:
        rgb_maze[pos[0], pos[1]] = [255, 0, 0]  # Red color
    return rgb_maze


def main():
    parser = argparse.ArgumentParser(description="Solve a maze image and mark the path in red.")
    parser.add_argument("input", help="Path to the input maze image.")
    parser.add_argument("output", help="Path to save the solved maze image.")
    args = parser.parse_args()

    # Load the maze image
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    try:
        im = Image.open(args.input).convert('L')
    except Exception as e:
        print(f"Error: Could not open the image. {e}")
        return

    # Convert image to binary
    binary = im.point(lambda p: 1 if p > 128 else 0)
    binary = np.array(binary)

    try:
        cropped_nim = crop_whitespace_from_grid(binary)
    except ValueError as e:
        print(f"Error: {e}")
        return

    h, w = cropped_nim.shape
    print(f"Cropped maze dimensions: {h}x{w}")

    # Define start and goal positions
    try:
        start = (0, np.where(cropped_nim[0] == 1)[0][2])  # First row, first walkable column
        goal = (h - 1, np.where(cropped_nim[-1] == 1)[0][2])  # Last row, first walkable column
    except IndexError:
        print("Error: Could not find valid start or goal positions in the maze.")
        return

    # Solve the maze
    try:
        path = astar(cropped_nim, start, goal)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Mark the path in red
    marked_maze = mark_red_path(cropped_nim, path)

    # Save the solved maze
    try:
        solved_image = Image.fromarray(marked_maze)
        solved_image.save(args.output)
        print(f"Solved maze saved to '{args.output}'.")
    except Exception as e:
        print(f"Error: Could not save the solved maze. {e}")


if __name__ == "__main__":
    main()
