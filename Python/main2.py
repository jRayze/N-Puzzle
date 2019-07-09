filemap = "map3x3"
import copy
import time
"""
    1. Fonction Deplacement piece               
    2. Fonction Calcul melange
    3. Fonction algorithme
"""

start_time = time.time()

class puzzle_create :
    #Constructeur
    def __init__(self) :
        self.puzzle = [] 
        self.heuristique = 0 #cout + nb distance de chaques pieces mal palces
        self.cout = 0 #nombre total des distance de toute les pieces jusqu a leur destination 
        self.id = ""
        self.predecessor = ""

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    #Fonction creation map
    def create(self, size, puzzle, cout, predecessor) :
        self.puzzle = puzzle
        self.id = setId(puzzle)
        self.cout = cout
        self.heuristique = self.manhattan() +  self.linear_conflicts(self.puzzle, Dest) + self.cout
        self.predecessor = predecessor
    #fonction mise a jour
    def update(self, cout, heuristique, predecessor) :
        self.cout = cout
        self.heuristique = heuristique
        self.predecessor = predecessor
        
    def manhattan(self) :
        puzz = self.puzzle
        i = 0
        melange = 0
        while i < size  :
            j = 0
            while j < size  :
                if puzz[i][j] != Dest[i][j] :
                    if puzz[i][j] != 0 :
                        melange += self.searchDest(puzz[i][j], i, j)
                j += 1
            i += 1
        return melange

    def hamming(self) :
        puzz = self.puzzle
        i = 0
        melange = 0
        while i < size  :
            j = 0
            while j < size  :
                if puzz[i][j] != Dest[i][j] :
                    if puzz[i][j] != 0 :
                        melange += 1
                j += 1
            i += 1
        return melange
    
    def linear_conflicts(self, array_2D_1, array_2D_2) :
        LinearConflict = 0
        for x in range(0,size):
	        counter = 0
	        temp = []
	        for y in range(0,size) :
	            if array_2D_1[x][y] in array_2D_2[x] :
	                temp.append(array_2D_1[x][y])
	                counter += 1
	        if counter == 2 :
	            G1 = array_2D_2[x].index(temp[0])
	            G2 = array_2D_2[x].index(temp[1])
	            L1 = array_2D_1[x].index(temp[0])
	            L2 = array_2D_1[x].index(temp[1])
	            if (G1-G2>0 and L1-L2<0) or (G1-G2<0 and L1-L2>0) :
	                LinearConflict += 1
	        if counter == 3 :
	            G1 = array_2D_2[x].index(temp[0])
	            G2 = array_2D_2[x].index(temp[1])
	            G3 = array_2D_2[x].index(temp[2])
	            L1 = array_2D_1[x].index(temp[0])
	            L2 = array_2D_1[x].index(temp[1])
	            L3 = array_2D_1[x].index(temp[2])
	            if (G1-G2>0 and L1-L2<0) or (G1-G2<0 and L1-L2>0) :
	                LinearConflict += 1
	            if (G1-G3>0 and L1-L3<0) or (G1-G3<0 and L1-L3>0) :
	                LinearConflict += 1
	            if (G3-G2>0 and L3-L2<0) or (G3-G2<0 and L3-L2>0) :
	                LinearConflict += 1
        return LinearConflict

    
    def searchDest(self, value, x, y):
      i = 0
      while i < size :
         j = 0
         while j < size :
            if Dest[i][j] == value :
               return (x - i if x > i else i - x) + (y - j if y > j else j - y)
            j += 1
         i += 1
      return 0

    def foundEmpty(self) :
      puzz = self.puzzle
      i = 0
      posZero = []
      while i < size :
          j = 0
          while j < size :
            if puzz[i][j] == 0 :
                posZero.append(i)
                posZero.append(j)
                break
            j += 1
          i += 1
      return posZero
    
    def adjacent(self, etat) :
        zero = self.foundEmpty()
        #print("zero =", zero)
        value = []
        if zero[0] > 0 :
            value.append("u")
        if zero[0] < size - 1:
            value.append("d")
        if zero[1] > 0 :
            value.append("l")
        if zero[1] < size - 1 :
            value.append("r")
        return createMove(etat, value, zero)

def setId(puzzle) :
    i = 0
    id = ""
    while i < size :
        j = 0
        while j < size :
            id += str(puzzle[i][j])
            j += 1
        i += 1
    return id


def createMove(prevEtat, value, zero) :
    tabSuccesseur = []
    tmph = zero[0] 
    tmpl = zero[1]
    for cpt in value :
        puzzle = copy.deepcopy(prevEtat.puzzle)
        if cpt == "r"  :
            puzzle[tmph][tmpl] = prevEtat.puzzle[tmph][tmpl + 1]
            puzzle[tmph][tmpl + 1] = 0
        elif cpt == "u" :
            puzzle[tmph][tmpl] = prevEtat.puzzle[tmph - 1][tmpl]
            puzzle[tmph - 1][tmpl] = 0
        elif cpt == "d" :
            puzzle[tmph][tmpl] = prevEtat.puzzle[tmph + 1][tmpl]
            puzzle[tmph + 1][tmpl] = 0
        elif cpt == "l" :
            puzzle[tmph][tmpl] = prevEtat.puzzle[tmph][tmpl - 1]
            puzzle[tmph][tmpl - 1] = 0
        if setId(puzzle) != prevEtat.predecessor :
            successeur = puzzle_create()
            successeur.create(size, puzzle, prevEtat.cout + 1, prevEtat.id)
            tabSuccesseur.append(successeur)
    return tabSuccesseur

#fonction solution puzzle
def solution(size) :
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

def getSuccesseurs(etat) :
  listSuccesseurs = []
  listSuccesseurs = etat.adjacent(etat)
  return listSuccesseurs

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

print_map(puzzle, "Start")

Dest = solution(size)
idDest = setId(Dest)
puzclass = puzzle_create()
puzclass.create(size, puzzle, 0, 0)
print(puzclass.foundEmpty())

Start = puzclass

print("start =")
print(Start)
print("Dest =")
print(Dest)

def getCout(etat1, etat2) :
    for elem in etat2 :
        if elem.id == etat1.id :
            return elem.cout
    return -1

def getCoutDict(etat1, etat2) :
    if not etat2 :
        return -1
    elif etat1.id in etat2  :
        return etat2[etat1.id].cout
    return -1

def retracePath(etat, listeOpen, listeClosed, start, nbCout) :
    nbCout += 1
    if etat.id == start.id :
        print(nbCout)
        print("deplacements")
        return 
    for elem in listeOpen :
        if etat.predecessor == elem.id :
            print_map(elem.puzzle, "chemin")
            return retracePath(elem, listeOpen, listeClosed, start, nbCout)
    for elem in listeClosed :
        if etat.predecessor == elem.id :
            print_map(elem.puzzle, "chemin")
            return retracePath(elem, listeOpen, listeClosed, start, nbCout)

def getMinDict (openList) :
    identifiant = "0"
    heuristique = 0
    cout = 0
    for elem in openList.values() :
        if identifiant != "0" :
            if heuristique > elem.heuristique or (heuristique == elem.heuristique and cout > elem.cout) :
                identifiant = elem.id
                heuristique = elem.heuristique
                cout = elem.cout
        else :
            identifiant = elem.id
            heuristique = elem.heuristique
            cout = elem.cout
    return openList[identifiant]


def algorithme_a_star(Start, Dest) :
    closedList = {}
    openList = {}
    openList[Start.id] =  Start
    #mini = Start
    while openList :
        #currentEtat = openList[mini.id]
        currentEtat = getMinDict(openList)
        #print(currentEtat)
        if currentEtat.id == idDest :
            print("FIN !")
            print_map(currentEtat.puzzle, "")
           # retracePath(currentEtat, openList, closedList, Start, 0)
            return 1
        successeurs = getSuccesseurs(currentEtat)
        for elem in successeurs :
            currentCout = elem.cout
            prevClosedCout = getCoutDict(elem, closedList)
            prevOpenCout = getCoutDict(elem, openList)
            if not ((prevClosedCout != -1 and prevClosedCout < currentCout) or (prevOpenCout != -1 and prevOpenCout < currentCout)) :
                openList[elem.id] = elem
        closedList[currentEtat.id] = currentEtat
        del openList[currentEtat.id]
        #mini = tmpMini
    return -1

if algorithme_a_star(Start, Dest) == -1 :
    print("ERROR")
else :
    print("SUCCESS")



elapsed_time = time.time() - start_time
print(elapsed_time)
