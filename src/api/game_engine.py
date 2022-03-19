# https://quoridorstrats.wordpress.com/notation/


# Example of a game record, each number referring to a round. 
# 1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v 
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

# Example of board state
# d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3
# horzontal walls / vertical walls / player pieces / walls remaining by player / which player's turn?
def state_to_array(shorthand):
  gameOut = game(9,2)
  walls = [0,0,0,0]
  print(shorthand)
  temp = shorthand.split('/')
  temp[0]=temp[0].strip()
  temp[1]=temp[1].strip()
  temp[2]=temp[2].strip()
  temp[3]=temp[3].strip()
  temp[4]=temp[4].strip()

  # Horizontal Walls
  hori = [temp[0][i:i+2] for i in range(0, len(temp[0]), 2)]
  for i in hori:
    x = ord(i[0])-ord('`')
    y = int(i[1])
    gameOut.get(x,y).set_wall_h()

  # Vertical Walls
  verti = [temp[1][i:i+2] for i in range(0, len(temp[1]), 2)]
  for i in verti:
    x = ord(i[0])-ord('`')
    y = int(i[1])
    gameOut.get(x,y).set_wall_v()

  # players
  players = temp[2].split(' ')
  for i in range(len(players)):
    x = ord(players[i][0])-ord('`')
    y = int(players[i][1])
    gameOut.get(x,y).val = i+1

  walls = temp[3].split(' ')
  for i in range(len(walls)):
    print("Player " +(i+1).__str__()+ " has " + walls[i].__str__() + " walls remaining.")

  print("It is Player "+temp[4]+"'s turn.")

  return gameOut.__repr__()
    

## Game Engine Data Structures
# Tile Class is equivalent to a 'node' data structure.
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
    if self.val == 1: return 'x'
    if self.val == 2: return 'o'
    if self.val == 3: return '@'
    if self.val == 4: return '*'
    return ' '
  def set_wall_h(self):
    print("Horizontal wall at "+self.__repr__())
    self.get_north().w_south = True
    self.w_north = True 
    self.get_east().get_north().w_south = True
    self.get_east().w_north = True
  def set_wall_v(self):
    print("Vertical wall at "+self.__repr__())
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
  def html(self,):
    out = "<td style='"
    if self.w_north:  out +="border-top: 2px solid;"
    if self.w_east: out +="border-right: 2px solid;"
    if self.w_south: out +="border-bottom: 2px solid;"
    if self.w_west: out +="border-left: 2px solid;"
    if self.val == 1: out += 'background-color:#bae1ff;'
    elif self.val == 2: out += 'background-color:#baffc9;'
    elif self.val == 3: out += 'background-color:#ffffba;'
    elif self.val == 4: out += 'background-color:#ffdfba;'
    out += "'>"
    out += chr(ord('`')+self.x)
    out += self.y.__str__()
    out+="</td>"
    return out
    
  def get_coor(self): 
    return "("+chr(ord('`')+self.x)+self.get_char()+self.y.__str__()+")"
  
# Game stores 
class game:
  def __init__(self,size,players):
    assert (players > 1 & players < 5),  f"{players} is an invalid number of players"
    assert (size > 1 & size < 10),  f"{size} is an invalid board size"
    self.size = size
    self.board = [[tile(1+x,size-y,self) for x in range(size)] for y in range(size)]
  def get(self,x,y): # 3 4
    return self.board[self.size-y][x-1] # 5 3
  def __repr__(self):
    #out = '<link rel="stylesheet" href="{% static "css/ascii.css" %}" />'
    out = "<div id='wrapper'><h1>Converted Game Board:</h1>\
      <section id='left'><table><tbody>"
    for y in range(self.size):
      out += "<tr>"
      for x in range(self.size):
        out += self.get(x+1,self.size-y).html() 
      out +='</tr>'
    out +="</tbody></table></section>"
    out +="<section id='right'><table>\
      <tr><td style = 'background-color:#bae1ff;'>Player 1</td><td style = 'background-color:#baffc9;'>Player 2</td></tr>\
      <tr><td style = 'background-color:#ffffba;'>Player 3</td><td style = 'background-color:#ffdfba;'>Player 4</td></tr>\
      </table></section>"
    return out
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
