import turtle
import random
import tkinter
from tkinter import *
from math import ceil
from tkinter import ttk
from variables import *
from threading import Thread
from tkinter import messagebox
from turtle import Screen, Turtle
version = "0.2"
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
  button = Turtle()
  button.hideturtle()
  button.shape('circle')
  button.fillcolor('red')
  button.penup()
  button.goto(width-73, -10)
  button.write("Save World", align='center', font=FONT)
  button.sety(0)
  button.setx(width - 12)
  button.onclick(saveMap)
  button.showturtle()
  turtle = Turtle()
  turtle.hideturtle()
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      drawResource(column, row)
def drawInventory():
  global drawing
  if drawing == False:
    drawing = True
    rendererT.color(BACKGROUNDCOLOUR)
    rendererT.goto(0,28)
    rendererT.begin_fill()
    for i in range(2):
      rendererT.forward(inventory_height - 60)
      rendererT.right(90)
      rendererT.forward(width-24)
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
def loadWorld():
  file = open("worlds/world1.world", "r")
  lineOld = file.readlines()
  line = []
  line2 = ""
  for item in lineOld:
    line2 = item
  for item in line2:
    line.append(item)
  counter2 = 0
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      counter2 = counter2 + 1
      if counter2 >= 625:
        break
      else:
        character = line[counter2]
      if character == "0":
          world[column][row] = DIRT
      elif character == "1":
        world[column][row] = GRASS
      elif character == "2":
        world[column][row] = WATER
      elif character == "3":
        world[column][row] = BRICK
      elif character == "4":
        world[column][row] = WOOD
      elif character == "5":
        world[column][row] = SAND
      elif character == "6":
        world[column][row] = PLANK
      elif character == "7":
        world[column][row] = GLASS
  file.close()
def saveMap(nothing, nothing2):
  worldFile = open("worlds/world1.world", "r")
  firstLine1 = worldFile.readlines()
  line4 = ""
  for item1 in firstLine1:
    line4 = item1
  firstChar = line4[0]
  worldFile.close()
  worldFile = open("worlds/world1.world", "w+")
  worldFile.write(str(firstChar))
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      worldFile.write(str(world[column][row]))
  worldFile.close()
  messagebox.showinfo("World saved", "Your world has been successfully saved")
def generateRandomWorld():
  worldFile = open("worlds/world1.world", "w+")
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
      worldFile.write(str(tile))
  worldFile.close()
def generateWorld():
  menu.destroy()
  global option
  option = "newWorld"
def openWorld():
  menu.destroy()
  global option
  option = "openWorld"
TILESIZE = 20
INVWIDTH = 8
FONT = ('Arial', 12, 'bold')
drawing = False
option = ""
menu = tkinter.Tk()
menu.title("AvoCraft Menu")
name = Label(menu, text="AvoCraft", font=("Calibri", 16, "bold"))
name.pack(ipadx=20)
newWorld = ttk.Button(menu, text="Create new world", command=generateWorld)
newWorld.pack(ipadx=25)
loadWorldBtn = ttk.Button(menu, text="Open saved world", command=openWorld)
loadWorldBtn.pack(ipadx=25)
try:
  checkFile = open("worlds/world1.world", "r")
  checkFile.close()
except:
  loadWorldBtn['state'] = tkinter.DISABLED
menu.mainloop()
screen = turtle.Screen()
screen.onscreenclick(saveMap, 1, add=False)
screen.title("AvoCraft " + version)
width = (TILESIZE * MAPWIDTH-370) + max(200,INVWIDTH * 50)
num_rows = int(ceil((len(resources) / INVWIDTH)))
inventory_height =  num_rows * 120 + 40
height = (TILESIZE * MAPHEIGHT) + inventory_height + 20
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
if option == "newWorld":
  generateRandomWorld()
elif option == "openWorld":
  loadWorld()
drawInventory()
drawWorld()
