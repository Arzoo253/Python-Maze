"""
    Written by turidus (github.com/turidus) 
    Dependend on Pillow, a fork of PIL (https://pillow.readthedocs.io/en/4.2.x/index.html)
"""
from PIL import Image,ImageDraw
import random as rnd

class Maze:
    """ This Class represents a Maze. After init it consists of an unformed maze made out of a nested list (grid) of 
            untouched floor tiles. It size in X and Y are dependent on input.
            It depends on Pillow, a PIL fork (https://pillow.readthedocs.io/en/4.2.x/index.html).
            
            The finale internal representation of the maze is a nested list of touched floor tiles that are connected to at 
            least one neighbour. Walls will be added by the graphic representation. 
            
            The maze can be formed than by two different algorithms, modified Prim's and Growing Tree. A short 
            explanation of the used algorithms (and many more) can be found at http://www.astrolog.org/labyrnth/algrithm.htm
            A more in depth explanation can be found in this article series:
            Prims Algorithm: http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
            Growing Tree Algorithm: http://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
            
            This classes raises Maze Error on invalid input; when a maze get the command to change after it was formed or
            if the maze gets the command to make a graphical representation of an unformed maze.
            
            Content:
            
            private subclass    Maze Tile:  Structure representing a single tile.
            private subclass    Maze Error: Custom Error
            
            private function    __init_(int,int,int = 10,string = A_Maze):    this function takes two integers for size(X,Y)
                                                                              one optional integer for the pixel size of one tile
                                                                              and an optional string for the name of the Maze.
            private function    __str__; __repr()__ :  Housekeeping
            private function    getNextTiles(int,int):  returns a list of tiles
                                                        function finding available tiles to a specified tile
            private function    connectTile(tileA,tileB): connects specified tiles to make a way
            private function    makeEntryandExit(): creates a entry and an exit into the maze
            
            public function     makeMazeSimple:():  returns True
                                                    This function takes the unformed maze and forms it with the modified Prim's
                                                    algorithm. This results in an simple to solve maze. This algorithms is less 
                                                    efficient than the Growing Tree algorithm.
            public function     makeMazeGrowingTree(int,int): returns True
                                                              This algorithm forms the maze with the Growing Tree algorithmus
                                                              takes two integer values between 0 and 100, with the first 
                                                              integer bigger than the second one. These are are weights defining the 
                                                              behavior of the algorithm. (see link above)
            public function     makePP():   Returns an image object.
                                            This function takes a formed maze and creates a picture with the help of Pillow.
                                            The size of the picture depends on the chosen pixel size per tiles and the amount of tiles
                                            
            public function     saveImage(image,string = None): Specialized implementation of Pillow's Save function. Takes an image and
                                                                saves it with an (optional) given name. If no name is given, a name will
                                                                be constructed.
                                            
                                                              
    """

    class MazeTile:
        """ This subclass is a structure representing a single tile inside the Maze. This tile has a X and Y coordinate which are specified on generation.
            It can also be specified if the tile is a wall or a floor.
        """
        
        def __init__(self, X, Y, isWall = True):
            """Generator for the MazeTile class
            """
            
            
            self.workedOn = False   # Needed for certain generation algorithm to define if a tile as already be touched
            self.wall = isWall      # Is the tile a wall (True) or a floor (False). Mostly for future proving
            self.coordinateX = X    # Defining the X coordinate
            self.coordinateY = Y    # Defining the Y coordinate 
            self.connectTo = []     # A list of strings that describe the tiles this tile is connected to (North, South, West, East)

            
        def __str__(self):
            return str(self.wall)
            
        
        def __repr__(self):
            
            return "Mazetile, wall = {}, worked on = {} ,x = {}, y = {} ---".format(self.wall , self.workedOn, self.coordinateX, self.coordinateY)
            
    class MazeError(Exception):
        """ Custom Maze Error, containing a string describing the error that occurred.
        """
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
    
    
    def __init__(self, dimensionX, dimensionY, pixelSizeOfTile = 10, mazeName = "A_Maze"):
        """Generator for the Maze class.
           It takes two integer to decide the size of the maze (X and Y), an optional integer two decide how many pixel a tile is wide in the finale
           picture. It also takes an optional tile to determine the name of the maze.
        
        """
        
        if not isinstance(dimensionX, int) or not isinstance(dimensionY, int) or not isinstance(pixelSizeOfTile, int) or not isinstance(mazeName, str): 
                                                                                                                                #Checking input errors
            raise self.MazeError("Maze dimensions have to be an integer > 0")
            
        if dimensionX < 1 or dimensionY < 1: # Checking input errors
            
            raise self.MazeError("Maze dimensions have to be an integer > 0")
            
        self.sizeX = dimensionX     #The size of the Maze in the X direction (from left to right)
        self.sizeY = dimensionY     #The size of the Maze in the Y direction (from up to down)
        self.pixel = pixelSizeOfTile    #The pixel size of a single tile. Determines the finale size of the picture
        
        self.name = mazeName    #The name of the Maze. Can be any string
        self.mazeIsDone = False     #When this flag is False, no picture can be made. When this flag is True, the maze can not be changed
        
        self.mazeList = []          #A nested List of maze Tiles. The internal representation of the maze
        
        self.wallList = []          #A list of all lists that are walls (needed for certain algorithm
        self.tileList = []          #A single list of all tiles (needed of certain algorithm)
        
        self.mazeString = ""        #A string describing the Maze in a pseudo graphical manner, gets generated everytime __str__() gets called
        
        
        for indexY in range (0,self.sizeY):     #This loops generates the mazeList and populates it with new untouched floor tiles
            templist = []
            
            for indexX in range(0,self.sizeX):
                newTile = self.MazeTile(indexX, indexY, isWall = False)
                templist.append(newTile)
                
            self.mazeList.append(templist)
        
        
        
    def __str__(self): #Generates the mazeString which is a string with as many columns as sizeX and as many lines as sizeY
        
        self.mazeString = ""
        
        for row in self.mazeList:
            
            for tile in row:
                
                self.mazeString += "{:^7}".format(str(tile))
        
            self.mazeString += "\n"
        
        
        return self.mazeString
        
            
        
    def __repr__(self): #Builds a representing string
            
            
        return "This is a Maze with width of {} and height of {}".format(self.sizeX , self.sizeY)
    
    def getNextTiles(self,X,Y): 
        """ 
            This function collects all nearest neighbour of a tile. Important for tiles that lay on a border.
            
        """
        
        if X < 0 or Y < 0:  #Checks input error (this should never happen)
            
            raise self.MazeError("Inputs have to be an integer > 0")
        
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
        """   Takes two tiles and returns True if successful. 
              Connect the two given tiles to make a way. This is used to decide where walls shouldn't be in the final picture.
              The Tile connectTo field is appended by the compass direction of the tile it connects to (N,S,E,W).
        """
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
        """ Takes an optional boolean
            If random is set to True, it chooses the entry and exit field randomly.
            It set to False, it chooses the left upper most and right lower most corner as entry. 
        """
        if random:
            
            tile = rnd.choice(self.mazeList[0])
            tile.connectTo.append("N")
                    
            tile = rnd.choice(self.mazeList[-1])
            tile.connectTo.append("S")
        else:
            self.mazeList[0][0].connectTo.append("N")
            self.mazeList[-1][-1].connectTo.append("S")
            
        return True
                
            
        
    
    def makeMazeSimple(self):
        """Algorithm to form the final maze. It works like the modified Prim's algorithm
            (http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
            
            It works on the initial mazeList. The finale mazeList consist of touched floor tiles that are connect
            with each other.
            The end result is a easy to solve perfect 2D maze.
            
            This runs much slower than GrowTreeAlgorithm.
             
             
            A short description of what happens:
            At first a untouched (tile.workedOn = False) tile is randomly chosen, it is transformed to a
            touched tile and all neighbour are put into a frontier list.
             
            From this list comes the next tile which is again transformed into a touched tile
            and removed from the frontier list.
            Then this touched tile is connected to a randomly neighbor that was also touched.
            All neighbours that are untouched tiles are added into the frontier list.
             
            This will run until the frontier list is empty.
        """
        
        if self.mazeIsDone:     #Can only run if the maze is not already formed
            raise self.MazeError("Maze is already done")
        
        frontList = []          #A list of all untouched tiles that border a touched tile
        startingtile = rnd.choice(rnd.choice(self.mazeList))    #A randomly chosen tile that acts as starting tile
        
        startingtile.workedOn = True    #This flag always gets set when a tile has between worked on.
        frontList += self.getNextTiles(startingtile.coordinateX, startingtile.coordinateY)  #populates the frontier
                                                                                                #list with the first 2-4 tiles 
        

        while len(frontList) > 0 : #When the frontier list is empty the maze is finished because all tiles have been connected
            
            

            newFrontTiles = []
            workedOnList = []
            
            rnd.shuffle(frontList)
            nextTile = frontList.pop()
            nextTile.workedOn = True
            
            tempList = self.getNextTiles(nextTile.coordinateX,nextTile.coordinateY)
            

            for tile in tempList: #Finds all neighbours who are touched and all that are a untouched
                if tile.workedOn:
                    
                    workedOnList.append(tile)
                    
                else:
                    
                    if not tile in frontList:
                        newFrontTiles.append(tile)
                    
            frontList += newFrontTiles
            

            
            if len(workedOnList) > 1:   #Chooses the neighbor the tile should connect to
                connectTile = rnd.choice(workedOnList)
            
            else:
                connectTile = workedOnList[0]
            
            self.connectTiles(nextTile,connectTile)
            
        self.makeEntryandExit()     #Finally produces a Entry and an Exit
        self.MazeIsDone = True
        return True
            
   
    def makeMazeGrowTree(self,weightFirst = 90,weightLast = 30):
        
        """Algorithm to form the final maze. It works like the Grow Tree algorithm
            http://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
            
            It works on the initial mazeList. The finale mazeList consist of touched floor tiles that are connect
            with each other.
            The end result is a perfect 2D maze that has a variable hardness in solution
            
            This runs much faster than makeMazeSimple and should be used as default.
            
            This algorithm can be modified with two weights between 0 and 100. 
            weightFirst should always be higher or equal to weightLast.
            
            Three extrems:
            
            weightFirst == weightlast == 0:
                
                The resulting maze will have a lot of long passageways (high river factor) and
                will be very easy to solve.
            
            weightFirst == 100, weightLast == 0
                
                The algorithm always chooses the next tile randomly
                and behaves like Prim's algorithm, but runs much faster.
                
            weightFirst == 100, weightLast == 100:
                
                The algorithm always takes the the first tile out of the choice list and behaves
                like a reversed backtrace 
                http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
                
            I personally like a 90/50 distribution but feel free to experiment yourself.
             
            A short description of what happens:
            At first one untouched tile is randomly chosen, it is transformed to a
            touched tile and it is out into a list of available tiles.
            
            From this list is a tile chosen, how depends on the weights.
            If this tile has no untouched neighbours it is removed from the list of available tiles.
            Else a neighbour is chosen, marked as touched, put into the availabe tile list and
            connected to the current tile.
            This loops until the list of available tiles is empty.
        """
        
        if self.mazeIsDone: #This function only runs of the Maze is not already formed.
            raise self.MazeError("Maze is already done")
        
        
        startingtile = rnd.choice(rnd.choice(self.mazeList))    #First tile is randomly chosen
        startingtile.workedOn = True
        
        choiceList = [startingtile] #The list of available tiles
        
        while len(choiceList) > 0:  #Runs until choiceList is empty
            
            choice_ = rnd.random() * 100    #This random choice determines how the next tile is chosen
            
            if choice_ <= weightLast:  
                nextTile = choiceList[-1]
            elif weightLast < choice_ < weightFirst:
                nextTile=rnd.choice(choiceList)
            else:
                nextTile = choiceList[0]
            
            neiList = []    #List of neighbours
            
            for tile in self.getNextTiles(nextTile.coordinateX,nextTile.coordinateY):
                
                if not tile.workedOn:
                    neiList.append(tile)
            
            if len(neiList) == 0:   #either removing this tile or choosing a neighbour to interact with
                choiceList.remove(nextTile)
            
            else:
                connectTile = rnd.choice(neiList)
                connectTile.workedOn = True
                choiceList.append(connectTile)
                self.connectTiles(nextTile,connectTile)
                
        
            
        self.makeEntryandExit() #finally marking an Entry and an Exit
        self.MazeIsDone = True
        return True
        
    def makePP(self):
        """
        This generates and returns a Pillow Image object. It takes into account the size of the maze and
            the size of the the indivual pixel defined with pixelSizeOfTile. Defaults to 10 pixel.
            
            It create this picture by drawing a white square with the defined size for every tile in
            the mazeList on a black background. It then proceeds to draw in the connections this tile has by checking
            tile,connectedTo.
        """
        
        if len(self.mazeList) == 0:
            raise self.MazeError("There is no Maze yet")
        
        size = (self.pixel * (self.sizeX * 2 + 1), self.pixel * (self.sizeY * 2 + 1)) 
            #Determines the size of the picture. It does this by taking the number of tiles,
                # multiplying it with 2 to account for walls or connections and adds one for offset
        

        image = Image.new("1",size,color = 0) #Generates a Pillow Image object
        drawImage = ImageDraw.Draw(image)
        
        for row in self.mazeList: #Iterates over all tiles
                
                for tile in row:
                    
                    x = ((tile.coordinateX  + 1) * 2 - 1) * self.pixel
                    y = ((tile.coordinateY  + 1) * 2 - 1) * self.pixel
                    drawImage.rectangle([x, y, x + self.pixel -1, y + self.pixel -1], fill = 1)

                    
                    if "N" in tile.connectTo:
                        drawImage.rectangle([x, y - self.pixel, x + self.pixel - 1, y - 1], fill = 1)
                        
                    if "S" in tile.connectTo:
                        drawImage.rectangle([x, y + self.pixel, x + self.pixel - 1, y + self.pixel + self.pixel - 1], fill = 1)
                        
                    if "W" in tile.connectTo:
                        drawImage.rectangle([x - self.pixel, y, x - 1, y + self.pixel - 1], fill = 1)
        
                    if "E" in tile.connectTo:
                        drawImage.rectangle([x + self.pixel, y, x + self.pixel + self.pixel - 1, y + self.pixel - 1], fill = 1)

        return image #returns an image object
        
                        
    def saveImage(self,image,name = None):
        """Specialized implementation of Pillow's Save function. Takes an image and
            saves it with an (optional) given name. If no name is given, a name will
            be constructed.
            
            The name is constructed out of the Maze Name and its size in x and y direction
        """
        if name == None:
            size = (self.pixel * self.sizeX, self.pixel * self.sizeY)
            name = self.name +"-"+ str(size[0]) + "_" + str(size[1]) + ".png"
        image.save(name)
                    
        return True

#Examples:
#newMaze = Maze(100,100)
#newMaze.makeMazeGrowTree(90.30)
#mazeImage = newMaze.makePP()
#mazeImage.show() #can or can not work, see Pillow documentation 
#newMaze.saveImage(mazeImage)
