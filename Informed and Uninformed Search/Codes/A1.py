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
def find_ambulance(cmap):
  for row in cmap:
    if 'A' in row:
      return row.index('A'),cmap.index(row)
class State(object):
  def __init__(self, _map, _moves, oh, _h):
    self.cmap = _map
    self.moves = _moves
    self.over_hospital = oh
    self.heuristic = _h
  def cpy(self):
    new_cmap = []
    for row in self.cmap:
      temp = []
      for i in row:
        temp.append(i)
      new_cmap.append(temp)
    return State(new_cmap, copy.deepcopy(self.moves), copy.deepcopy(self.over_hospital), copy.deepcopy(self.heuristic))
  def seth(self, _h):
    self.heuristic = _h
def heuristic1(cmap):
  px = []
  py = []
  hx = []
  hy = []
  index = -1
  for i in range(len(cmap)):
    for j in range(len(cmap[0])):
      if cmap[i][j]=='P':
        px.append(j)
        py.append(i)
      elif cmap[i][j] not in [' ', '#', 'A',]:
        hx.append(j)
        hy.append(i)
      elif cmap[i][j]=='A':
        ax = j
        ay = i
  min_A_to_P = 1000000
  for i in range(len(px)):
    if ((abs(px[i]-ax) + abs(py[i]-ay)))<min_A_to_P:
      min_A_to_P = (abs(px[i]-ax) + abs(py[i]-ay))
      index = i
  min_P_to_H = [1000000]*len(px)
  for p_index in range(len(px)):
    for h_index in range(len(hx)):
      if (abs(px[p_index]-hx[h_index]) + abs(py[p_index]-hy[h_index]))<min_P_to_H[p_index]:
        min_P_to_H[p_index] = (abs(px[p_index]-hx[h_index]) + abs(py[p_index]-hy[h_index]))
  return sum(min_P_to_H)
def find_best_state(frontiers):
  min_h = 1000000
  index = 0
  for i in range(len(frontiers)):
    if (frontiers[i].heuristic + frontiers[i].moves)<=min_h:
      min_h = frontiers[i].heuristic + frontiers[i].moves
      index = i
  return index
def A1(explored, frontiers, node):
  frontiers.append(node)
  total_states = 1
  total_unique_states = 1
  n = len(node.cmap)
  m = len(node.cmap[0])
  while frontiers:
    best_state = find_best_state(frontiers)
    exploring = frontiers.pop(best_state)
    ax,ay = find_ambulance(exploring.cmap)
    explored.add(hash(list_to_string(exploring.cmap)))
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
        if k==3 or sum==1 or (sides[3]==0 and k==2) or (sides[3]==0 and sides[2]==0 and k==1):
          neighbour = exploring
        else:
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
        if hash(list_to_string(neighbour.cmap)) not in explored:
          total_unique_states += 1
          neighbour.seth(heuristic1(neighbour.cmap))
          frontiers.append(neighbour)
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
sol_distance, total_states, total_unique_states = A1(explored, frontiers, State(model, 0, '0', heuristic1(model)))
print("--- %s seconds ---" % (time.time() - start_time))
if sol_distance==-1:
  print("No answer")
else:
  print("You need", sol_distance, "moves for goal")
print("Number of states seen:", total_states)
print("Number of unique states seen:", total_unique_states)

    

