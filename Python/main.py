filemap = "../maps/maps_4x_1"

"""
    1. Fonction Deplacement piece
    2. Fonction Calcul melange
    3. Fonction algorithme
"""

class puzzle_create :
    #Constructeur
    def __init__(self) :
        self.puzzle = [] 
        self.heuristique = 0 #cout + nb_cout depuis le debut
        self.cout = 0 #nombre total des distance de toute les pieces jusqu a leur destination 
        self.id = ""
        self.predecessor = ""

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    #Fonction creation map
    def create(self, size, puzzle, cout, predecessor) :
        self.puzzle = puzzle 
        self.id = setId(self.puzzle)
        self.cout = cout
        self.heuristique = self.countmelange() + self.cout
        self.predecessor = predecessor
    #fonction mise a jour
    def update(self, cout, heuristique, predecessor) :
        self.cout = cout
        self.heuristique = heuristique
        self.predecessor = predecessor
        
    def countmelange(self) :
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
      while i < size  :
          j = 0
          while j < size  :
              if puzz[i][j] != Dest[i][j] :
                  if puzz[i][j] == 0 :
                      posZero.append(i)
                      posZero.append(j)
              j += 1
          i += 1
      return posZero
    
    def adjacent(self, etat) :
      zero = self.foundEmpty()
      value = []
      if zero[0] > 0 :
          value.append("u")
      if zero[0] < size - 1 :
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
        successeur = puzzle_create()
        successeur.create(size, prevEtat.puzzle, prevEtat.cout + 1, prevEtat.id)
        if cpt == "r" :
            successeur.puzzle[tmph][tmpl] = puzzle[tmph][tmpl + 1]
            successeur.puzzle[tmph][tmpl + 1] = "0"
        elif cpt == "u" :
            successeur.puzzle[tmph][tmpl] = puzzle[tmph - 1][tmpl]
            successeur.puzzle[tmph - 1][tmpl] = "0"
        elif cpt == "d" :
            successeur.puzzle[tmph][tmpl] = puzzle[tmph + 1][tmpl]
            successeur.puzzle[tmph + 1][tmpl] = "0"
        elif cpt == "l" :
            successeur.puzzle[tmph][tmpl] = puzzle[tmph][tmpl - 1]
            successeur.puzzle[tmph][tmpl - 1] = "0"
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

def get_F_min(listSuccesseurs) :
  tmp = []
  first = 1
  for i in listSuccesseurs :
    if first == 1 :
      tmp = i
      first = 0
    elif i.heuristique < tmp.heuristique : 
      tmp = i

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


def algorithme_a_star(Start, Dest) : 
  openList = []
  openList.append(Start)
  openList.append(Start)
  closedList = []
  i = 0
  while openList[i] and openList[i].id != idDest :
    nbSucces = 0
    successeurs = getSuccesseurs(openList[i])
    fmin = get_F_min(successeurs)
    while successeurs[nbSucces] != null :
      if nbSucces == 0:
        closedList.append(successeurs[nbSucces])
      else :
        if search_etat(successeurs[nbSucces], closedList) == -1 and currentCout < prevcout :
          successseur[nbSucces].heuristique = openList[i].
          successeurs[nbSucces].predecessor = openList[i].id
                  
algorithme_a_star(Start, Dest)
