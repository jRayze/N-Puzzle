filemap = "../maps/maps_4x_1"

"""
    1. Fonction Deplacement piece
    2. Fonction Calcul melange
    3. Fonction algorithme
"""

class puzzle_create :
    #Constructeur
    def __init__(self) :
        self.size = 0
        self.puzzle = [] 
        self.stack = []#liste des puzzle possible a partir du point de depart
        self.heuristique = 0
        self.cout = 0 //nombre total des distance de toute les pieces jusqu a leur destination 
        self.dest = []
        self.id = 0
    #Fonction creation map
    def create(self, size, puzzle) :
        self.size = size
        self.puzzle = puzzle
        self.id = self.setId(puzzle)
        self.dest = self.solution(size)
        self.melange = self.countmelange()
    #fonction mise a jour
    def update(self, puzzle, cout, heuristique) :
        self.stack.append({"puzzle" : puzzle, "cout" : cout, "heuristique" : cout })
        self.cout = cout
        self.heuristique = heuristique
    #fonction solution puzzle
    def solution(self, size) :
        dest = []
        index = 1
        x = 0
        y = 0
        i = 0
        while i < size :
            dest.append([0] * size)
            i += 1 
        distance = size - 1 #premiere ligne distance = size ensuite on fait 2 * size - 1 en boucle
        move = 0
        status = 1
        direction = 6 #gauche = 4 / droite = 6 / haut = 8 / bas = 2
        while index < (size * size) :
            dest[x][y] = index
            if move == distance :
                if status == 1 :
                    distance = distance - 1
                    status = 0
                else :
                    status = 1
                move = 0
                direction = 2 if direction == 6 else 4 if direction == 2 else 8 if direction == 4 else 6
            else : 
                move += 1
            if direction == 4 :
                y -= 1
            elif direction == 6 :
                y += 1
            elif direction == 8 :
                x -= 1
            elif direction == 2 :
                x += 1
            index += 1
        print_map(dest, "solution")
        return dest
        
    def countmelange(self) :
        puzz = self.puzzle
        i = 0
        melange = 0
        while i < self.size  :
            j = 0
            while j < self.size  :
                if puzz[i][j] != self.dest[i][j] :
                    if puzz[i][j] != 0 :
                        melange += searchDest(puzz[i][j], i, j)
                j += 1
            i += 1
        return melange
    
    def searchDest(self, value, x, y):
      i = 0
      mélange = 0
      while i < self.size :
         j = 0
         while j < self.size :
            if self.dest[i][j] == value :
               return x > i ? x - i : i - x + y > j ? y - j : j - y
            j += 1
         i += 1
      return 0

    def foundEmpty(self) :
        puzz = self.puzzle
        i = 0
        posZero = []
        while i < self.size  :
            j = 0
            while j < self.size  :
                if puzz[i][j] != self.dest[i][j] :
                    if puzz[i][j] == 0 :
                        posZero = [i, j]
                j += 1
            i += 1
        return posZero
    
    def moving(self, puzzle) :
        zero = self.foundEmpty
        value = []
        if zero[0] > 0 :
            value.append("u")
        if zero[0] < size - 1 ;
            value.append("d")
        if zero[1] > 0 :
            value.append("l")
        if zero[1] < size - 1 :
            value.append("r")
        puzzle = self.createMove(puzzle, value, zero)

    def createMove(puzzle, value, zero) :
        tmph = zero[0] 
        tmpl = zero[1]
        for cpt in value :
            if value[cpt] == "r" :
                puzzle[tmph][tmpl] = puzzle[tmph][tmpl + 1]]
                puzzle[tmph][tmpl + 1]] = "0"
            elif value[cpt] == "u" :
                puzzle[tmph][tmpl] = puzzle[tmph - 1][tmpl]]
                puzzle[tmph - 1][tmpl]] = "0"
            elif value[cpt] == "d" :
                puzzle[tmph][tmpl] = puzzle[tmph + 1][tmpl]]
                puzzle[tmph + 1][tmpl]] = "0"
            elif value[cpt] == "l" :
                puzzle[tmph][tmpl] = puzzle[tmph][tmpl - 1]]
                puzzle[tmph][tmpl - 1]] = "0"


def print_map(puzzle, message) :
    print("Map :", message) 
    for i in puzzle :
        print(i)

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

print_map(puzzle, "")
puzclass = puzzle_create()
puzclass.create(size, puzzle)
puzclass.update(puzzle, 0, 0)
print(puzclass.foundZero())

Start = puzclass

def algorithme_a_star(Start, Dest) : 
    closedList = []
    openList = openList.append(Start)
    i = 0
    while openList[i] != null && openList[i].tab != Dest :
        x = get_F_min(openList[i].tab)
        cpt = 0
        while x[cpt] :
            if cpt == 0:
                closedList.append(x[cpt])
            else :
                if search_etat(x[cpt], closedList) == false && currentCout < prevcout :
                    x[cpt].predecessor = openList[i].