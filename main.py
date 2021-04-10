import tkinter as tk
import math
import random
import itertools
import copy

canvas = None
game = None

CHANGE_MAP = {
  "Left": {
    "pre": '',
    "next": '' 
  },
  "Up": {
    "pre": 'left_rotate',
    "next": 'right_rotate'
  },
  "Right": {
    "pre": 'reverse',
    "next": 'reverse'
  },
  "Down": {
    "pre": 'right_rotate',
    "next": 'left_rotate'
  },
}

SQUARE_LENGTH = 100
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 8
NUMBER = 4
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
CELL_COLOR = '#cbbeb5'
BORDER_COLOR = '#b2a698'
PATTERNS = [[i, j] for i in range(4) for j in range(4)]

def set_field():
  canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"], LENGTH + POSITION["y"], fill='#cbbeb5', width=BORDER_WIDTH, outline=BORDER_COLOR)

  for i in range(NUMBER - 1):
    x = POSITION["x"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    y = POSITION["y"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    canvas.create_line(x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH, fill=BORDER_COLOR)
    canvas.create_line(POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH, fill=BORDER_COLOR)

def create_canvas():
  root = tk.Tk()
  root.geometry(f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
  root.title("2048")
  canvas = tk.Canvas(root, width=(LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
  canvas.place(x=0, y=0)

  return root, canvas

def operate(event):
  if event.keysym in list(CHANGE_MAP.keys()):
    game.change_array(event.keysym)

class Game:
  def __init__(self):
    self.array = [[None for i in range(4)] for j in range(4)]
    for i, j in random.sample(PATTERNS, 2):
      self.array[j][i] = random.choice([2, 4])
    self.show_all()

  def create_sample(self):
    self.array[2][1] = 8
    self.array[3][1] = 4
    self.array[3][2] = 4
    self.array[2][3] = 8
    self.array[3][3] = 4 
    self.array[3][0] = 4 

  def change_array(self, key):
    _array = copy.copy(self.array)
    _array = self.change_direction('pre', key, _array)
    _array = self.calc(_array)
    _array = self.move_left(_array)
    _array = self.change_direction('next', key, _array)
    print("step")
    print(_array)
    print(self.array)
    if _array != self.array:
      _array = self.append_number(_array)
      self.array = _array
      self.show_all()

  def is_empty(self, pair, array):
    print(pair)
    return array[pair[1]][pair[0]] == None

  def append_number(self, array):
    print(self.array)
    empty_array = list(filter(lambda pair: self.is_empty(pair, array), list(PATTERNS)))
    print(empty_array)
    append_pos = random.choice(empty_array)
    array[append_pos[1]][append_pos[0]] = random.choice([2, 4])
    return array
    

  def change_direction(self, stage, direction, array):
    if (CHANGE_MAP[direction][stage] == 'right_rotate'):
      return self.rotate(array, is_right=True)
    elif (CHANGE_MAP[direction][stage] == 'left_rotate'):
      return self.rotate(array, is_right=False)
    elif (CHANGE_MAP[direction][stage] == 'reverse'):
      return self.reverse(array)
    else:
      return array

  def rotate(self, array, is_right=True):
    _array = [[None for i in range(4)] for j in range(4)]
    for i in range(len(array)):
      for j in range(len(array[0])):
        if is_right:
          _array[i][len(array) - 1 - j] = array[j][i]
        else:
          _array[len(array) - 1 - i][j] = array[j][i]
    return _array

  def reverse(self, array):
    return list(map(lambda ele: self.reverse_item(ele) , array))

  def reverse_item(self, array):
    _array = copy.copy(array)
    _array.reverse()
    return _array

  def move_left(self, array):
    _array = []
    for ele in array:
      cnt = ele.count(None)
      list_a_filtered = [x for x in ele if x] + [None for i in range(cnt)]
      _array.append(list_a_filtered)
    return _array

  def calc(self, array):
    return list(map(lambda ele: self.calc_ele(ele), array))
  
  def calc_ele(self, ele):
    cnt = ele.count(None)
    _ele = [x for x in copy.copy(ele) if x]
  
    i = 0
    while(i + 1 < len(_ele)):
      if _ele[i] == _ele[i + 1]:
        _ele[i], _ele[i + 1] = _ele[i] * 2, None
        i += 1
      i += 1
    return _ele + [None for i in range(cnt)]

  def show_all(self):
    canvas.delete("count_text")
    for i in range(4):
      for j in range(4):
        if self.array[j][i] != None:
          self.set_number(self.array[j][i], i, j)

  def set_number(self, num, x, y):
    print(num, x, y)
    center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
    center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2
    canvas.create_text(center_x, center_y, text=num, justify="center", font=("", 70), tag="count_text")
  
def play():
  global canvas
  global game
  root, canvas = create_canvas()
  set_field()
  game = Game()
  root.bind("<Key>", lambda event: operate(event))
  root.mainloop()

play()
