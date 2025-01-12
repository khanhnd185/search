from operator import ne
import sys
import csv

from search import Search, Explorer

class Subway(Explorer):

  def __init__(self, filename):
    super().__init__()
    
    self.stations = {}
    self.lines    = {}

    # Load data
    with open(f"{filename}", encoding="utf-8") as f:
      reader = csv.DictReader(f)

      for row in reader:
        if row["line"] not in self.lines.keys():
          self.lines[row["line"]] = {
            "name"    :  row["line"],
            "stations": [row["name"]]
          }
        else:
          self.lines[row["line"]]["stations"].append(row["name"])

        if row["name"] not in self.stations.keys():
          self.stations[row["name"]] = {
            "name"   :  row["name"],
            "no"     :  row["no"  ],
            "lines"  : {row["line"]},
            "lat"    : float(row["lat"]),
            "lng"    : float(row["lng"]),
          }
        else:
          self.stations[row["name"]]["lines"].add(row["line"])


  def print(self, solution):
    if solution is None:
      print("No solution.")
    else:
      print(f"Take {len(solution[1])} stations from {self.start} to {self.goal}:")
      for line, station in zip(solution[0], solution[1]):
        print(f"  {line}: {station}")

  def neighbors(self, state):
    neighbors = []
    for line in self.stations[state]["lines"]:
      stations = self.lines[line]["stations"]
      for i, station in enumerate(stations):
        if station != state   : continue
        if i > 0              : neighbors.append((line,stations[i-1]))
        if i < len(stations)-1: neighbors.append((line,stations[i+1]))
    
    return neighbors

  def get_state_from_str(self, station):
    station = station.lower()
    if station not in self.stations.keys():
      return None
    return station

def visualize(map
  , filename
  , explored
  , solution=None
  , show_solution=True
  , show_explored=False
):
  
  import matplotlib.pyplot as plt 
  # set the title of a plot 
  plt.title("Subway map") 

  for line in map.lines.keys():
    x = [map.stations[station]["lat"] for station in map.lines[line]["stations"]]
    y = [map.stations[station]["lng"] for station in map.lines[line]["stations"]]

    # plot scatter plot with x and y data 
    plt.scatter(x, y)

    # plot with x and y data 
    plt.plot(x, y, label=line)

  plt.legend()
  plt.show()


  input("Enter to continue...")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    sys.exit("Usage: python subway.py [filename]")

  m = Subway(filename=sys.argv[1])

  m.start = m.get_state_from_str(input("Name: "))
  if m.start is None:
    sys.exit("Station not found.")
  m.goal = m.get_state_from_str(input("Name: "))
  if m.goal is None:
    sys.exit("Station not found.")
  s = Search(m)
  print("Solving...")
  solution, explored = s.solve(m.start, m.goal)
  print("States Explored:", len(explored))
  print("Solution:")
  m.print(solution)

  #visualize(m, None, None)