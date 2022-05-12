from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget): # hérite de QWidget

    def __init__(self, parent = None):
        
        QWidget.__init__(self, parent )
        print("class Canvas")
        
        # Changement de la taille par défault
        self.setMinimumSize(200, 400)
        
        # Pour savoir si il existe un fichier log
        self.existeLog = True
        
        # Pour stocker les coordonnées du rectangle (None), ou de plusieurs rectangles ([])
        self.cursorPosPress = []
        self.cursorPosRelease = []
        
        # Pour pouvoir modifier la couleur du pinceau, de la brosse ...
        self.ColorPen = [0, 255, 0] # Couleur du pinceau sous forme de triplet R, G, B
        self.ColorBrush = [0, 0, 255] # Couleur de la brosse sous forme de triplet R, G, B
        self.Forme = "Rect"
        self.Width = 5
        
        # Pour pouvoir dessiner des formes, épaisseurs et couleurs différentes pour chaque figure
        self.Formes = []
        self.ColorsPen = [] # Stocke les composantes RGB
        self.ColorsBrush = [] # Stocke les composantes RGB
        self.Widths = []
        
        # Pour savoir dans quel mode on est
        self.mode = "Draw"
        
        # Pour pouvoir déplacer le dessin
        self.cursorPosDebut = None
        self.cursorPosFin = None
        
        # Pour pouvoir changer la couleur du rectangle sélectionné
        self.rectangle = None
        self.cursorPosSelect = None
        
        # La forme selectionnée
        self.figureSelection = None
        self.rougeSelection = 0 # Pour que ça ne l'affiche en rouge que la première fois
        
        # Pour le lasso
        self.cursorPosPressLasso = None
        self.cursorPosReleaseLasso = None
        self.figuresSelection = []
        
        # Pour le free drawing 
        self.lastCursorPos = None 
        self.finDessin = True
        
        # On charge le fichier log si il en existe un 
        try:
            with open("log.txt", "r"): pass
        except IOError:
            print("Il n'existe pas de fichier log")
            self.existeLog = False
        
        
        if self.existeLog == True:
            self.openCanvas("log.txt")

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")
        
    # Redéfinition de la méthode paintEvent
    def paintEvent(self, event): 
        painter = QPainter(self) # recupere le QPainter du widget 
        
        # On bouge le pinceau et on redessine
        if self.mode == "Move":
            if self.cursorPosDebut != None and self.cursorPosFin != None:
                for i in range(len(self.cursorPosRelease)):
                    self.cursorPosPress[i] = QPoint(self.cursorPosPress[i].x() + self.cursorPosFin.x() - self.cursorPosDebut.x(), self.cursorPosPress[i].y() + self.cursorPosFin.y() - self.cursorPosDebut.y())
                    self.cursorPosRelease[i] = QPoint(self.cursorPosRelease[i].x() + self.cursorPosFin.x() - self.cursorPosDebut.x(), self.cursorPosRelease[i].y() + self.cursorPosFin.y() - self.cursorPosDebut.y())
            
        # On dessine le rectangle si on clique sur l'écran
        for i in range(len(self.cursorPosRelease)): # Pour pouvoir tracer plusieurs formes
            pen = QPen(QColor(self.ColorsPen[3*i], self.ColorsPen[3*i + 1], self.ColorsPen[3*i + 2])) # instancier un pen
            pen.setWidth(self.Widths[i]) # change l'epaisseur
            
            if (self.rougeSelection > 0 and self.mode == "Select" and self.figureSelection == i) or (self.rougeSelection > 0 and self.mode == "Lasso" and self.figuresSelection != [] and i in self.figuresSelection): # Si on a sélectionné cette forme, on l'affiche avec un contour rouge
                pen = QPen(Qt.red) # On met le pinceau à rouge sur les éléments selectionnés
                pen.setWidth(15)
                self.rougeSelection -= 1
            
            painter.setPen(pen) # appliquer ce pen au painter 
            
            painter.setBrush(QColor(self.ColorsBrush[3*i], self.ColorsBrush[3*i + 1], self.ColorsBrush[3*i + 2])) # met le brush a la couleur sélectionnée
        
            if self.cursorPosPress[i] != None and self.cursorPosRelease[i] != None:
                if self.Formes[i] == "Rect":
                    painter.drawRect(self.cursorPosPress[i].x(), self.cursorPosPress[i].y(), self.cursorPosRelease[i].x() - self.cursorPosPress[i].x(), self.cursorPosRelease[i].y() - self.cursorPosPress[i].y()) 
                    self.rectangle = QRect(self.cursorPosPress[i].x(), self.cursorPosPress[i].y(), self.cursorPosRelease[i].x() - self.cursorPosPress[i].x(), self.cursorPosRelease[i].y() - self.cursorPosPress[i].y()) 
        
                if self.Formes[i] == "Elli":
                    painter.drawEllipse(self.cursorPosPress[i].x(), self.cursorPosPress[i].y(), self.cursorPosRelease[i].x() - self.cursorPosPress[i].x(), self.cursorPosRelease[i].y() - self.cursorPosPress[i].y()) 
                
                if self.Formes[i] == "Line":
                    painter.drawLine(self.cursorPosPress[i].x(), self.cursorPosPress[i].y(), self.cursorPosRelease[i].x(), self.cursorPosRelease[i].y())  
       
    # Redéfinition des méthodes pour dessiner interactivement
    def mousePressEvent(self, event): # evenement mousePress
        if self.mode == "Draw":
            self.cursorPosPress.append(event.pos())   # on stocke la position du curseur 
        
        if self.mode == "Move":
            self.cursorPosDebut = event.pos()
            
        if self.mode == "Select":
            self.cursorPosSelect = event.pos()
        
        if self.mode == "Lasso":
            self.figuresSelection = [] # Pour ne pas qu'au prochain appui sur lasso ça modifie aussi les objets sélectionnés la dernière fois
            self.cursorPosPressLasso = event.pos()
            
        if self.mode == "FreeDrawing":
            self.finDessin = False
            self.lastCursorPos = event.pos()
        
    def mouseReleaseEvent(self, event): # evenement mouseRelease
    
        if self.mode == "FreeDrawing":
            self.finDessin = True
            self.lastCursorPos = None 
        
        if self.mode == "Draw":
            self.cursorPosRelease.append(event.pos())  # on stocke la position du curseur 
            self.Formes.append(self.Forme) # on ajoute à la liste de formes la forme actuelle
            self.ColorsPen.extend(self.ColorPen) # on ajoute à la liste de couleurs de pinceaux la couleur actuelle
            self.ColorsBrush.extend(self.ColorBrush) # on ajoute à la liste de couleurs de brosse la couleur actuelle
            self.Widths.append(self.Width) # on ajoute à la liste d'épaisseurs l'épaisseur actuelle
            self.update()   # on met à jour l'affichage
        
        if self.mode == "Move":
            self.cursorPosFin = event.pos()
            self.update()
        
        if self.mode == "Select":
            # figure est la figure selectionnée  
            figure = None 
            
            if self.cursorPosSelect != None:
                for i in range(len(self.cursorPosPress)): # On parcourt toutes les figures pour voir si une correspond à la selection
                    if self.cursorPosPress[i].x() < self.cursorPosRelease[i].x(): # Si le rectangle va dans le bon sens des x
                        if self.cursorPosPress[i].x() > self.cursorPosSelect.x() or self.cursorPosSelect.x() > self.cursorPosRelease[i].x(): # Il n'est pas dans ce rectangle
                            continue
                    if self.cursorPosPress[i].x() > self.cursorPosRelease[i].x(): # Si le rectangle va dans le mauvais sens des x
                        if self.cursorPosPress[i].x() < self.cursorPosSelect.x() or self.cursorPosSelect.x() < self.cursorPosRelease[i].x(): # Il n'est pas dans ce rectangle
                            continue
                        
                    if self.cursorPosPress[i].y() < self.cursorPosRelease[i].y(): # Si le rectangle va dans le bon sens des y
                        if self.cursorPosPress[i].y() > self.cursorPosSelect.y() or self.cursorPosSelect.y() > self.cursorPosRelease[i].y(): # Il n'est pas dans ce rectangle
                            continue
                    if self.cursorPosPress[i].y() > self.cursorPosRelease[i].y(): # Si le rectangle va dans le mauvais sens des y
                        if self.cursorPosPress[i].y() < self.cursorPosSelect.y() or self.cursorPosSelect.y() < self.cursorPosRelease[i].y(): # Il n'est pas dans ce rectangle
                            continue
                    # Si on est encore là, c'est que le point est dans le rectangle
                    figure = i
                    #break # On en a trouvé un, ça suffira
                
                    if figure != None:
                        self.figureSelection = figure
                        self.rougeSelection = 1
                        self.ColorsBrush[3*figure] = self.ColorBrush[0]
                        self.ColorsBrush[3*figure + 1] = self.ColorBrush[1]
                        self.ColorsBrush[3*figure + 2] = self.ColorBrush[2]
                        
                        self.ColorsPen[3*figure] = self.ColorPen[0]
                        self.ColorsPen[3*figure + 1] = self.ColorPen[1]
                        self.ColorsPen[3*figure + 2] = self.ColorPen[2]
                        self.Widths[figure] = self.Width
                        self.update()
                        
                if figure == None:
                    self.update() # Pour enlever le rouge de la selection
                    print("Aucun élément sélectionné")
                
                self.cursorPosSelect = None # Pour ne pas qu'au prochain appui sur select ça modifie l'objet sélectionné la dernière fois
        
        if self.mode == "Lasso":
            # self.figuresSelection = [] # Pour ne pas qu'au prochain appui sur lasso ça modifie aussi les objets sélectionnés la dernière fois
            self.cursorPosReleaseLasso = event.pos()
            
            if self.cursorPosPressLasso != None:
                for i in range(len(self.cursorPosPress)): # On parcourt toutes les figures pour voir si une correspond à la selection
                    if self.cursorPosPress[i].x() > self.cursorPosPressLasso.x() and self.cursorPosPress[i].y() > self.cursorPosPressLasso.y() and self.cursorPosPress[i].x() < self.cursorPosReleaseLasso.x() and self.cursorPosPress[i].y() < self.cursorPosReleaseLasso.y(): # Si le point press du rectangle est entre les deux points du lasso
                        self.figuresSelection.append(i)
                        continue
                    
                    if self.cursorPosRelease[i].x() > self.cursorPosPressLasso.x() and self.cursorPosRelease[i].y() > self.cursorPosPressLasso.y() and self.cursorPosRelease[i].x() < self.cursorPosReleaseLasso.x() and self.cursorPosRelease[i].y() < self.cursorPosReleaseLasso.y(): # Si le point release du rectangle est entre les deux points du lasso
                        self.figuresSelection.append(i)
                        continue
                
                if self.figuresSelection != []:
                    for figure in self.figuresSelection :
                        self.ColorsBrush[3*figure] = self.ColorBrush[0]
                        self.ColorsBrush[3*figure + 1] = self.ColorBrush[1]
                        self.ColorsBrush[3*figure + 2] = self.ColorBrush[2]
                        
                        self.ColorsPen[3*figure] = self.ColorPen[0]
                        self.ColorsPen[3*figure + 1] = self.ColorPen[1]
                        self.ColorsPen[3*figure + 2] = self.ColorPen[2]
                        self.Widths[figure] = self.Width
                    self.rougeSelection = len(self.figuresSelection)
                    self.update()
                        
                if self.figuresSelection == []:
                    self.update() # Pour enlever le rouge de la selection
                    print("Aucun élément sélectionné")
                    
        if self.mode == "FreeDrawing":
            self.lastCursorPos = None    
                    
    """ SI ON NE VEUT QU UNE SEULE FIGURE MODIFIEE dans le Select
    if self.cursorPosSelect != None:
                for i in range(len(self.cursorPosPress)-1, 1, -1): # On parcourt toutes les figures pour voir si une correspond à la selection
                    if self.cursorPosPress[i].x() < self.cursorPosRelease[i].x(): # Si le rectangle va dans le bon sens des x
                        if self.cursorPosPress[i].x() > self.cursorPosSelect.x() or self.cursorPosSelect.x() > self.cursorPosRelease[i].x(): # Il n'est pas dans ce rectangle
                            continue
                    if self.cursorPosPress[i].x() > self.cursorPosRelease[i].x(): # Si le rectangle va dans le mauvais sens des x
                        if self.cursorPosPress[i].x() < self.cursorPosSelect.x() or self.cursorPosSelect.x() < self.cursorPosRelease[i].x(): # Il n'est pas dans ce rectangle
                            continue
                        
                    if self.cursorPosPress[i].y() < self.cursorPosRelease[i].y(): # Si le rectangle va dans le bon sens des y
                        if self.cursorPosPress[i].y() > self.cursorPosSelect.y() or self.cursorPosSelect.y() > self.cursorPosRelease[i].y(): # Il n'est pas dans ce rectangle
                            continue
                    if self.cursorPosPress[i].y() > self.cursorPosRelease[i].y(): # Si le rectangle va dans le mauvais sens des y
                        if self.cursorPosPress[i].y() < self.cursorPosSelect.y() or self.cursorPosSelect.y() < self.cursorPosRelease[i].y(): # Il n'est pas dans ce rectangle
                            continue
                    # Si on est encore là, c'est que le point est dans le rectangle
                    figure = i
                    break # On en a trouvé un, ça suffira
                
                if figure != None:
                    self.figureSelection = figure
                    self.rougeSelection += 1
                    self.ColorsBrush[3*figure] = self.ColorBrush[0]
                    self.ColorsBrush[3*figure + 1] = self.ColorBrush[1]
                    self.ColorsBrush[3*figure + 2] = self.ColorBrush[2]
                    
                    self.ColorsPen[3*figure] = self.ColorPen[0]
                    self.ColorsPen[3*figure + 1] = self.ColorPen[1]
                    self.ColorsPen[3*figure + 2] = self.ColorPen[2]
                    self.Widths[figure] = self.Width
                    self.update()
                    self.cursorPosSelect = None # Pour ne pas qu'auu prochain appui sur select ça modifie l'objet sélectionné la dernière fois
                if figure == None:
                    self.update() # Pour enlever le rouge de la selection
                    print("Aucun élément sélectionné")"""
    
    
    def  mouseMoveEvent(self, event): 
        if self.mode == "FreeDrawing":
            if self.finDessin == False:
                
                self.cursorPosPress.append(self.lastCursorPos) # on stocke le point de depart du trait 
                self.cursorPosRelease.append(event.pos()) # on stocke le point d'arrivée du trait 
                self.Formes.append("Line") # on ajoute à la liste de formes la forme actuelle
                self.ColorsPen.extend(self.ColorPen) # on ajoute à la liste de couleurs de pinceaux la couleur actuelle
                self.ColorsBrush.extend(self.ColorBrush) # on ajoute à la liste de couleurs de brosse la couleur actuelle
                self.Widths.append(self.Width) # on ajoute à la liste d'épaisseurs l'épaisseur actuelle
                self.update()   # on met à jour l'affichage
            
            self.lastCursorPos = event.pos()
            
            
    # Pour que la fonction main puisse changer la couleur du pinceau, de la brosse, ...
    def setBrushColor(self, color): # color est un tableau des trois composantes R G B
        self.ColorBrush = color
        if self.mode == "Select":
            self.ColorsBrush[3*self.figureSelection] = self.ColorBrush[0]
            self.ColorsBrush[3*self.figureSelection + 1] = self.ColorBrush[1]
            self.ColorsBrush[3*self.figureSelection + 2] = self.ColorBrush[2]
            self.update()
            
        if self.mode == "Lasso":
            if self.figuresSelection != []:
                for figure in self.figuresSelection :
                    self.ColorsBrush[3*figure] = self.ColorBrush[0]
                    self.ColorsBrush[3*figure + 1] = self.ColorBrush[1]
                    self.ColorsBrush[3*figure + 2] = self.ColorBrush[2]
                self.update()
            
        
    def setPenColor(self, color): # color est un tableau des trois composantes R G B
        self.ColorPen = color
        if self.mode == "Select":
            self.ColorsPen[3*self.figureSelection] = self.ColorPen[0]
            self.ColorsPen[3*self.figureSelection + 1] = self.ColorPen[1]
            self.ColorsPen[3*self.figureSelection + 2] = self.ColorPen[2]
            
            self.update()
            
        if self.mode == "Lasso":
            if self.figuresSelection != []:
                for figure in self.figuresSelection :                    
                    self.ColorsPen[3*figure] = self.ColorPen[0]
                    self.ColorsPen[3*figure + 1] = self.ColorPen[1]
                    self.ColorsPen[3*figure + 2] = self.ColorPen[2]
                    
                self.update()
        
    def setForme(self, forme):
        if self.mode == "FreeDrawing":
            self.mode = "Draw" # On considère que si on clique sur une figure après le free drawing, c'est pour dessiner
            
        self.Forme = forme
        
        if self.mode == "Select" and self.figureSelection != None:
            self.Formes[self.figureSelection] = self.Forme
            self.update()
            
        if self.mode == "Lasso" and self.figuresSelection != []:
                for figure in self.figuresSelection :
                    self.Formes[figure] = self.Forme
                self.update()
       
    def setWidth(self, width):
        self.Width = width
        
        if self.mode == "Select" and self.figureSelection != None:
            self.Widths[self.figureSelection] = self.Width
            self.update()
            
        if self.mode == "Lasso" and self.figuresSelection != []:
                for figure in self.figuresSelection :
                    self.Widths[figure] = self.Width
                self.update()
                    
    def changeWidth(self):
        if self.Width == 14:
            self.Width = 1
        else :
            self.Width += 1
            
        if self.mode == "Select" and self.figureSelection != None:
            self.Widths[self.figureSelection] = self.Width
            self.update()
            
        if self.mode == "Lasso" and self.figuresSelection != []:
                for figure in self.figuresSelection :
                    self.Widths[figure] = self.Width
                self.update()
        
    def move(self):
        self.mode = "Move"
        self.figureSelection = None # Plus de figure selectionnée
        self.update()
        
    def draw(self):
        self.mode = "Draw"
        self.figureSelection = None # Plus de figure selectionnée
        self.update()
        
    def freedrawing(self):
        self.mode = "FreeDrawing"
        
    def select(self):
        self.mode = "Select"
                
    def lasso(self):
        self.mode = "Lasso"
        
    def retour(self):
        if len(self.cursorPosPress) == 0:
            print("Pas de retour à effectuer, aucune figure dessinée")
            
        else:
            del self.cursorPosPress[-1]
            del self.cursorPosRelease[-1]
            del self.Formes[-1]
            
            # Pour les suppressions, on ne change pas l'indice car del va tout décaler sur la gauche
            del self.ColorsPen[-1]
            del self.ColorsPen[-1]
            del self.ColorsPen[-1]
            del self.ColorsBrush[-1]
            del self.ColorsBrush[-1]
            del self.ColorsBrush[-1]
            
            del self.Widths[-1]
            self.update()
            
    def supprime(self): # AJOUT de supprime
        if self.mode == "Lasso" and self.figuresSelection != []:
            for fig in range(len(self.figuresSelection)):
                figureAenlever = self.figuresSelection[fig]
                for i in range(len(self.figuresSelection)):
                    if self.figuresSelection[i] > figureAenlever:
                        self.figuresSelection[i] -= 1 # Pour que l'indice soit le bon après la suppression d'un élément
                del self.cursorPosPress[figureAenlever]
                del self.cursorPosRelease[figureAenlever]
                del self.Formes[figureAenlever]
                
                del self.ColorsPen[3*figureAenlever]
                del self.ColorsPen[3*figureAenlever]
                del self.ColorsPen[3*figureAenlever]
                del self.ColorsBrush[3*figureAenlever]
                del self.ColorsBrush[3*figureAenlever]
                del self.ColorsBrush[3*figureAenlever]
                del self.Widths[figureAenlever]
                         
            self.figuresSelection = []
            self.update()   
            
        if self.mode == "Select" and self.figureSelection != None:
            del self.cursorPosPress[self.figureSelection]
            del self.cursorPosRelease[self.figureSelection]
            del self.Formes[self.figureSelection]
            
            del self.ColorsPen[3*self.figureSelection]
            del self.ColorsPen[3*self.figureSelection]
            del self.ColorsPen[3*self.figureSelection]
            del self.ColorsBrush[3*self.figureSelection]
            del self.ColorsBrush[3*self.figureSelection]
            del self.ColorsBrush[3*self.figureSelection]
            
            del self.Widths[self.figureSelection]
            
            self.figureSelection = None
            self.update()  
            
    def clear(self): # Ajout de clear
    
        # Attributs de sauvegarde de figures
        self.cursorPosPress = []
        self.cursorPosRelease = []
        self.Formes = []
        self.ColorsPen = []
        self.ColorsBrush = []
        self.Widths = []
        
        # Attributs de déplacement, et selection
        self.cursorPosDebut = None
        self.cursorPosFin = None
        self.rectangle = None
        self.cursorPosSelect = None
        self.figureSelection = None
        self.rougeSelection = 0 
        self.cursorPosPressLasso = None
        self.cursorPosReleaseLasso = None
        self.figuresSelection = []
        
        self.lastCursorPos = None
            
        self.update()
        
    def openCanvas(self, nameFichier):
        self.clear()
        
        fichier = open(nameFichier, "r")
        contenu = fichier.read()
        contenu = contenu.split(";")
        
        contenu0 = contenu[0].split(",")  
        i = 0
        while i + 1 < len(contenu0):
            self.cursorPosPress.append(QPoint(int(contenu0[i]), int(contenu0[i+1])))
            i += 2
            
        contenu1 = contenu[1].split(",")
        i = 0
        while i + 1 < len(contenu1):
            self.cursorPosRelease.append(QPoint(int(contenu1[i]), int(contenu1[i+1])))
            i += 2
            
        contenu2 = contenu[2].split(",")
        for i in range(len(contenu2)):
            self.Formes.append(contenu2[i])
            
        contenu3 = contenu[3].split(",")
        i = 0
        while i + 2 < len(contenu3):
            self.ColorsPen.append(int(contenu3[i])) 
            self.ColorsPen.append(int(contenu3[i+1]))
            self.ColorsPen.append(int(contenu3[i+2]))
            i += 3
            
        contenu4 = contenu[4].split(",")
        i = 0
        while i + 2 < len(contenu4):
            self.ColorsBrush.append(int(contenu4[i])) 
            self.ColorsBrush.append(int(contenu4[i + 1]))
            self.ColorsBrush.append(int(contenu4[i + 2]))
            i += 3
            
        contenu5 = contenu[5].split(",")
        for i in range(len(contenu5)):
            self.Widths.append(int(contenu5[i]))
            
        fichier.close()
    
        self.update()
