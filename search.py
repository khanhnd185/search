import abc

class Node():
  def __init__(self, state, parent, action):
    self.state = state
    self.parent = parent
    self.action = action


class StackFrontier():
  def __init__(self):
    self.frontier = []

  def add(self, node):
    self.frontier.append(node)

  def contains_state(self, state):
    return any(node.state == state for node in self.frontier)

  def empty(self):
    return len(self.frontier) == 0

  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[-1]
      self.frontier = self.frontier[:-1]
      return node


class QueueFrontier(StackFrontier):

  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[0]
      self.frontier = self.frontier[1:]
      return node

class Explorer:
  def __init__(self):
    self.start    = None
    self.goal     = None

  @abc.abstractmethod
  def neighbors(self, state):
    pass

  @abc.abstractmethod
  def print(self, solution):
    pass

  @abc.abstractmethod
  def get_state_from_str(self, station):
    pass



class Search:

  def __init__(self, explorer : Explorer, frontier="queue"):

    self.explorer     = explorer
    if   frontier == "queue": self.frontier = QueueFrontier()
    elif frontier == "stack": self.frontier = StackFrontier()
    else: raise ValueError


  def solve(self, source, target):

    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    self.frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

      # If nothing left in frontier, then no path
      if self.frontier.empty():
        return None, explored

      # Choose a node from the frontier
      node = self.frontier.remove()

      # If node is the goal, then we have a solution
      if node.state == target:
        actions = []
        cells = []
        while node.parent is not None:
          actions.append(node.action)
          cells.append(node.state)
          node = node.parent
        actions.reverse()
        cells.reverse()
        return (actions, cells), explored

      # Mark node as explored
      explored.add(node.state)

      # Add neighbors to frontier
      for action, state in self.explorer.neighbors(node.state):
        if not self.frontier.contains_state(state) and state not in explored:
          child = Node(state=state, parent=node, action=action)
          self.frontier.add(child)
