# https://quoridorstrats.wordpress.com/notation/
import pprint


def full_game_to_array(shorthand):
  print(shorthand)  
  count = -1
  moves = []
  for i in shorthand.split(' '):
    if i[1] == '.': 
      count += 1
      moves.append([])
    else:
      moves[count].append(i)
  print("This game has",count+1,"rounds")
  print(moves) 

def state_to_array(shorthand):
  test()
  gameOut = game(9,2)
  gameOut.get(5,1).val = 1
  gameOut.get(5,9).val = 2
  print(shorthand)
  temp = shorthand.split('/')
  temp[0]=temp[0].strip()
  for i in range(5):
    print(temp[i])
  print("["+temp[0]+"]")
  hori = [temp[0][i:i+2] for i in range(0, len(temp[0]), 2)]
  for i in hori:
    x = ord(i[0])-ord('`')
    y = int(i[1])
    gameOut.get(x,y).set_wall_h()

  gameOut.draw()
    

  


class tile:
  def __init__(self, x, y,parent):
    self.x = x
    self.y = y
    self.val = 0
    self.parent = parent
    self.w_north = False
    self.w_east = False
    self.w_south = False
    self.w_west = False
  def get_north(self):
    if self.w_north: return None
    return self.parent.get(self.x,self.y+1)
  def get_east(self): 
    if self.w_east: return None
    return self.parent.get(self.x+1,self.y)
  def get_south(self):
    if self.w_south: return None
    return self.parent.get(self.x,self.y-1)
  def get_west(self):
    if self.w_west: return None
    return self.parent.get(self.x-1,self.y)
  def get_val(self):
    if self.val == 0: return ' '
    if self.val == 1: return 'x'
    if self.val == 2: return 'o'
  def set_wall_h(self):
    print(self)
    self.get_north().w_south = True
    self.w_north = True
    self.get_east().get_north().w_south = True
    self.get_east().w_north = True
  def set_wall_v(self):
    print(self)
    self.get_north().get_east().w_west = True
    self.get_north().w_east = True
    self.get_east().w_west = True
    self.w_east = True

    

  def get_char(self):
    if self.w_north: return '﹋'+self.get_val()+'﹋' 
    if self.w_east: return ' ' + self.get_val()+'⏐'
    if self.w_south: return '﹏'+self.get_val()+'﹏'
    if self.w_west: return '⏐'+self.get_val()+' '
    return ' '+self.get_val()+' '
  def __repr__(self,):
    return  self.get_coor()
  def get_coor(self): 
    return "("+chr(ord('`')+self.x)+self.get_char()+self.y.__str__()+")"
  
class game:
  def __init__(self,size,players):
    assert (players > 1 & players < 5),  f"{players} is an invalid number of players"
    assert (size > 1 & size < 10),  f"{size} is an invalid board size"
    self.size = size
    self.board = [[tile(1+x,size-y,self) for x in range(size)] for y in range(size)]
  def get(self,x,y): # 3 4
    return self.board[self.size-y][x-1] # 5 3
  def draw(self):
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    print()
    for y in range(self.size):
      for x in range(self.size):
        print(self.get(x+1,self.size-y) , end = '      \t')
      print()
      print()
    
    print("------------------------------------------------------------------------------------------------------------------------------------------")

    
def test():
  game1 = game(9,2)
  game1.get(5,3).set_wall_h()
  game1.get(7,2).set_wall_v()
  game1.get(5,1).val = 1
  game1.get(5,9).val = 2
  game1.draw()
  print(game1.get(3,4).get_coor()+":")
  print()
  print("                "+game1.get(3,4).get_north().get_coor())
  print("        "+ game1.get(3,4).get_west().get_coor()+" "+ game1.get(3,4).get_coor()+" "+ game1.get(3,4).get_east().get_coor())
  print("                "+game1.get(3,4).get_south().get_coor())
  print()
