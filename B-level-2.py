#   Import modules
import random, math

#   Global variables (constants) and styling for board
alph = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
digits = range(1,len(alph)+1)

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

#   Main class which represents a chessboard
class Board:
    #   Set necessary variables
    def __init__(self):
        self.matrix = []
        self.currentPos = ""
        self.travelHistory = []
        self.highlighted = []

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
            #   Correct format
            try:
                letter = inp[1].upper()
                try:
                    if int(inp[0]) in digits and letter in alph:
                        startPos = [(alph.index(letter) + 1),((size+1)-int(inp[0]))]
                        self.move(startPos)
                    else:
                        print('Wrong format of coordinate')
                except:
                    print('Wrong format of coordinate (y)')
            #   Incorrect format
            except:
                print('Wrong format of coordinate (x)')

    #   Move horse to given position
    def move(self, chosen):
        self.travelHistory.append(chosen)

#   Main loop
def main(sp):
    #   Generate board-object and grid
    environment = Board()
    environment.generateFunctionalBoard(environment.matrix)
    environment.setStartPos(sp)
    #   Main game loop
    while True:
        environment.checkRoutes()
        #   Check if there are no more possible moves
        if environment.highlighted == []:
            return environment.travelHistory
        environment.move(environment.highlighted[random.randint(0, len(environment.highlighted)-1)])

possible_games = []
cells = []

for i in range(1, size+1)[::-1]:
  for x in range(1, size+1):
    cells.append(str(i) + str(alph[x-1]))
  
i = m = 0

for x in cells:
    ok = True
    while ok:
        th = main(x)
        if th not in possible_games:
            possible_games.append(th)
            #print('Generated length: '+str(len(th)) + ', longest game so far: '+str(m))
            if len(th) >= m:
                m = len(th)
            if len(th) >= size**2-4 and len(th) >= m:
                print('Length '+str(len(th)))
                for i in range(len(th)):
                    th[i] = str(th[i][0]) + alph[int(th[i][1])-1]
                print(th)
                ok = False
#winner = ['18', '37', '25', '13', '34', '55', '63', '51', '32', '11', '23', '15', '27', '48', '36', '17', '38', '57', '78', '66', '45', '53', '72', '84', '76', '68', '87', '75', '83', '71', '52', '31', '12', '24', '43', '22', '14', '26', '47', '28', '16', '35', '54', '46', '58', '77', '65', '44', '56', '64', '85', '73', '81', '62', '41', '33', '21', '42', '61', '82', '74', '86', '67', '88']
