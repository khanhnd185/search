import sys

from search import Search, Explorer

class Tile(Explorer):

  def __init__(self, filename):
    super().__init__()

    # Read file and set height and width of maze
    with open(filename) as f:
      contents = f.read()
      
    contents = contents.splitlines()
    n = len(contents)

    self.start = []
    self.empty = [-1,-1]
    flatten    = []
    for row, content in enumerate(contents):
      tiles = content.split(",")
      if len(tiles) != n:
        raise Exception("Only square tile accepted")

      line = []
      for col, val in enumerate(tiles):
        if val == "x":
          v = 0
          self.empty = [row, col]
        else: v = int(val)
        
        if v < 0 or v >= n*n or v in flatten:
          raise ValueError("Number in wrong")
        else:
          line.append(v)
          flatten.append(v)

      self.start.append(line)

    self.goal = []
    for row in range(n):
      line = []
      for col in range(n): line.append(row*n+col+1)
      self.goal.append(line)
    self.goal[n-1][n-1] = 0



  def neighbors(self, state):

    result = []

    return result
  

def visualize(tile
  , filename
  , explored
  , solution=None
  , show_solution=True
  , show_explored=False
):
  def print_tile(tile):
    n = len(tile)
    for row in range(n):
      print("+-"*n+"+")
      for col in range(n):
        print("|"+str(tile[row][col]),end="")
      print("|")
    print("+-"*n+"+")
    print()

  print_tile(tile.start)
  print_tile(tile.goal)

if __name__=="__main__":
  if len(sys.argv) != 2:
    sys.exit("Usage: python tiles.py data/tiles/tile1.txt")

  t = Tile(sys.argv[1])
  visualize(t, None, None)
