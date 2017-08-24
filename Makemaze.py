from PIL import Image,ImageDraw
import random as rnd
import time

class Maze:

    class MazeTile:
        
        def __init__(self, X, Y, isWall = True):
            
            self.workedOn = False
            self.wall = isWall
            self.coordinateX = X
            self.coordinateY = Y
            self.connectTo = []

            
        def __str__(self):
            return str(self.wall)
            
        
        def __repr__(self):
            
            return "Mazetile, wall = {}, worked on = {} ,x = {}, y = {} ---".format(self.wall , self.workedOn, self.coordinateX, self.coordinateY)
            
    class MazeError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
    
    
    def __init__(self, dimensionX, dimensionY, pixelSizeOfTile = 10, mazeName = "A_Maze"):
        
        if not isinstance(dimensionX, int) or not isinstance(dimensionY, int):
            
            raise self.MazeError("Maze dimensions have to be an integer > 0")
            
        if dimensionX < 1 or dimensionY < 1:
            
            raise self.MazeError("Maze dimensions have to be an integer > 0")
            
        self.sizeX = dimensionX 
        self.sizeY = dimensionY 
        self.pixel = pixelSizeOfTile
        
        self.name = mazeName
        
        self.mazeIsDone = False
        self.mazeList = []
        self.wallList = []
        self.tileList = []
        
        
        
        for indexY in range (0,self.sizeY):
            templist = []
            
            for indexX in range(0,self.sizeX):
                newTile = self.MazeTile(indexX, indexY, isWall = False)
                templist.append(newTile)
                
            self.mazeList.append(templist)
        
        self.mazeString = ""
        
    def __str__(self):
        
        self.mazeString = ""
        
        for row in self.mazeList:
            
            for tile in row:
                
                self.mazeString += "{:^7}".format(str(tile))
        
            self.mazeString += "\n"
        
        
        return self.mazeString
        
            
        
    def __repr__(self):
            
            
        return "This is a Maze with width of {} and height of {}".format(self.sizeX , self.sizeY)
    
    def getNextTiles(self,X,Y):
        
        if X < 0 or Y < 0:
            
            raise self.MazeError("Inputes have to be an integer > 0")
        
        templist = []
        
        try:
            if Y == 0:
                pass
            else:
                templist.append(self.mazeList[Y-1][X])
        
        except(IndexError):
            pass

        try:
            templist.append(self.mazeList[Y+1][X])
        except(IndexError):
            pass
            
        try:
            if X == 0:
                pass
            else:
                templist.append(self.mazeList[Y][X-1])
        except(IndexError):
            pass
            
        try:
            templist.append(self.mazeList[Y][X+1])
        except(IndexError):
            pass
        
        return templist
        
    def connectTiles(self, tileA, tileB):
        
        X1 = tileA.coordinateX 
        Y1 = tileA.coordinateY
        
        X2 = tileB.coordinateX 
        Y2 = tileB.coordinateY
        
        if X1 == X2:
            
            if Y1 < Y2:
                
                tileA.connectTo.append("S")
                tileB.connectTo.append("N")
            
            elif Y1 > Y2:
                tileA.connectTo.append("N")
                tileB.connectTo.append("S")

        else:
            if X1 < X2:
                
                tileA.connectTo.append("E")
                tileB.connectTo.append("W")
            
            else:
                tileA.connectTo.append("W")
                tileB.connectTo.append("E")
        
        return True
        
    def makeEntryandExit(self,random = False):
        
        if random:
            
            tile = rnd.choice(self.mazeList[0])
            tile.connectTo.append("N")
                    
            tile = rnd.choice(self.mazeList[-1])
            tile.connectTo.append("S")
        else:
            self.mazeList[0][0].connectTo.append("N")
            self.mazeList[-1][-1].connectTo.append("S")
                
            
        
    
    def makeMazeSimple(self):
        
        if self.mazeIsDone:
            raise self.MazeError("Maze is already done")
        
        frontList = []
        startingtile = rnd.choice(rnd.choice(self.mazeList))
        startingtile.workedOn = True
        frontList += self.getNextTiles(startingtile.coordinateX, startingtile.coordinateY)
        

        while len(frontList) > 0 :
            
            
            

            newFrontTiles = []
            workedOnList = []
            
            rnd.shuffle(frontList)
            nextTile = frontList.pop()
            nextTile.workedOn = True
            
            tempList = self.getNextTiles(nextTile.coordinateX,nextTile.coordinateY)
            

            for tile in tempList:
                if tile.workedOn:
                    
                    workedOnList.append(tile)
                    
                else:
                    
                    if not tile in frontList:
                        newFrontTiles.append(tile)
                    
            frontList += newFrontTiles
            

            
            if len(workedOnList) > 1:
                connectTile = rnd.choice(workedOnList)
            
            else:
                connectTile = workedOnList[0]
            
            self.connectTiles(nextTile,connectTile)
            
        self.makeEntryandExit()
        self.MazeIsDone = True
        return True
            
   
    def makeMazeGrowTree(self,weightLast = 100,weightFirst = 100):
        
        if self.mazeIsDone:
            raise self.MazeError("Maze is already done")
        
        
        startingtile = rnd.choice(rnd.choice(self.mazeList))
        startingtile.workedOn = True
        
        choiceList = [startingtile]
        
        while len(choiceList) > 0:
            
            choice_ = rnd.random() * 100
            
            if choice_ <= weightLast:
                nextTile = choiceList[-1]
            elif weightLast < choice_ < weightFirst:
                nextTile=rnd.choice(choiceList)
            else:
                nextTile = choiceList[0]
            
            neiList = []
            
            for tile in self.getNextTiles(nextTile.coordinateX,nextTile.coordinateY):
                
                if not tile.workedOn:
                    neiList.append(tile)
            
            if len(neiList) == 0:
                choiceList.remove(nextTile)
            
            else:
                connectTile = rnd.choice(neiList)
                connectTile.workedOn = True
                choiceList.append(connectTile)
                self.connectTiles(nextTile,connectTile)
                
        
            
        self.makeEntryandExit()
        self.MazeIsDone = True
        return True
        
    def makePP(self):
        
        if len(self.mazeList) == 0:
            raise self.MazeError("There is no Maze yet")
        
        size = (self.pixel * (self.sizeX * 2 + 1), self.pixel * (self.sizeY * 2 + 1))

        image = Image.new("1",size,color = 0)
        drawImage = ImageDraw.Draw(image)
            
        wallTiles = []
        for row in self.mazeList:
                
                for tile in row:
                    
                    x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                    y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                    drawImage.rectangle([x, y, x + self.pixel -1, y + self.pixel -1], fill = 1)

                    
                    if "N" in tile.connectTo:
                        
                        x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                        y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                        drawImage.rectangle([x, y - self.pixel, x + self.pixel - 1, y - 1], fill = 1)
                        
                    if "S" in tile.connectTo:
                        
                        x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                        y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                        drawImage.rectangle([x, y + self.pixel, x + self.pixel - 1, y + self.pixel + self.pixel - 1], fill = 1)
                        
                    if "W" in tile.connectTo:
                        
                        x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                        y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                        drawImage.rectangle([x - self.pixel, y, x - 1, y + self.pixel - 1], fill = 1)
        
                    if "E" in tile.connectTo:
                        
                        x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                        y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                        drawImage.rectangle([x + self.pixel, y, x + self.pixel + self.pixel - 1, y + self.pixel - 1], fill = 1)

        return image
        
                        
    def saveImage(self,image,name = None):
        
        if name == None:
            size = (self.pixel * self.sizeX, self.pixel * self.sizeY)
            name = self.name +"-"+ str(size[0]) + "_" + str(size[1]) + ".png"
        image.save(name)
                    
        return True

timer = time.time()
newMaze = Maze(100,100)
newMaze.makeMazeGrowTree(80.50)
print(time.time() - timer)
newMaze.makePP().show
#newMaze.saveImage(newMaze.makePP())
