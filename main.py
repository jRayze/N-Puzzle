import copy
import time
import sys
import re
#import tkinter as tk
from heapq import heappop, heappush, _siftdown, heapify
#from tkinter import *
#from PIL import Image, ImageTk

##############################################affichage fenetre###################################

class Taquin() :
    def __init__(self, puzzle, Dest, size) :
        """Tk.__init__(self)
        self.title("Npuzzle")
        self.geometry("1080x720")
        self.minsize(1080,720)
        self.maxsize(1080, 720)
        self.config(background='#536878')
        self.frame = Frame(self, bg='#536878', bd=1, relief=SUNKEN)
        self.label_title = Label(self, text="N-puzzle", font=("Helvetica", 30), bg="#536878", fg="#00BFFF")
        self.label_title.pack()
        self.width=600
        self.height=600
        #self.canvas = Canvas(self, width=self.width, height=self.height, bg="#536878", bd=0, highlightthickness=0)
        #self.canvas.grid (row=0, column=0, rowspan = size, columnspan = size, padx = 6, pady = 8)
        for i in range(0,size):
            for j in range(0, size):
                self.canvas.create_rectangle(((self.width/size)*i), ((self.height/size) *j), ((self.width/size)*(i + 1)), ((self.height/size) *(j + 1)), fill="#393c51")
        self.canvas.pack(expand=YES)
        self.frame.pack(expand=YES)
        self.afficher(puzzle)"""
        self.resoudre(puzzle, Dest)

    """def afficher(self, puzzle):
        "Affiche les caractéres sur le canvas"
        for j in range (0,size):
            for i in range (0,size):
                eff=self.canvas.create_rectangle(((self.width/size)*i), ((self.height/size) *j), ((self.width/size)*(i + 1)), ((self.height/size) *(j + 1)), fill="#393c51" if puzzle[j][i] != 0 else "#FFFFFF") #efface l'ancien caractere
                aff=self.canvas.create_text(((self.width/size) *i + (self.width/size/2)),((self.height/size) *j + (self.height/size/2)),text=str(puzzle[j][i] if puzzle[j][i] != 0 else ""), font=("helvetica", 30))"""

    def printResult(self, liste, i = 1) :
        #self.afficher(liste.pop(0))
        if liste :
            self.after(500, self.printResult, liste, i + 1)
        else :
            self.after(3000, self.setexit)

    def setexit(self):
        quit()

    def resoudre(self, puzzle, Dest) :
        start_time = time.time()
        idDest = setId(Dest)
        puzclass = puzzle_create()
        puzclass.create(size, puzzle, 0, 0, "")

        Start = puzclass

        print("start =")
        print(Start)
        print("Dest =")
        print(Dest)
        retour = algorithme_a_star(Start, Dest, idDest) 
        if retour == -1 :
            print("ERROR")
        else :
            print("SUCCESS")
            #self.printResult(retour)
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        return retour

#################################################################################################

class puzzle_create :
    #Constructeur
    def __init__(self) :
        self.puzzle = [] 
        self.heuristique = 0 #cout + nb distance de chaques pieces mal palces
        self.cout = 0 #nombre total des distance de toute les pieces jusqu a leur destination 
        self.id = ""
        self.predecessor = ""
        self.prevMove = ""

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    #Fonction creation map
    def create(self, size, puzzle, cout, predecessor, prevMove) :
        self.puzzle = puzzle
        self.id = setId(puzzle)
        self.cout = cout
        if gh == 1:
            self.heuristique == self.hamming() + self.cout
        elif gh == 2:
            self.heuristique = self.manhattan() + self.cout
        elif gh == 3:
            self.heuristique = self.manhattan() + (self.linear_conflicts(self.puzzle, Dest) *2) + self.cout
        elif gh == 4 :
            self.heuristique = self.manhattan() +  (self.linear_conflicts(self.puzzle, Dest) * 2) + self.cout +self.hamming()
        self.predecessor = predecessor
        self.prevMove = prevMove
    #fonction mise a jour
    def update(self, cout, heuristique, predecessor) :
        self.cout = cout
        self.heuristique = heuristique
        self.predecessor = predecessor
        
    def manhattan(self) :
        puzz = self.puzzle
        dest = []
        board = []
        for x in puzz:
            board += x  #In python you can merge 2 lists with +
        for x in Dest:
            dest += x
        somme = sum(abs(b%size - g%size) + abs(b//size - g//size)
            for b, g in ((board.index(i), dest.index(i)) 
                for i in range(1, size * size)
            )
        )
        return somme

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
        value = []
        if zero[0] > 0 and etat.prevMove != 'd':
            value.append("u")
        if zero[0] < size - 1 and etat.prevMove != 'u':
            value.append("d")
        if zero[1] > 0 and etat.prevMove != 'r':
            value.append("l")
        if zero[1] < size - 1 and etat.prevMove != 'l' :
            value.append("r")
        return createMove(etat, value, zero)

def setId(puzzle) :
    id = ''.join(str(item) for innerlist in puzzle for item in innerlist)
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
            successeur.create(size, puzzle, prevEtat.cout + 1, prevEtat.id, cpt)
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

def foundValue(puzzlei, value) :
    puzz = puzzlei
    i = 0
    posZero = []
    while i < size :
        j = 0
        while j < size :
            if puzz[i][j] == value :
                posZero.append(i)
                posZero.append(j)
                break
            j += 1
        i += 1
    return posZero

def converter2Dto1DList(array):
    return sum(array, [])

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

def calculInvariance(etat, solution) :
    nb = 0
    cpt = 0
    while cpt < len(solution) :
        sol = solution[:cpt] #tout les elements avantle nombre
        puzz = etat[etat.index(solution[cpt]) + 1:len(solution)] #tout les elements apres le nombre
        inter = intersection(sol, puzz)
        nb += len(inter) if len(inter) > 0 else 0 
        cpt += 1
    return nb

def isSoluble(puzzle, dest) :
    zeroOnPuzz = foundValue(puzzle, 0)
    zeroOnDest = foundValue(dest, 0)

    distanceOfZero = abs(zeroOnPuzz[0] - zeroOnDest[0]) + abs(zeroOnPuzz[1] - zeroOnDest[1])
    puzzleOnLine = converter2Dto1DList(puzzle)
    destOnLine = converter2Dto1DList(dest)

    invariant = calculInvariance(puzzleOnLine, destOnLine)

    if (distanceOfZero % 2 == 0 and invariant % 2 == 0) or (distanceOfZero % 2 != 0 and invariant % 2 == 0):
        return True
    return False

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

def retracePath (idetat, lopen, lclosed, start, liste) :
    if idetat == start.id :
        print_map(start.puzzle, 'step ' + str(len(liste)))
        liste.append(start.puzzle)
        return liste
    if idetat in lclosed :
        retracePath(lclosed[idetat].predecessor, lopen, lclosed, start, liste)
        print_map(lclosed[idetat].puzzle, 'step ' + str(len(liste)))
        liste.append(lclosed[idetat].puzzle)
        return liste
    elif idetat in lopen :
        retracePath(lopen[idetat].predecessor, lopen, lclosed, start, liste)
        print_map(lopen[idetat].puzzle, 'step ' + str(len(liste)))
        liste.append(lopen[idetat].puzzle)
        return liste

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


def algorithme_a_star(Start, Dest, idDest) :
    closedList = {}
    openList = {}
    openList[Start.id] =  Start
    heap = [(0.000000, Start.id)]
    nbTurn = 0
    lenL = 0
    while openList :
        val = heappop(heap)
        currentEtat =  openList[val[1]]
        #print(currentEtat)
        tot = len(openList) + len(closedList)
        if (tot > lenL) :
            lenL = tot
        if currentEtat.id == idDest :
            print("FIN !")
            print_map(currentEtat.puzzle, "")
            print ('Total number of states ever selected in the "opened" set :', nbTurn)
            print ('Maximum number of states ever represented in memory at the same time during the search :', lenL)
            print ('Number of moves required to transition from the initial state to the final state, according to the search :', currentEtat.cout)
            liste = []
            liste = retracePath(currentEtat.id, openList, closedList, Start, liste)
            return liste
        successeurs = getSuccesseurs(currentEtat)
        for elem in successeurs :
            #t = 0
            currentCout = elem.cout
            prevClosedCout = getCoutDict(elem, closedList)
            prevOpenCout = getCoutDict(elem, openList)
            if not ((prevClosedCout != -1 and prevClosedCout < currentCout) or (prevOpenCout != -1 and prevOpenCout < currentCout)) :
                if (elem.id in openList) :
                    #t +=  1
                    value = openList[elem.id].heuristique + (openList[elem.id].cout / 100000)
                    i = heap.index((value, elem.id))
                    heap[i] = (elem.heuristique + (elem.cout / 100000), elem.id)
                    _siftdown(heap, 0, i)
                else :
                    heappush(heap, (elem.heuristique + (elem.cout / 100000), elem.id))
                openList[elem.id] = elem
        #if t > 0 :
            #heapify(heap)
        closedList[currentEtat.id] = currentEtat
        del openList[currentEtat.id]
        nbTurn += 1
    return -1

def sous_image (src,xA,yA,xB,yB):
    """
    renvoie un morceau rectangulaire de l'image ``src``
    depuis le point supérieur gauche de coordonnées (xA,yA)
    au point inférieur droit de coordonnées (xB,yB).
    """
    pce = PhotoImage ()
    pce.tk.call (pce, 'copy', src,
                 '-from', xA, yA, xB, yB, '-to', 0, 0)
    return pce

if len(sys.argv) <= 2 or len(sys.argv) >= 4:
    sys.stderr.write("usage: main.py -[manhattan][hamming][linearconflicts][all]\n")
    sys.exit()

if len(sys.argv) == 3:
    if (sys.argv[1] == "-hamming") :
        gh = 1
    elif (sys.argv[1] == "-manhattan") :
        gh = 2
    elif (sys.argv[1] == "-linearconflicts") :
        gh = 3
    elif (sys.argv[1] == "-all") :
        gh = 4
    else :
        sys.stderr.write("You must choose one of these heuristics :\n -manhattan (count number of misplace and their distance from destination\n -hamming (count number of misplace)\n -linearconflicts (manhattan + number of 2 case who must be swap by line)")
        sys.exit()
    path = sys.argv[2]
    if open(path) == -1 :
        sys.stderr.write("file not found\n")
        sys.exit()
    else :
        filemap = path

def create_puzzle(array):
    i = 0
    width = 0
    height = 0
    puzzle = []
    size = int(array[0])
    while i < size :
        puzzle.append([0] * size)
        i += 1
    while height < size :
        width = 0
        while width < size :
            puzzle[height][width] = int(array[width + (size * height) + 1])
            width += 1
        height += 1
    return puzzle


def checkSize(array, size):
    cpth = 1
    cptw = 0
    if (int((len(array) - 1) / size) != size) :
        return False
    return True


with open(filemap) as fd:
    i = 0
    line = fd.readline()
    count = 1
    height = 0
    width = 0
    size = 0
    array = []
    while line :
        value = line.strip()
        if bool(re.match('^[0-9 ]+$', value)) == False : 
            print("Suppression Ligne")
        else :
            i = 0
            val = value.split()
            for elem in  val :
                array.append(elem)
            print(array)
        line = fd.readline()
        count += 1
    size = int(array[0])
    if checkSize(array, size) == False :
        print("Not a valid File !")
    puzzle = create_puzzle(array)


if (size < 2) :
    sys.exit()

Dest = solution(size)

if not isSoluble(puzzle, Dest) :
    sys.stderr.write("This puzzle can't be solved !")
else :
    print_map(puzzle, "Start")
    taquin = Taquin(puzzle, Dest, size)
#taquin.mainloop()