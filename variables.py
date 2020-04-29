BACKGROUNDCOLOUR = "white"
MAXTILES = 20
MAPWIDTH = 25
MAPHEIGHT = 25
DIRT = 0
GRASS = 1
WATER = 2
BRICK = 3
WOOD = 4
SAND = 5
PLANK = 6
GLASS = 7
texturePath = "assets/textures/"
resources = [DIRT, GRASS, WATER, BRICK, WOOD, SAND, PLANK, GLASS]
names = {
  DIRT:"dirt",
  GRASS:"grass",
  WATER:"water",
  BRICK:"brick",
  WOOD:"wood",
  SAND:"sand",
  PLANK:"plank",
  GLASS:"glass"
}
textures = {
  DIRT:texturePath+"dirt.gif",
  GRASS:texturePath+"grass.gif",
  WATER:texturePath+"water.gif",
  BRICK:texturePath+"brick.gif",
  WOOD:texturePath+"wood.gif",
  SAND:texturePath+"sand.gif",
  PLANK:texturePath+"plank.gif",
  GLASS:texturePath+"glass.gif"
}
inventory = {
  DIRT:10,
  GRASS:10,
  WATER:10,
  BRICK:0,
  WOOD:5,
  SAND:3,
  PLANK:0,
  GLASS:0
}
playerImg = texturePath+"player.gif"
playerX = 0
playerY = 0
crafting = {
  BRICK:{WATER:1, DIRT:2},
  PLANK:{WOOD:3},
  GLASS:{SAND:1, WATER:1}
}
placekeys = {
  DIRT:"1",
  GRASS:"2",
  WATER:"3",
  BRICK:"4",
  WOOD:"5",
  SAND:"6",
  PLANK:"7",
  GLASS:"8"
}
craftkeys = {
  BRICK:"r",
  PLANK:"p",
  GLASS:"g"
}

