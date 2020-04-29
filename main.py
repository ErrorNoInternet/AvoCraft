import turtle
import random
from math import ceil
from variables import *
from threading import Thread
version = "0.1"
def moveLeft():
  global playerX
  if(drawing == False and playerX > 0):
    oldX = playerX
    playerX -= 1
    drawResource(oldX, playerY)
    drawResource(playerX, playerY)
def moveRight():
  global playerX, MAPWIDTH
  if(drawing == False and playerX < MAPWIDTH - 1):
    oldX = playerX
    playerX += 1
    drawResource(oldX, playerY)
    drawResource(playerX, playerY)
def moveUp():
  global playerY
  if(drawing == False and playerY > 0):
    oldY = playerY
    playerY -= 1
    drawResource(playerX, oldY)
    drawResource(playerX, playerY)
def moveDown():
  global playerY, MAPHEIGHT
  if(drawing == False and playerY < MAPHEIGHT - 1):
    oldY = playerY
    playerY += 1
    drawResource(playerX, oldY)
    drawResource(playerX, playerY)
def pickUp():
  global playerX, playerY
  drawing = True
  currentTile = world[playerX][playerY]
  if inventory[currentTile] < MAXTILES:
    inventory[currentTile] += 1
    world[playerX][playerY] = DIRT
    drawResource(playerX, playerY)
    drawInventory()
def place(resource):
  if inventory[resource] > 0:
    currentTile = world[playerX][playerY]
    if currentTile is not DIRT:
      inventory[currentTile] += 1
    world[playerX][playerY] = resource
    inventory[resource] -= 1
    drawResource(playerX, playerY)
    drawInventory()
  else:
    pass
def craft(resource):
  if resource in crafting:
    canBeMade = True
    for i in crafting[resource]:
      if crafting[resource][i] > inventory[i]:
        canBeMade = False
        break
    if canBeMade == True:
      for i in crafting[resource]:
        inventory[i] -= crafting[resource][i]
      inventory[resource] += 1
    else:
      pass
    drawInventory()
def makeplace(resource):
  return lambda: place(resource)
def bindPlacingKeys():
  for k in placekeys:
    screen.onkey(makeplace(k), placekeys[k])
def makecraft(resource):
  return lambda: craft(resource)
def bindCraftingKeys():
  for k in craftkeys:
    screen.onkey(makecraft(k), craftkeys[k])
def drawResource(y, x):
  global drawing
  if drawing == False:
    drawing = True
    rendererT.goto( (y * TILESIZE) + 20, height - (x * TILESIZE) - 20 )
    texture = textures[world[y][x]]
    rendererT.shape(texture)
    rendererT.stamp()
    if playerX == y and playerY == x:
      rendererT.shape(playerImg)
      rendererT.stamp()
    screen.update()
    drawing = False
def drawWorld():
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      drawResource(column, row)
def drawInventory():
  global drawing
  if drawing == False:
    drawing = True
    rendererT.color(BACKGROUNDCOLOUR)
    rendererT.goto(0,0)
    rendererT.begin_fill()
    for i in range(2):
      rendererT.forward(inventory_height - 60)
      rendererT.right(90)
      rendererT.forward(width)
      rendererT.right(90)
    rendererT.end_fill()
    rendererT.color('black')
    for i in range(1,num_rows+1):
      rendererT.goto(20, (height - (MAPHEIGHT * TILESIZE)) - 20 - (i * 100))
      rendererT.write("Place")
      rendererT.goto(20, (height - (MAPHEIGHT * TILESIZE)) - 40 - (i * 100))
      rendererT.write("Craft")
    xPosition = 70
    yPostition = height - (MAPHEIGHT * TILESIZE) - 80
    itemNum = 0
    for i, item in enumerate(resources):
      rendererT.goto(xPosition, yPostition)
      rendererT.shape(textures[item])
      rendererT.stamp()
      rendererT.goto(xPosition, yPostition - TILESIZE)
      rendererT.write(inventory[item])
      rendererT.goto(xPosition, yPostition - TILESIZE - 20)
      rendererT.write(placekeys[item])
      if crafting.get(item) != None:
        rendererT.goto(xPosition, yPostition - TILESIZE - 40)
        rendererT.write(craftkeys[item])     
      xPosition += 50
      itemNum += 1
      if itemNum % INVWIDTH == 0:
        xPosition = 70
        itemNum = 0
        yPostition -= TILESIZE + 80
    drawing = False
def generateRandomWorld():
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      randomNumber = random.randint(0,12)
      if randomNumber in [1,2]:
        tile = WATER
      elif randomNumber in [3,4]:
        tile = GRASS
      elif randomNumber == 5:
        tile = WOOD
      elif randomNumber == 6:
        tile = SAND
      else:
        tile = DIRT
      world[column][row] = tile
TILESIZE = 20
INVWIDTH = 8
drawing = False
screen = turtle.Screen()
screen.title("AvoCraft " + version)
width = (TILESIZE * MAPWIDTH-370) + max(200,INVWIDTH * 50)
num_rows = int(ceil((len(resources) / INVWIDTH)))
inventory_height =  num_rows * 120 + 40
height = (TILESIZE * MAPHEIGHT) + inventory_height
screen.setup(width, height)
screen.setworldcoordinates(0,0,width,height)
screen.bgcolor(BACKGROUNDCOLOUR)
screen.listen()
screen.register_shape(playerImg)
for texture in textures.values():
  screen.register_shape(texture)
rendererT = turtle.Turtle()
rendererT.hideturtle()
rendererT.penup()
rendererT.speed(0)
rendererT.setheading(90)
world = [ [DIRT for w in range(MAPHEIGHT)] for h in range(MAPWIDTH) ]
screen.onkey(moveUp, 'w')
screen.onkey(moveDown, 's')
screen.onkey(moveLeft, 'a')
screen.onkey(moveRight, 'd')
screen.onkey(pickUp, 'space')
bindPlacingKeys()
bindCraftingKeys()
generateRandomWorld()
drawInventory()
drawWorld()
screen.mainloop()
