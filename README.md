# MazeSolver
Python program to solve mazes using A* algorithm

This Python program solves a 2D maze image using the A* pathfinding algorithm. It parses the maze from an input image, identifies the shortest path from the entrance to the exit, and marks the solution path in red on the output image.

## Features
- Automatically crops extra whitespace around the maze.
- Finds the shortest path using the A* algorithm.
- Marks the solution path in red on the maze image.
- Accepts custom input and output paths via command-line arguments.
- Provides error handling for invalid inputs or unsolvable mazes.

## Requirements
- Python 3.6 or higher
- The following Python libraries:
  - `Pillow`
  - `NumPy`

You can install the required libraries with:
```bash
pip install pillow numpy
```

## Usage

### Command-Line Arguments
The program takes two arguments:
1. **Input Image Path**: Path to the maze image file (e.g., `maze.png`).
2. **Output Image Path**: Path where the solved maze image will be saved (e.g., `solved_maze.png`).

### Run the Program
```bash
python3 solve_maze.py <input_image> <output_image>
```

#### Example:
```bash
python3 solve_maze.py maze.png solved_maze.png
```

### Input Maze Image
- The maze image should have black walls and white paths.
- It can be in `.png`, `.jpg`, or other common image formats.
- Ensure the entrance is at the top of the maze and the exit is at the bottom.

### Output Solved Maze
- The solved maze will have the path marked in red and saved to the specified output path.

## Program Workflow
1. **Load and Parse**:
   - The input image is converted to grayscale and binarized (1 for paths, 0 for walls).
   - Extra whitespace around the maze is cropped.
2. **Pathfinding**:
   - The A* algorithm is used to calculate the shortest path from the entrance to the exit.
3. **Visualization**:
   - The solution path is overlaid on the maze image in red.
4. **Save Output**:
   - The solved maze is saved to the specified output file.


## Error Handling
The program provides the following error messages for invalid inputs:
- "Input file does not exist" if the input path is incorrect.
- "Could not find valid start or goal positions" if the maze does not have a proper entrance or exit.
- "No path found from start to goal" if the maze is unsolvable.

---
