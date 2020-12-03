#   Import modules
import random, pygame, math

#   Sizes of outer display and inner board
displayWidth = 800
displayHeight = 800
boardWidth = displayWidth*0.8
boardHeight = displayHeight*0.8

#   Global variables (constants) and styling for board
alph = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
digits = range(1,len(alph)+1)
bgColor = (148,85,58)
borderColor = (0,0,0)
textColor = (0,0,0)
gameOverColor = (0,0,0)
warningColor = (168,66,50)
paddingTop = 30
lightCellColor = (255,255,255)
darkCellColor = (148,85,58)
steppedOnLightCellColor = (186,93,93)
steppedOnDarkCellColor = (148,58,58)
highlightColorLight = (180,180,180)
highlightColorDark = highlightColorLight#(118,55,28)
linewidth = 7
#   Size of board, must be between 1-25
size = 8#   Ex:   4--> 4x4, 8--> 8x8, 16--> 16x16

#   Determine if size is OK (not OK if it's greater than the length of the alphabet)
while size > len(alph):
    try:
        size = int(input('Length of square board (one dimension, integer):'))
        if type(size) == typeof(1) and size != 0 and len(alph) >= size:
            break
    except:
        continue
    
#   Initiate pygame
pygame.init()
chessDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Chessboard')
clock = pygame.time.Clock()
#   Load horse image
horseImg = pygame.image.load('horse.png')
horseImg = pygame.transform.scale(horseImg, (math.floor(boardWidth/size),math.floor(boardHeight/size)))
horseImg.set_colorkey((255,255,255))

#   Main class which represents a chessboard
class Board:
    #   Set necessary variables
    def __init__(self):
        self.matrix = []
        self.currentPos = ""
        self.travelHistory = []
        self.highlighted = []
        self.mousePosX = 0
        self.mousePosY = 0
        self.clickedCells = []
        self.space = False
        self.X = []

    #   Generate functional board which is used to generate graphical board
    def generateFunctionalBoard(self, grid):
        for i in range(1, size+1)[::-1]:
            col = []
            for x in range(1, size+1):
                col.append([i,x])
            grid.append(col)

    #   Check potential next step from current position
    def checkRoutes(self):
        #   Get current position
        x = int(self.travelHistory[-1][1])
        y = int(self.travelHistory[-1][0])

        #   Possible positions array set
        possiblePos = []

        #   Check steps in all directions

        #   Up and right
        newY = y - 2
        newX = x + 1
        if newY > 0 and newX < size+1 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Up and left
        newY = y - 2
        newX = x - 1
        if newY > 0 and newX > 0 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Down and right
        newY = y + 2
        newX = x + 1
        if newY < size+1 and newX < size+1 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Down and left
        newY = y + 2
        newX = x - 1
        if newY < size+1 and newX > 0 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Right and up
        newY = y - 1
        newX = x + 2
        if newY > 0 and newX < size+1 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Right and down
        newY = y + 1
        newX = x + 2
        if newY < size+1 and newX < size+1 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Left and up
        newY = y - 1
        newX = x - 2
        if newY > 0 and newX > 0 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Left and down
        newY = y + 1
        newX = x - 2
        if newY < size+1 and newX > 0 and [newY, newX] not in self.travelHistory:  #Tillåtet
            temp = [newY, newX]
            possiblePos.append(temp)
            
        #   Set possible steps as an inconstant attribute (which change depending on position)
        self.highlighted = possiblePos

    #   Set starting position
    def setStartPos(self, inp):
        #   Ex: inp = [2,"d"]
        #   Check format (length) of given position

        #   Incorrect format
        if len(inp) != 2:
            print('Wrong length of coordinate')
 
        #   Correct format
        else:
            #   Check format of position on x-axis

            try:
                letter = inp[1].upper()
                try:
                    if inp[0] in digits and letter in alph:
                        #   Correct format
                        startPos = [(alph.index(letter) + 1),((size+1)-int(inp[0]))]
                        print('Horse started at '+str(inp[0]) + str(inp[1]))
                        self.move(startPos)
                    else:
                        #   Incorrect format
                        print('Wrong format of coordinate')
                except:
                    #   Incorrect format
                    print('Wrong format of coordinate (y)')
            except:
                #   Incorrect format
                print('Wrong format of coordinate (x)')

    #   Move horse to given position
    def move(self, chosen):
        self.travelHistory.append(chosen)

    #   Draw cell on canvas
    def cell(self, x, y, w, h, color):
        pygame.draw.rect(chessDisplay, color, (x, y, w, h))
        
    #   Animate X (adds cell to animated Xs)
    def animateX(self,cell):
        self.X.append([cell,1])
        
    #   Handle mouseclick event
    def mouseClick(self, b, p):
        self.mousePosX = p[0]
        self.mousePosY = p[1]
        
        #   If left mouse click
        if(b == 1):
    
            #   If the board is empty
            if len(self.travelHistory) == 0:
                cellX = math.floor(1+(self.mousePosX-0.5*(displayWidth-boardWidth))/(boardWidth/size))
                cellY = math.floor(1+(self.mousePosY-0.5*(displayHeight-boardHeight))/(boardHeight/size))
                #   Corresponding cells to mouseclick
                if cellX > 0 and cellX < size+1 and cellY > 0 and cellY < size+1:
                    #   Add clicked cell to array
                    corrCell = [size+1-cellY,alph[cellX-1]]
                    self.clickedCells.append(corrCell)
                    
            #   If the board is not empty
            elif len(self.travelHistory) > 0:
                cellX = math.floor(1+(self.mousePosX-0.5*(displayWidth-boardWidth))/(boardWidth/size))
                cellY = math.floor(1+(self.mousePosY-0.5*(displayHeight-boardHeight))/(boardHeight/size))
                #   Corresponding cells to mouseclick
                if cellX > 0 and cellX < size+1 and cellY > 0 and cellY < size+1:
                    corrCell =  [cellX,cellY]
                    #   Move horse to clicked cell if it is highlighted
                    if corrCell in self.highlighted:
                        self.move(corrCell)
                    else:
                        self.animateX(corrCell)
                        
    #   Write something to the board
    def write(self,text,fontSize,x,y, fontColor):
        largeText = pygame.font.Font(pygame.font.get_default_font(),fontSize)
        textSurf = largeText.render(text, True, fontColor)
        textRect = textSurf.get_rect()
        textRect.center = (x,y)
        chessDisplay.blit(textSurf, textRect)

#   Main loop
def main():
    #   Generate board-object and grid
    crashed = False
    environment = Board()
    environment.generateFunctionalBoard(environment.matrix)
    
    #   Main game loop
    while not crashed:
        
        #   Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            elif event.type == pygame.KEYDOWN:
                #   If space is pressed and not the first step --> random step to one of HIGHLIGHTED cells
                #   If space is pressed and the first step --> random step to one of ALL cells
                if event.key == pygame.K_SPACE:
                    if len(environment.highlighted) > 0 and len(environment.travelHistory) > 0:
                        environment.move(environment.highlighted[random.randint(0, len(environment.highlighted) - 1)])
                    elif len(environment.travelHistory) == 0:
                        environment.move(environment.matrix[random.randint(0, size-1)][random.randint(0, size-1)])
                #   If enter is pressed and game has stopped --> restart
                if event.key == pygame.K_RETURN:
                    if len(environment.highlighted) == 0 and len(environment.travelHistory) > 0:
                        main()
            #   If mousebuttons are used --> trigger mouseclick event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                environment.mouseClick(event.button,event.pos)

        #   Draw background
        pygame.draw.rect(chessDisplay, bgColor, (0,0,displayWidth,displayHeight))
        
        #   Draw chess board
        for i in environment.matrix:
            for z in i:
                writeFootprint = False
                #   Already stepped on
                if z in environment.travelHistory: 
                    if (int(z[0]) + int(z[1])) % 2 == 0:
                        #   Light cells (set cell's color to light)
                        c = steppedOnLightCellColor
                    else:
                        #   Dark cells (set cell's color to dark)
                        c = steppedOnDarkCellColor
                    #   This variable is later used for writing footprint for this particular cell
                    writeFootprint = True
                    
                #   Not stepped on --> highlight it
                elif z in environment.highlighted:
                    if (int(z[0]) + int(z[1])) % 2 == 0:
                        #   Set color of light colored cells 
                        c = highlightColorLight
                    else:
                        #   Set color of dark colored cells 
                        c = highlightColorDark
                else:
                    #   Not stepped on and not highlighted --> draw normally
                    if (int(z[0]) + int(z[1])) % 2 == 0:
                        c = lightCellColor
                    else:
                        c = darkCellColor
                #   Draw cell with appropriate color
                environment.cell(0.5*(displayWidth-boardWidth)+(int(z[0])-1)*boardWidth/size,0.5*(displayHeight-boardHeight)+(int(z[1])-1)*boardHeight/size,boardWidth/size,boardHeight/size,c)
                #   Write footprint
                if writeFootprint:
                    environment.write(str(environment.travelHistory.index(z)),15,(0.5*boardWidth/size)+0.5*(displayWidth-boardWidth)+(int(z[0])-1)*boardWidth/size,(0.5*boardHeight/size)+0.5*(displayHeight-boardHeight)+(int(z[1])-1)*boardHeight/size,textColor)
                #   If cell exists in X array, animate X on cell as long as time left is greater than 0
                for pressedCell in environment.X:
                    if pressedCell[0] == z and pressedCell[0] != environment.travelHistory[-1] and pressedCell[1] > 0:
                        #   Coordinates for line drawings
                        sx = 0.5*(displayWidth-boardWidth)+(int(z[0])-1)*boardWidth/size
                        sy = 0.5*(displayHeight-boardHeight)+(int(z[1])-1)*boardHeight/size
                        w = boardWidth/size
                        h = boardHeight/size
                        pygame.draw.line(chessDisplay, warningColor, (sx,sy),(sx+w,sy+h),linewidth)
                        pygame.draw.line(chessDisplay, warningColor, (sx+w,sy),(sx,sy+h),linewidth)
                        #   Remove time from remaining time
                        environment.X[environment.X.index(pressedCell)][1] = environment.X[environment.X.index(pressedCell)][1] - 1/(3)
                    #   If remaining time is less than 0 --> remove cell from animated cells array
                    elif pressedCell[0] == z and pressedCell[1] < 0:
                        del environment.X[environment.X.index(pressedCell)]
                        
        #   Draw border
        pygame.draw.line(chessDisplay, borderColor, (boardWidth+0.5*(displayWidth-boardWidth),boardHeight+0.5*(displayHeight-boardHeight)), (boardWidth+0.5*(displayWidth-boardWidth),0.5*(displayHeight-boardHeight)))
        pygame.draw.line(chessDisplay, borderColor, (boardWidth+0.5*(displayWidth-boardWidth),boardHeight+0.5*(displayHeight-boardHeight)), (0.5*(displayWidth-boardWidth),boardHeight+0.5*(displayHeight-boardHeight)))
        pygame.draw.line(chessDisplay, borderColor, (0.5*(displayWidth-boardWidth),0.5*(displayHeight-boardHeight)), (0.5*(displayWidth-boardWidth),boardHeight+0.5*(displayHeight-boardHeight)))
        pygame.draw.line(chessDisplay, borderColor, (0.5*(displayWidth-boardWidth),0.5*(displayHeight-boardHeight)), (boardWidth+0.5*(displayWidth-boardWidth),0.5*(displayHeight-boardHeight)))

        #   Write letters and numbers
        for i in range(1,size+1):
            #   Letters
            environment.write(alph[i-1],20,(i-1)*boardWidth/size+0.5*(displayWidth-boardWidth)+boardWidth/(size*2),boardHeight+0.5*(displayHeight-boardHeight)+paddingTop,textColor)

            #   Numbers
            environment.write(str(int(size+1-i)),20,boardHeight+0.5*(displayHeight-boardHeight)+paddingTop,(i-1)*boardWidth/size+0.5*(displayWidth-boardWidth)+boardWidth/(size*2),textColor)

        #   If the round represents the first step --> Write instructions and await click event
        if len(environment.travelHistory) == 0:
            environment.write('Press space to step randomly',25,displayWidth/2,3*displayHeight/7,textColor)
            environment.write('Press the highlighted squares to move horse',25,displayWidth/2,4*displayHeight/7,textColor)
            pygame.display.update()
            clock.tick(60)
            #   Await event (click on first cell)
            if len(environment.clickedCells) > 0:
                environment.setStartPos(environment.clickedCells[-1])
        #   If the round does not represent the first step
        if len(environment.travelHistory) > 0:
            currentPos = environment.travelHistory[-1]
            x = (int(currentPos[0])-1)*boardWidth/size+0.5*(displayWidth-boardWidth)
            y = (int(currentPos[1])-1)*boardHeight/size+0.5*(displayHeight-boardHeight)

            #   Draw horse to designated coordinates
            rect = horseImg.get_rect()
            rect = rect.move((x, y))
            chessDisplay.blit(horseImg, rect)
            environment.checkRoutes()

            #   Check if there are no more possible moves
            if environment.highlighted == []:
                #   Draw end screen if game has stopped
                environment.write('No more possible moves ('+ str(len(environment.travelHistory))+' total moves)',35,displayWidth/2,3*displayHeight/7,textColor)
                environment.write('Press enter to restart',35,displayWidth/2,4*displayHeight/7,textColor)

            #   Update canvas
            pygame.display.flip()
            pygame.display.update()
            clock.tick(60)
main()
