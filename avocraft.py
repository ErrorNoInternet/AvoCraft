import sys
import pygame
import random
import tkinter
from tkinter import *
from math import ceil
from tkinter import ttk
from pygame.locals import *
from threading import Thread
from tkinter import messagebox
fpsClock = pygame.time.Clock()
TILESIZE = 20
MAPWIDTH  = 32
MAPHEIGHT = 25
INVHEIGHT = 4*TILESIZE
PADDING = TILESIZE/1.1
BLACK = (0,0,0)
WHITE = (255,255,255)
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5
WOOD  = 6
FIRE  = 7
SAND  = 8
STONE = 9
BRICK = 10
recipeList = """
Wood = 2 Dirt
Torch = 2 Wood 1 Coal
Sand = 1 Dirt 1 Rock
Stone = 2 Rock
Brick = 1 Stone 1 Sand"""
resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA, WOOD, FIRE, SAND, STONE, BRICK]
textures = {
    DIRT  : pygame.image.load('Images/DirtPixel.png'),
    GRASS : pygame.image.load('Images/GrassPixel.png'),
    WATER : pygame.image.load('Images/WaterPixel.png'),
    COAL  : pygame.image.load('Images/CoalPixel.png'),
    ROCK  : pygame.image.load('Images/RockPixel.png'),
    LAVA  : pygame.image.load('Images/LavaPixel.png'),
    WOOD  : pygame.image.load('Images/WoodPixel.png'),
    FIRE  : pygame.image.load('Images/TorchPixel.png'),
    SAND  : pygame.image.load('Images/SandPixel.png'),
    STONE : pygame.image.load('Images/StonePixel.png'),
    BRICK : pygame.image.load('Images/BrickPixel.png')
}
inventory = {
    DIRT  : 10,
    GRASS : 5,
    WATER : 5,
    COAL  : 0,
    ROCK  : 1,
    LAVA  : 0,
    WOOD  : 5,
    FIRE  : 0,
    SAND  : 0,
    STONE : 0,
    BRICK : 0
}
craft = {
    WOOD  : {DIRT:2},
    FIRE  : {WOOD:2, COAL:1},
    SAND  : {DIRT:1, ROCK:1},
    STONE : {ROCK:2},
    BRICK : {STONE:1, SAND:1}
}
controls = {
    DIRT  : 49,
    GRASS : 50,
    WATER : 51,
    COAL  : 52,
    ROCK  : 53,
    LAVA  : 54,
    WOOD  : 55,
    FIRE  : 56,
    SAND  : 57,
    STONE : 48,
    BRICK : 45 
}
BASE_RARITY = 0
VERY_COMMON = 30
COMMON      = 45
RARE        = 50
VERY_RARE   = 53
ULTRA_RARE  = 54
tilemap = [ [GRASS for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)]
def showRecipes():
    recipe = tkinter.Tk()
    recipe.title("Recipe List")
    recipe.resizable(False, False)
    name = Label(recipe, text="Crafting Recipe List", font=("Calibri", 16, "bold"))
    name.pack(ipadx=20)
    recipeLabel = Label(recipe, text=recipeList)
    recipeLabel.pack()
    recipe.mainloop()
def generateRandomWorld():
    worldFile = open("Worlds/world1.world", "w+")
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            random_num = random.randint(BASE_RARITY, ULTRA_RARE)
            this_tile = GRASS
            if random_num < VERY_COMMON:
                if (random_num % 3) == 0:
                    this_tile = ROCK
                else:
                    this_tile = GRASS
            elif random_num >= VERY_COMMON and random_num < COMMON:
                if (random_num % 2) == 0:
                    this_tile = WATER
                else:
                    this_tile = DIRT
            elif random_num >= RARE and random_num < VERY_RARE:
                if (random_num % 2) == 0:
                    this_tile = COAL
                else:
                    this_tile = LAVA
            tilemap[row][column] = this_tile
            if this_tile == BRICK:
                worldFile.write(str("-"))
            else:
                worldFile.write(str(this_tile))
    worldFile.close()
player_position = [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)]
def loadWorld():
  file = open("Worlds/world1.world", "r")
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
      if counter2 >= 801:
        break
      else:
        character = line[counter2]
      if character == "0":
          tilemap[row][column] = DIRT
      elif character == "1":
        tilemap[row][column] = GRASS
      elif character == "2":
        tilemap[row][column] = WATER
      elif character == "3":
        tilemap[row][column] = COAL
      elif character == "4":
        tilemap[row][column] = ROCK
      elif character == "5":
        tilemap[row][column] = LAVA
      elif character == "6":
        tilemap[row][column] = WOOD
      elif character == "7":
        tilemap[row][column] = FIRE
      elif character == "8":
        tilemap[row][column] = SAND
      elif character == "9":
        tilemap[row][column] = STONE
      elif character == "-":
        tilemap[row][column] = BRICK
  file.close()
def saveMap():
  worldFile = open("Worlds/world1.world", "r")
  firstLine1 = worldFile.readlines()
  line4 = ""
  for item1 in firstLine1:
    line4 = item1
  firstChar = line4[0]
  worldFile.close()
  worldFile = open("Worlds/world1.world", "w+")
  worldFile.write(str(firstChar))
  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
        if tilemap[row][column] == BRICK:        
            worldFile.write(str("-"))
        else:
            worldFile.write(str(tilemap[row][column]))
  worldFile.close()
option = ""
def generateWorld():
    menu.destroy()
    global option
    option = "newWorld"
def openWorld():
    menu.destroy()
    global option
    option = "openWorld"
menu = tkinter.Tk()
menu.title("AvoCraft Menu")
menu.resizable(False, False)
name = Label(menu, text="AvoCraft", font=("Calibri", 16, "bold"))
name.pack(ipadx=20)
newWorld = ttk.Button(menu, text="Create new world", command=generateWorld)
newWorld.pack(ipadx=25)
loadWorldBtn = ttk.Button(menu, text="Open saved world", command=openWorld)
loadWorldBtn.pack(ipadx=24)
recipeBtn = ttk.Button(menu, text="Recipe list", command=showRecipes)
recipeBtn.pack(ipadx=38)
invisibleSep = Label(menu, text="")
invisibleSep.pack()
playerSep = Label(menu, text="Player Options", font=("Calibri", 14, "underline"))
playerSep.pack()
infiniteItems = IntVar()
unlimitedItems = ttk.Checkbutton(menu, text="Unlimited Resources", variable=infiniteItems)
infiniteItems.set(0)
unlimitedItems.pack()
try:
  checkFile = open("Worlds/world1.world", "r")
  checkFile.close()
except:
  loadWorldBtn['state'] = tkinter.DISABLED
menu.mainloop()
if infiniteItems.get() == 1:
    inventory = {
        DIRT  : 950,
        GRASS : 950,
        WATER : 950,
        COAL  : 950,
        ROCK  : 950,
        LAVA  : 950,
        WOOD  : 950,
        FIRE  : 950,
        SAND  : 950,
        STONE : 950,
        BRICK : 950
}
if option == "newWorld":
  generateRandomWorld()
elif option == "openWorld":
  loadWorld()
pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + INVHEIGHT))
pygame.display.set_caption('AvoCraft')
INVFONT = pygame.font.Font('Fonts/freesansbold.ttf', 18)
PLAYER = pygame.image.load('Images/Player.gif')
pygame.display.set_icon(pygame.image.load('Images/Player.gif'))
while True:
    DISPLAY_SURFACE.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            exit()
        elif event.type == KEYDOWN:
            saveMap()
            if (event.key == K_d) and (player_position[0] < MAPWIDTH - 1):
                player_position[0] +=1
            elif (event.key == K_a) and (player_position[0] > 0):
                player_position[0] -=1
            elif (event.key == K_w) and (player_position[1] > 0):
                player_position[1] -=1
            elif (event.key == K_s) and (player_position[1] < MAPHEIGHT - 1):
                player_position[1] +=1
            elif (event.key == K_SPACE):
                this_tile = tilemap[player_position[1]][player_position[0]]
                inventory[this_tile] +=1
                tilemap[player_position[1]][player_position[0]] = DIRT
            for key in controls:
                if (event.key == controls[key]):
                    if key in craft:
                        canBeMade = True
                        for each in craft[key]:
                            if craft[key][each] > inventory[each]:
                                canBeMade = False
                        if canBeMade == True:
                            for i in craft[key]:
                                inventory[i] -= craft[key][i]
                            inventory[key] += 1
            for key in controls:
                canBeMade = False
                if (event.key == controls[key]):
                    if inventory[key] > 0:
                        standing_tile = tilemap[player_position[1]][player_position[0]]
                        inventory[standing_tile] += 1
                        inventory[key] -= 1
                        tilemap[player_position[1]][player_position[0]] = key
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAY_SURFACE.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))
    inventory_x_position = PADDING
    inventory_y_position = MAPHEIGHT*TILESIZE + PADDING + 15
    for item in resources:
        DISPLAY_SURFACE.blit(textures[item], (inventory_x_position, inventory_y_position))
        inventory_x_position += PADDING
        numInventoryText = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAY_SURFACE.blit(numInventoryText, (inventory_x_position, inventory_y_position))
        inventory_x_position += PADDING*2
    DISPLAY_SURFACE.blit(PLAYER, (player_position[0]*TILESIZE, player_position[1]*TILESIZE))
    pygame.display.update()
    fpsClock.tick(24)
