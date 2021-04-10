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
CELL_COLOR = '#eee4da'
BORDER_COLOR = '#bbada0'
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
    game.move(event.keysym)

class Game:
  def __init__(self):
    self.tile_cols = [[None for i in range(4)] for j in range(4)]
    for i, j in random.sample(PATTERNS, 2):
      self.tile_cols[j][i] = random.choice([2, 4])
    self.show_all()

  def move(self, key):
    _tile_cols = copy.copy(self.tile_cols)
    _tile_cols = self.change_direction('pre', key, _tile_cols)
    _tile_cols = self.calc(_tile_cols)
    _tile_cols = self.move_left(_tile_cols)
    _tile_cols = self.change_direction('next', key, _tile_cols)

    if _tile_cols != self.tile_cols:
      _tile_cols = self.append_number(_tile_cols)
      self.tile_cols = _tile_cols
      self.show_all()

  def is_empty(self, pair, tile_cols):
    return tile_cols[pair[1]][pair[0]] == None

  def append_number(self, tile_cols):
    empty_tile_cols = list(filter(lambda pair: self.is_empty(pair, tile_cols), list(PATTERNS)))
    append_pos = random.choice(empty_tile_cols)
    tile_cols[append_pos[1]][append_pos[0]] = random.choice([2, 4])
    return tile_cols
    
  def change_direction(self, stage, direction, tile_cols):
    if (CHANGE_MAP[direction][stage] == 'right_rotate'):
      return self.rotate(tile_cols, is_right=True)
    elif (CHANGE_MAP[direction][stage] == 'left_rotate'):
      return self.rotate(tile_cols, is_right=False)
    elif (CHANGE_MAP[direction][stage] == 'reverse'):
      return self.reverse(tile_cols)
    else:
      return tile_cols

  def rotate(self, tile_cols, is_right=True):
    _tile_cols = [[None for i in range(4)] for j in range(4)]
    for i in range(len(tile_cols)):
      for j in range(len(tile_cols[0])):
        if is_right:
          _tile_cols[i][len(tile_cols) - 1 - j] = tile_cols[j][i]
        else:
          _tile_cols[len(tile_cols) - 1 - i][j] = tile_cols[j][i]
    return _tile_cols

  def reverse(self, tile_cols):
    return list(map(lambda ele: self.reverse_item(ele) , tile_cols))

  def reverse_item(self, tile_cols):
    _tile_cols = copy.copy(tile_cols)
    _tile_cols.reverse()
    return _tile_cols

  def move_left(self, tile_cols):
    _tile_cols = []
    for ele in tile_cols:
      cnt = ele.count(None)
      list_a_filtered = [x for x in ele if x] + [None for i in range(cnt)]
      _tile_cols.append(list_a_filtered)
    return _tile_cols

  def calc(self, tile_cols):
    return list(map(lambda ele: self.calc_ele(ele), tile_cols))
  
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
        if self.tile_cols[j][i] != None:
          self.set_number(self.tile_cols[j][i], i, j)

  def set_number(self, num, x, y):
    center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
    center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2
    font_size = round(30 + 40 / len(str(num)))
    canvas.create_text(center_x, center_y, text=num, justify="center", font=("", font_size), tag="count_text")
  
def play():
  global canvas
  global game
  root, canvas = create_canvas()
  set_field()
  game = Game()
  root.bind("<Key>", lambda event: operate(event))
  root.mainloop()

play()
