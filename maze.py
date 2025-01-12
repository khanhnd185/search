import sys

from search import Search, Explorer

class Maze(Explorer):

  def __init__(self, filename):
    super().__init__()

    # Read file and set height and width of maze
    with open(filename) as f:
      contents = f.read()

    # Validate start and goal
    if contents.count("A") != 1:
      raise Exception("maze must have exactly one start point")
    if contents.count("B") != 1:
      raise Exception("maze must have exactly one goal")

    # Determine height and width of maze
    contents = contents.splitlines()
    self.height = len(contents)
    self.width = max(len(line) for line in contents)

    # Keep track of walls
    self.walls = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        try:
          if contents[i][j] == "A":
            
            self.start = (i, j)
            row.append(False)
          elif contents[i][j] == "B":
            self.goal = (i, j)
            row.append(False)
          elif contents[i][j] == " ":
            row.append(False)
          else:
            row.append(True)
        except IndexError:
          row.append(False)
      self.walls.append(row)


  def print(self, solution):
    states = solution[1] if solution is not None else None
    print()
    for i, row in enumerate(self.walls):
      for j, col in enumerate(row):
        if col:
          print("█", end="")
        elif (i, j) == self.start:
          print("A", end="")
        elif (i, j) == self.goal:
          print("B", end="")
        elif states is not None and (i, j) in states:
          print("*", end="")
        else:
          print(" ", end="")
      print()
    print()


  def neighbors(self, state):
    row, col = state
    candidates = [
      ("up", (row - 1, col)),
      ("down", (row + 1, col)),
      ("left", (row, col - 1)),
      ("right", (row, col + 1))
    ]

    result = []
    for action, (r, c) in candidates:
      if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
        result.append((action, (r, c)))
    return result

  def get_state_from_str(self, coordinate):
    ret = coordinate.split(",")

    if len(ret) != 2:
      return None

    try:
      r = float(ret[0])
      c = float(ret[1])
      if 0 <= r < self.height and 0 <= c < self.width:
        return r,c
    except:
      pass
    return None
      

def visualize(maze
  , filename
  , explored
  , solution=None
  , show_solution=True
  , show_explored=False
):
  from PIL import Image, ImageDraw
  cell_size = 50
  cell_border = 2

  # Create a blank canvas
  img = Image.new(
    "RGBA",
    (maze.width * cell_size, maze.height * cell_size),
    "black"
  )
  draw = ImageDraw.Draw(img)

  states = solution[1] if solution is not None else None
  for i, row in enumerate(maze.walls):
    for j, col in enumerate(row):

      # Walls
      if col:
        fill = (40, 40, 40)

      # Start
      elif (i, j) == maze.start:
        fill = (255, 0, 0)

      # Goal
      elif (i, j) == maze.goal:
        fill = (0, 171, 28)

      # Solution
      elif states is not None and show_solution and (i, j) in states:
        fill = (220, 235, 113)

      # Explored
      elif states is not None and show_explored and (i, j) in explored:
        fill = (212, 97, 85)

      # Empty cell
      else:
        fill = (237, 240, 252)

      # Draw cell
      draw.rectangle(
        ([(j * cell_size + cell_border, i * cell_size + cell_border),
          ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
        fill=fill
      )

  img.save(filename)


if __name__=="__main__":
  if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py data/mazes/maze1.txt")

  m = Maze(sys.argv[1])
  s = Search(m)
  print("Maze:")
  m.print(None)
  print("Solving...")
  solution, explored = s.solve(m.start, m.goal)
  print("States Explored:", len(explored))
  print("Solution:")
  m.print(solution)
  visualize(m, "maze.png", explored, solution, show_explored=True)
