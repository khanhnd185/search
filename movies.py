import csv
import sys

from search import Search, Explorer

class Movies(Explorer):
  def __init__(self, directory):
    super().__init__()

    self.people   = {}
    self.movies   = {}
    self.names    = {}

    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        self.people[row["id"]] = {
          "name": row["name"],
          "birth": row["birth"],
          "movies": set()
        }
        if row["name"].lower() not in self.names:
          self.names[row["name"].lower()] = {row["id"]}
        else:
          self.names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        self.movies[row["id"]] = {
          "title": row["title"],
          "year": row["year"],
          "stars": set()
        }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
          try:
            self.people[row["person_id"]]["movies"].add(row["movie_id"])
            self.movies[row["movie_id"]]["stars"].add(row["person_id"])
          except KeyError:
              pass


  def print(self, solution):
    if solution is None:
      print("Not connected.")
    else:
      path = [(action, state) for action, state in zip(solution[0], solution[1])]
      degrees = len(path)
      print(f"{degrees} degrees of separation.")
      path = [(None, self.start)] + path
      for i in range(degrees):
        person1 = self.people[path[i][1]]["name"]
        person2 = self.people[path[i + 1][1]]["name"]
        movie = self.movies[path[i + 1][0]]["title"]
        print(f"{i + 1}: {person1} and {person2} starred in {movie}")


  def neighbors(self, state):
    movie_ids = self.people[state]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
      for person_id in self.movies[movie_id]["stars"]:
        neighbors.add((movie_id, person_id))
    return neighbors


  def get_state_from_str(self, name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(self.names.get(name.lower(), set()))
    if len(person_ids) == 0:
      return None
    elif len(person_ids) > 1:
      print(f"Which '{name}'?")
      for person_id in person_ids:
        person = self.people[person_id]
        name = person["name"]
        birth = person["birth"]
        print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
      try:
        person_id = input("Intended Person ID: ")
        if person_id in person_ids:
          return person_id
      except ValueError:
          pass
      return None
    else:
      return person_ids[0]


if __name__ == "__main__":
  if len(sys.argv) != 2:
    sys.exit("Usage: python movies.py [directory]")

  m = Movies(directory=sys.argv[1])

  m.start = m.get_state_from_str(input("Name: "))
  if m.start is None:
    sys.exit("Person not found.")
  m.goal = m.get_state_from_str(input("Name: "))
  if m.goal is None:
    sys.exit("Person not found.")

  s = Search(m)

  print("Solving...")
  solution, explored = s.solve(m.start, m.goal)
  print("States Explored:", len(explored))
  print("Solution:")
  m.print(solution)
  
