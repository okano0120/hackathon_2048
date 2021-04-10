import tkinter as tk
import math
import random
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

TILE_COLORS = ["#eee4da", "#eee1c9", "#f3b27a", "#f69664", "#f77c5f", "#f75f3b", "#edd073", "#edcc62"]
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
    game.play(event.keysym)

class Game:
  def __init__(self):
    self.tile_cols = [[None for i in range(4)] for j in range(4)]
    self.is_finish = False
    for i, j in random.sample(PATTERNS, 2):
      self.tile_cols[j][i] = random.choice([2, 4])
    self.show_all()

  def play(self, key):
    if self.is_finish:
      return None

    _tile_cols = copy.copy(self.tile_cols)
    _tile_cols = self.move(_tile_cols, key)

    if _tile_cols == self.tile_cols:
      return None

    _tile_cols = self.append_number(_tile_cols)

    if not self.get_is_changable(_tile_cols):
      self.is_finish = True

    self.tile_cols = _tile_cols
    self.show_all()

    if self.is_finish:
      self.show_result()

  def get_is_changable(self, tile_cols):
    if self.get_empty_tile_cols(tile_cols) != []:
      return True
    else:
      is_changable = False
      for change_key in list(CHANGE_MAP.keys()):
        if tile_cols != self.move(tile_cols, change_key):
          is_changable = True
      return is_changable

  def move(self, tile_cols, key):
    tile_cols = self.change_direction('pre', key, tile_cols)
    tile_cols = self.move_left(tile_cols)
    tile_cols = self.change_direction('next', key, tile_cols)
    return tile_cols

  def is_empty(self, pair, tile_cols):
    return tile_cols[pair[1]][pair[0]] == None

  def append_number(self, tile_cols):
    empty_tile_cols = self.get_empty_tile_cols(tile_cols)
    if empty_tile_cols == []:
      return tile_cols

    append_pos = random.choice(empty_tile_cols)
    tile_cols[append_pos[1]][append_pos[0]] = random.choice([2, 4])
    return tile_cols

  def get_empty_tile_cols(self, tile_cols):
    return list(filter(lambda pair: self.is_empty(pair, tile_cols), list(PATTERNS)))
    
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
    return list(map(lambda tiles: self.reverse_item(tiles) , tile_cols))

  def reverse_item(self, tile_cols):
    _tile_cols = copy.copy(tile_cols)
    _tile_cols.reverse()
    return _tile_cols

  def move_left(self, tile_cols):
    return list(map(lambda tiles: self.calc_tiles(tiles), tile_cols))
  
  def calc_tiles(self, tiles):
    _tiles, null_count = self.sort_tiles(copy.copy(tiles))
    i = 0
    while(i + 1 < len(_tiles)):
      if _tiles[i] == _tiles[i + 1]:
        _tiles[i], _tiles[i + 1] = _tiles[i] * 2, None
        i += 1
      i += 1
    _tiles, null_count = self.sort_tiles(_tiles, null_count=null_count)
    return _tiles + [None for i in range(null_count)]

  def sort_tiles(self, tiles, null_count=0):
    null_count += tiles.count(None)
    _tiles = [tiles for tiles in tiles if tiles]
    return _tiles, null_count

  def show_all(self):
    canvas.delete("count_text")
    for i, j in PATTERNS:
      if self.tile_cols[j][i] != None:
        self.set_number(self.tile_cols[j][i], i, j)

  def set_number(self, num, x, y):
    center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
    center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2
    font_size = round(40 + 30 / len(str(num)))
    font_color, bk_color = self.get_color(num)
    canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill=bk_color, width=0, tag="count_text")
    canvas.create_text(center_x, center_y, text=num, justify="center", font=("", font_size), tag="count_text", fill = font_color)

  def show_result(self):
    canvas.create_text(POSITION["x"] + LENGTH / 2, POSITION["y"] + LENGTH / 2, text="game over", justify="center", font=("", 70), tag="gameover", fill="#776e65")

  def get_color(self, num):
    font_color, bk_color = "#ffffff", TILE_COLORS[-1]
    if (round(math.log2(num)) - 1) < len(TILE_COLORS):
      bk_color = TILE_COLORS[(round(math.log2(num)) - 1)]
    if num <= 4:
      font_color = "#776e65"
    return font_color, bk_color
  
def play():
  global canvas
  global game
  root, canvas = create_canvas()
  set_field()
  game = Game()
  root.bind("<Key>", lambda event: operate(event))
  root.mainloop()

play()
