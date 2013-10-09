#Sudoku.py
#An AI solver of one of the only games on the planet Kai will actively do

'''
SUDOKU SOLVER
Solves easy, medium, and kind of hard...
But hey, most people cannot even get to that level
So this guy is fairly normal

INSTRUCTIONS:
When running, enter in text file via 'quote.txt'
If you do not have a file,
Enter in sequence of numbers via text file
Of the format: **n*nn***
Where n is a number and * is a '*' or an empty space
There should be 9 rows - add extra space at the end
(so your txt file would be 10 lines long)
Finding coordinates on Sudoku map should be down-across
NOTE: EVERYTHING IS A STRING
'''

class Sudoku():
    def __init__(self, file_in):
        """
        INITIALIZE
            Creates a new puzzle based on the input file (file_in)
            Puzzle extensions include:
                puzzle = DICTIONARY, the puzzle trying to be solves
                memory = LIST of DICT, containing the memory of the last number
                    safely input without any overlap
                solved = DICT, the empty spaces
        """
        #No specific methods to modify this, but is constantly being updated
        self.puzzle = self.getPuzzle(file_in)
        
        #All class methods work to modify this
        #Initialize with the first base case memory (state 0 = unsovlved)
        self.memory = [self.puzzle]
        
        self.tosolve = allprop(self.toFind(), self.puzzle)
        
    def getPuzzle(self, filen):
        """
        RETURNS DICTIONARY {(x, y, z): n}
            Each number space is given coordinates via tuple, 
            x = row, y = column, z = cube the number is in
        filen = STRING, file name
        """
        f = open(filen, 'r')
        parf = {}
        
        maxel = 0 #Which row in file we are on (0-8)
        for line in f:
            sep_num = list(line)
            sep_num.pop() #Remove /n new line segment
            for pos in range(len(sep_num)):
                coord = (maxel+1, pos+1, findCube(maxel+1, pos+1))
                parf[coord] = sep_num[pos]
            maxel = maxel + 1
        
        return parf

    def toFind(self):
        """
        RETURNS INT
            Figures out how many spaces need to be solved at __init__
        """
        t = {}
        for key in self.puzzle:
            if self.puzzle[key] == '*':
                t[key] = '*'
        return t

    def update(self, update):
        """
        MODIFIES puzzle, memory, to solve
        Updates everything
        """
        self.memory.append(self.puzzle)
        self.puzzle = update
        self.tosolve = allprop(self.toFind(), self.puzzle)
    
    def pop_memory(self):
        """
        MODIFIES self.puzzle
            Pops the last item of the memory list
            And sets self.puzzle back one step
        """
        self.puzzle = self.memory.pop()
    
        
def findCube(x, y):
    """
    RETURNS INT (z)
        Determines the corresponding cube the number is in
    x = row
    y=column
    """
    if x < 4:
        #Top cubes
        if y < 4:
            return 1
        elif y > 3 and y < 7:
            return 2
        else:
            return 3
    elif x > 3 and x < 7:
        #Middle Cubes
        if y < 4:
            return 4
        elif y > 3 and y < 7:
            return 5
        else:
            return 6
    else:
        #Bottom cubes
        if y < 4:
            return 7
        elif y > 3 and y < 7:
            return 8
        else:
            return 9

def getRow(x, dict_coord):
    """
    RETURNS DICT
        Extracts a dictionary where all elements are in the same row
    x = row coordinate (top down)
    """
    row_dict = {}
    for coord in dict_coord:
        if coord[0] == x:
            row_dict[coord] = dict_coord[coord]
    
    return row_dict

def getCol(y, dict_coord):
    """
    RETURNS DICT
        Extracts a dictionary where all elements are in the same column
    y = row coordinate (left right)
    """
    col_dict = {}
    for coord in dict_coord:
        if coord[1] == y:
            col_dict[coord] = dict_coord[coord]
    
    return col_dict

def getCube(z, dict_coord):
    """
    RETURNS DICT
        Extracts a dictionary where all elements are in the same row
    z = cube coordinate (type writer)
    """
    cube_dict = {}
    for coord in dict_coord:
        if coord[2] == z:
            cube_dict[coord] = dict_coord[coord]
    
    return cube_dict

def sweepPart(coord, dict_coord):
    """
    RETURNS BOOLEAN
        Sweeps through a row to make sure all numbers are unique
    dict_coord = DICTIONARY where (x, *, *), (*, y, *), (*,*,z)
    """
    for cd in dict_coord:
        #For each element in the dictionary row/col/cube
        if dict_coord[cd] != '*' and cd != coord:
            if dict_coord[cd] == dict_coord[coord]:
                return False
    return True

def sweep(coord, dictxyz):
    """
    RETURNS BOOLEAN
        Goes through all columns, rows, and cubes to make sure
        coordinates value is not shared in the same row/col/cube
    coord = TUPLE (x, y, z)
    dictxyz = DICTIONARY {puzzle data}
    """
    x, y, z = coord
    #Booleans
    #print 'row'
    tempx = sweepPart(coord, getRow(x, dictxyz))
    #print 'col'
    tempy = sweepPart(coord, getCol(y, dictxyz))
    #print 'cube'
    tempz = sweepPart(coord, getCube(z, dictxyz))
    
    #print dictxyz[coord], ':', x, tempx, y, tempy, z, tempz
    
    if tempx == True: 
        if tempy == True:
            if tempz == True:
                return True
    return False

def plug(n, coord, dictxyz):
    """
    RETURNS BOOLEAN
        Puts a number in an empty space
        Then sweeps entire dictionary to ensure it is not
        Overlapping with anything
    n = the number in question
    coord = TUPLE (x,y,z)
    dictxyz = DICT, the master puzzle
    """
    dictxyz[coord] = n
    isopen = sweep(coord, dictxyz)
    dictxyz[coord] = '*'
    return isopen

def allprop(dict_open, dictxyz):
        """
        RETURNS DICTIONARY (updated version with all probabilities
            Figures out all possible numbers that can fill a space
        """
        for key in dict_open:
            #make copy of original puzzle
            coord = []
            for i in range(9):
                n = str(i+1)
                dictxyz[key] = n
                if sweep(key, dictxyz):
                    coord.append(n)
                dictxyz[key] = '*'
            dict_open[key] = coord

        return dict_open
        
def extract(dict_open, dictxyz):
    """
    RETURNS BOOLEAN, DICTIONARY
        Takes all coordinates that only have one possibility,
        Extracts that number and puts it in the new list
    """
    nosing = False
    for cd in dict_open:
        if len(dict_open[cd]) == 1:
            temp = dict_open[cd]
            dictxyz[cd] = temp[0]
            nosing = True
    
    return nosing, dictxyz

def dictToList(dictn):
    """
    RETURNS LIST [( (x,y,z) , n )]
        Converts a dictionary to a sorted list of tuples
    """
    n = []
    for key in dictn:
        #print key, dictn[key]
        n.append( (key, dictn[key]) )
    n.sort()
    
    return n

def toRow(x, listxyz):
    """
    RETURNS STRING
        Converts a section of list to a row
    """
    row = ''
    for i in listxyz:
        xyz, n = i
        if xyz[0] == x:
            row = row + ' ' + n
    return row

def prntFin(listxyz):
    """
    PRINTS EVERYTHING
        Yeah...snazy formatting too
    """  
    for x in range(9):
        n = x+1
        print toRow(n, listxyz)

def trysweep(s, max):
    """
    RETURNS DICTIONARY
        Tests out an iteration of a specific list
    """
    n = 0
    while len(s.tosolve) != 0 and n != max:
        sing, newd = extract(s.tosolve, s.puzzle)
        if sing:
            s.update( newd )
        else:
            guess(1, s, max)
        n += 1
    
    for cd in s.tosolve:
        if len(s.tosolve[cd]) == 0 and len(s.memory) != 0:
            s.pop_memory()
   
def guess(it, objxyz, max):
    """
    RETURNS DICTIONARY
        Randomly guesses a number before preceding
    it = iteration, this can be recursive
    dict_open = avalible spaces and probabilities
    dictxyz = object passed through with the puzzle and all info
    """
    temp = objxyz.tosolve
    for cd in temp:
        num = temp[cd]
        for i in range(len(temp[cd])):
            tester = objxyz
            tester.puzzle[cd] = num[i]
            tester.update(tester.puzzle)
            trysweep(tester, max)
            
            if len(tester.tosolve) == 0:
                break
            
            tester.puzzle[cd] = '*'
            if it >= 45:
                break
            it += 1
            
        if len(objxyz.tosolve) == 0:
                break
        if it >= 45:
                break
   
    
def solve(filen, max):
    """
    Runs the program
    """
    s = Sudoku(filen)
    n = 0
    #max is how many itterations is allowed
    while len(s.tosolve) != 0 and n != max:
        sing, newd = extract(s.tosolve, s.puzzle)
        if sing:
            s.update( newd )
        else:
            guess(1, s, max)
        n += 1
    
    print s.tosolve
    final = dictToList(s.puzzle)
    prntFin(final)
    

if __name__ == "__main__":
    filen = input('Enter file name in quotes: ')
    solve(filen, 100)
