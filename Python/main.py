filemap = "../maps/map4x2"
import copy
import time
"""
    1. Fonction Deplacement piece               
    2. Fonction Calcul melange
    3. Fonction algorithme
"""

start_time = time.time()

class Node :
    def __init__(self, etat) :
        self.left = None
        self.right = None
        self.parent = None
        self.etat = etat

    def __iter__(self):
        if self.left:
            for node in self.left:
                yield node
        yield self.etat
        if self.right:
            for node in self.right:
                yield node

    def __getitem__(self, Id):
        node = self.get(Id)
        if node:
            return node
        raise KeyError(Id)

    def insert(self, etat) :
        if etat.heuristique < self.etat.heuristique or (etat.heuristique == self.etat.heuristique and etat.cout < self.etat.cout) :
            if self.left is None :
                self.left = Node(etat)
                self.left.parent = self
            else :
                self.left.insert(etat)
        elif etat.heuristique > self.etat.heuristique or (etat.heuristique == self.etat.heuristique and etat.cout > self.etat.cout) :
            if self.right is None :
                self.right = Node(etat)
                self.right.parent = self
            else :
                self.right.insert(etat)
        else :
            if etat.heuristique == self.etat.heuristique and etat.cout == self.etat.cout :
                if etat.id != self.etat.id :
                    if self.right is None :
                        self.right = Node(etat)
                        self.right.parent = self
                    else :
                        self.right.insert(etat)
    
    def showInfix(self, level = 0) :
        if self.right:
            self.right.showInfix(level + 1)
            print (f"{' ' * 4 * level}{self.etat}")
        if self.left:
            self.left.showInfix(level + 1)
    
    def count_children(self):
        return bool(self.left) + bool(self.right)

    def get(self, etat):
        if etat.heuristique < self.etat.heuristique :
            return self.left.get(etat) if self.left else None
        elif etat.heuristique > self.etat.heuristique :
            return self.right.get(etat) if self.right else None
        else :
            if etat.cout < self.etat.cout :
                return self.left.get(etat) if self.left else None
            elif etat.cout > self.etat.cout :
                return self.right.get(etat) if self.right else None
            else :
                if etat.id == self.etat.id :
                    return self
        return None
    
    def getPredecById(self, idP, level = 0) :
        if self.right:
            self.right.getPredecById(idP, level + 1)
            if self.etat.id == idP :
                return self
        if self.left:
            self.left.getPredecById(idP, level + 1)

    def getId(self, etat):
        if etat.heuristique < self.etat.heuristique :
            return self.left.get(etat) if self.left else None
        elif etat.heuristique > self.etat.heuristique :
            return self.right.get(etat) if self.right else None
        return self.etat.id
    
    def getHeuristique(self, etat):
        if etat.heuristique < self.etat.heuristique :
            return self.left.get(etat) if self.left else None
        elif etat.heuristique > self.etat.heuristique :
            return self.right.get(etat) if self.right else None
        return self.etat.heuristique

    def min(self):
        node = self
        while node.left:
            node = node.left
        return node
    
    def is_left_child(self):
        return self.parent and self is self.parent.left
    
    def is_right_child(self):
        return self.parent and self is self.parent.right

    def get_successor(self):
        if self.right:
            return self.right.min()
        node = self
        while node.is_right_child():
            node = node.parent
        return node.parent

    def get_predecessor(self):
        if self.left:
            return self.left.max()
        node = self
        while node.is_left_child():
            node = node.parent
        return node.parent
    
    def delete(self, etat):

        node = self.get(etat)
       # print("test")
        if not node:
            return
        #print("test2")

        children_count = node.count_children()

        if children_count == 0:
            if node.is_left_child():
                if node.parent != None :
                    node.parent.left = None
            else:
                if node.parent != None :
                    node.parent.right = None
            #print(node)
            del node

        elif children_count == 1:
            child = node.left or node.right
            if node.is_left_child():
                node.parent.left = child
                child.parent = node.parent
                #print(node)
                del node
            elif node.is_right_child():
                node.parent.right = child
                child.parent = node.parent
                #print(node)
                del node
            else:
                root = node
                root.etat = child.etat
                root.left = child.left
                root.right = child.right
                if child.left:
                    child.left.parent = root
                if child.right:
                    child.right.parent = root
                #print(child)
                del child

        else:
            succ = node.get_successor()
            node.etat = succ.etat
            if succ.is_left_child():
                succ.parent.left = succ.right
            else:
                succ.parent.right = succ.right
            if succ.right:
                succ.right.parent = succ.parent
            #print(node)
            del succ


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

def compare(etat1, etat2) :
    if etat1.heuristique < etat2.heuristique :
        return 1
    elif etat1.heuristique == etat2.heuristique :
        return 0
    else :
        return -1

def insertSort(olist, elem) :
    found = 0
    index = 0
    lenght = len(olist)
    for i in range(0, lenght) :
        if (olist[i].heuristique < elem.heuristique or (olist[i].heuristique == elem.heuristique and olist[i].cout < elem.cout)) :
            if (i + 1) < lenght :
                if (olist[i + 1].heuristique > elem.heuristique or (olist[i + 1].heuristique  == elem.heuristique and olist[i + 1].cout > elem.cout)) :
                    index = i + 1
                    found = 1
                    break
        i += 1
    if (found == 0) :
        olist.append(elem)
    else :
        olist.insert(index, elem)
    return olist
    

def insertionSort(list) :
    for i in range(1, len(list)) :
        key = list[i]
        j = i - 1
        while j >= 0 and (list[j].heuristique > key.heuristique or (list[j].heuristique == key.heuristique and list[j].cout > key.cout)) :
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = key
    return list 

def get_pos_elem_in_list(list, etat) :
    posx = 0
    for elem in list :
        if elem.id == etat.id :
            return posx
        posx += 1
    return -1

def getCout(etat1, etat2) :
    for elem in etat2 :
        if elem.id == etat1.id :
            return elem.cout
    return -1

def retracePath(etat, listeOpen, listeClosed, start, nbCout) :
    nbCout += 1
    if etat.id == start.id :
        print(nbCout)
        print("deplacements")
        return
    elem = listeOpen.getPredecById(etat.predecessor)
    if elem != None :
        print_map(elem.etat.puzzle, "chemin")
        return retracePath(elem.etat, listeOpen, listeClosed, start, nbCout)

    for elem in listeClosed :
        if etat.predecessor == elem.id :
            print_map(elem.puzzle, "chemin")
            return retracePath(elem, listeOpen, listeClosed, start, nbCout)

"""
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

def algorithme_a_star(Start, Dest) : 
    closedList = []
    openList = []
    openList.append(Start)
    while openList :
        currentEtat = openList[0]
        if currentEtat.id == idDest :
            print("FIN !")
            print_map(currentEtat.puzzle, "")
            retracePath(currentEtat, openList, closedList, Start, 0)
            return 1
        successeurs = getSuccesseurs(currentEtat)
        openList.pop(0)
        for elem in successeurs :
            currentCout = elem.cout
            prevClosedCout = getCout(elem, closedList)
            prevOpenCout = getCout(elem, openList)
            if not (prevClosedCout != -1 and prevClosedCout < currentCout) or (prevOpenCout != -1 and prevOpenCout < currentCout) :
                elem.update(currentEtat.cout + 1, currentEtat.cout  + 1 + elem.linear_conflicts(elem.puzzle, Dest) + elem.manhattan(), currentEtat.id)
                if prevOpenCout == -1 :
                    if currentEtat.heuristique > elem.heuristique or (currentEtat.heuristique == elem.heuristique and currentEtat.cout > elem.cout) :
                        openList.insert(0, elem)
                    else :
                        openList.append(elem)
                        openList = insertionSort(openList)
                        #openList = insertSort(openList, elem)
                else :
                    openList[get_pos_elem_in_list(openList, elem)].update(elem.cout, elem.heuristique, elem.predecessor)
                    openList = insertionSort(openList)
        closedList.append(currentEtat)
       # print_map(openList[0].puzzle, "Heuristique faible")
        #print("cout = ", openList[0].cout, "heuristique = ", openList[0].heuristique)
    return -1 """

def algorithme_a_star(Start, Dest) : 
    closedList = []
    openList = Node(Start)
    while openList :
        currentEtat = openList.min().etat
        #print(currentEtat)
        if currentEtat.id == idDest :
            print("FIN !")
            print_map(currentEtat.puzzle, "")
            print(currentEtat.cout)
          #  retracePath(currentEtat, openList, closedList, Start, 0)
            return 1
        successeurs = getSuccesseurs(currentEtat)
        openList.delete(currentEtat)
        #print("lool")
        #print(openList.showInfix())
        #print("looooool")
        
        for elem in successeurs :
            currentCout = elem.cout
            prevClosedCout = getCout(elem, closedList)
            prevOpenCout = openList.get(elem)
            if not (prevClosedCout != -1 and prevClosedCout < currentCout) or (prevOpenCout != None and prevOpenCout.etat.cout < currentCout) :
                elem.update(currentEtat.cout + 1, currentEtat.cout  + 1 + elem.linear_conflicts(elem.puzzle, Dest) + elem.manhattan(), currentEtat.id)
                if prevOpenCout == None :
                    openList.insert(elem)
                else :
                    openList.delete(elem)
                    openList.insert(elem)
               # print("loool")
        closedList.append(currentEtat)
       # print_map(openList.min().etat.puzzle, "Heuristique faible")
       # print("cout = ", openList.min().etat.cout, "heuristique = ", openList.min().etat.heuristique)
    return -1

if algorithme_a_star(Start, Dest) == -1 :
    print("ERROR")
else :
    print("SUCCESS")



elapsed_time = time.time() - start_time
print(elapsed_time)
