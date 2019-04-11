filemap = "../maps/map1"

"""
    1. Fonction Deplacement piece
    2. Fonction Calcul melange
    3. Fonction algorithme
"""

def print_map(puzzle) :
    print("Map :") 
    for i in puzzle :
        print(i)
class puzzle_create :
    #Constructeur
    def __init__(self) :
        self.size = 0
        self.puzzle = []
    #Fonction creation map
    def create(self, size, puzzle) :
        self.size = size
        self.puzzle = puzzle
    def create_piece( ):

class piece :
    def __init__(self) :
        self.dest = {'height': 0, 'width' : 0}
        self.pos = {'height': 0, 'width' : 0}
        self.status = 0
        self.value = 0
    
    def getInfo(self, posX, posY, value) :
        self.pos = {'height': posX, 'width' : poxY}
        self.dest = destination(value)
        self.value = value

    def destination(self, value):
        dest = [0, 0]
        if (value == 0)
            dest = [(puzzle_create.size / puzzle_create.size ) - 1, (puzzle_create.size / puzzle_create.size) - 1]
        if (value == 1)
            dest = [0, 0]
        else
            dest = [(value / puzzle_create.size), (value / puzzle_create.size)]
        return dest

with open(filemap) as fd:
    i = 0
    line = fd.readline()
    count = 1
    height = 0
    width = 0
    size = 0
    puzzle = []
    while line :
        value = line.strip()
        if count == 2 :
            size = int(value)
            while i < size :
                puzzle.append([0] * size)
                i += 1 
        elif count > 2 :
            if width < size :
                puzzle[height][width] = int(value)
            if width == int(size) - 1 :
                width = 0
                height += 1
                
            else :
                width += 1
        line = fd.readline()
        count += 1

print_map(puzzle)
puzclass = puzzle_create()
puzclass.create(size, puzzle)
print(puzclass.size)
