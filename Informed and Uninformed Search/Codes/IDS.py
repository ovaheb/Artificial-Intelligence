import copy
import time
dx = [ 0, 1, 0, -1]
dy = [ 1, 0, -1, 0]
def list_to_string(l):
  result = ""
  for i in l:
    for j in i:
      result += j
  return result
def is_goal(state):
  for temp in state.cmap:
    if 'P' in temp:
      return False
  return True
def find_ambulance(state):
  for row in state.cmap:
    if 'A' in row:
      return row.index('A'),state.cmap.index(row)
class State(object):
  def __init__(self, _map, _moves, oh):
    self.cmap = _map
    self.moves = _moves
    self.over_hospital = oh
  def cpy(self):
    new_cmap = []
    for row in self.cmap:
      temp = []
      for i in row:
        temp.append(i)
      new_cmap.append(temp)
    return State(new_cmap, copy.deepcopy(self.moves), copy.deepcopy(self.over_hospital))
def ids(explored, frontiers, node):
  total_states = 1
  total_unique_states = 1
  n = len(node.cmap)
  m = len(node.cmap[0])
  length = -1
  while True:
    frontiers = []
    frontiers.append(node)
    explored = set()
    length += 1
    while(frontiers):
      exploring = frontiers.pop(0)
      if exploring.moves>=length:
        continue
##      print("Length is :", length, "Moves are :", exploring.moves)
##      for row in exploring.cmap:
##        print(row)
      ax,ay = find_ambulance(exploring)
      explored.add(hash(list_to_string(exploring.cmap) + chr(exploring.moves)))
      sides = [0, 0, 0, 0]
      for k in range(4):
        new_ax = ax + dx[k]
        new_ay = ay + dy[k]
        if not (new_ax==0 or new_ay==0 or new_ax==(m-1) or new_ay==(n-1)) \
        and (exploring.cmap[new_ay][new_ax]==' ' or (exploring.cmap[new_ay][new_ax]=='P' \
        and not (exploring.cmap[new_ay + dy[k]][new_ax + dx[k]]=='P' or \
        exploring.cmap[new_ay + dy[k]][new_ax + dx[k]]=='#'))):
          sides[k] = 1
      sum = sides[0] + sides[1] + sides[2] + sides[3]
      for k in range(4):
        if sides[k]:
          new_ax = ax + dx[k]
          new_ay = ay + dy[k]
          total_states += 1
          neighbour = exploring.cpy()
          neighbour.moves += 1
          if not neighbour.over_hospital=='0':
            neighbour.cmap[ay][ax] = neighbour.over_hospital
            neighbour.over_hospital = '0'
          else:
            neighbour.cmap[ay][ax] = ' '
          if neighbour.cmap[new_ay][new_ax]==' ' :
            neighbour.cmap[new_ay][new_ax] = 'A'
          elif neighbour.cmap[new_ay][new_ax]=='P':
            if neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]]==' ':
              neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]] = 'P'
              neighbour.cmap[new_ay][new_ax] = 'A'
            else:
              neighbour.cmap[new_ay][new_ax] = 'A'
              if (ord(neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]])-48)==1:
                neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]] = ' '
              else:
                neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]] = chr(ord(neighbour.cmap[new_ay + dy[k]][new_ax + dx[k]])-1)
          else:
            neighbour.oh = neighbour.cmap[new_ay][new_ax]
            neighbour.cmap[new_ay][new_ax] = ' '
          if hash(list_to_string(neighbour.cmap) + chr(neighbour.moves)) not in explored:
            total_unique_states += 1
            frontiers.insert(0, neighbour)
          if is_goal(neighbour):
            return neighbour.moves, total_states, total_unique_states
  return -1, total_states, total_unique_states
filename = input("Please enter name of input file: ")
start_time = time.time()
file = open(filename, "r")
model = list(file.readlines())
model = list(map(lambda s: s.strip(), model))
for i in range(len(model)):
  model[i] = list(model[i])
frontiers = []
explored = set()
sol_distance, total_states, total_unique_states = ids(explored, frontiers, State(model, 0, '0'))
print("--- %s seconds ---" % (time.time() - start_time))
if sol_distance==-1:
  print("No answer")
else:
  print("You need", sol_distance, "moves for goal")
print("Number of states seen:", total_states)
print("Number of unique states seen:", total_unique_states)






