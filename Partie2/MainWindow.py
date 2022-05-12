import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import * 
import resources
import time
import os

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
        self.resize(600, 500)
        
        #TP1
        # Création d'une barre de menu
        menu = self.menuBar()
        fileMenu = menu.addMenu( "Fichier" ) 
        
        # Création de l'action New et ajout de cette action à la barre de menu
        actNew = QAction(QIcon("./icons/new.png"), "New…", self)
        fileMenu.addAction(actNew)
        
        # Création de l'action Open et ajout de cette action à la barre de menu
        actOpen = QAction(QIcon("./icons/opent.png"), "Open text…", self)
        fileMenu.addAction(actOpen)
        actOpeni = QAction(QIcon(":/icons/open.png"), "Open canvas…", self)
        fileMenu.addAction(actOpeni)
        
        # Action pour faire une animation
        actAnim = QAction(QIcon("./icons/animation.png"), "Play animation…", self)
        fileMenu.addAction(actAnim)
        
        # Création de l'action Save et ajout de cette action à la barre de menu
        actSavet = QAction(QIcon("./icons/savet.png"), "Save text…", self)
        fileMenu.addAction(actSavet)
        # Création de l'action Save et ajout de cette action à la barre de menu
        actSavei = QAction(QIcon("./icons/savei.png"), "Save canvas…", self)
        fileMenu.addAction(actSavei)
        # Création de l'action Quit et ajout de cette action à la barre de menu
        actQuit = QAction(QIcon(":/icons/quit.png"), "Quit…", self)
        fileMenu.addAction(actQuit)
        # Création d'une barre d'outils
        tool = QToolBar("Barre")
        tool.addAction(actSavet)
        tool.addAction(actSavei)
        tool.addAction(actNew)
        tool.addAction(actOpen)
        tool.addAction(actOpeni)
        tool.addAction(actAnim)
        tool.addAction(actQuit)
        
        ToolBar = self.addToolBar(tool)
        
        # Accélérateurs clavier  
        actNew.setShortcut( QKeySequence("Ctrl+N" ) )
        actSavet.setShortcut( QKeySequence("Ctrl+S" ) )
        actOpen.setShortcut( QKeySequence("Ctrl+O" ) )
        actQuit.setShortcut(QKeySequence("Ctrl+Q"))
        
        # Bulles d’aides
        actNew.setToolTip("New File")
        actSavet.setToolTip("Save Text")
        actSavei.setToolTip("Save Canvas")
        actOpen.setToolTip("Open Text")
        actOpeni.setToolTip("Open Canvas")
        actAnim.setToolTip("Play animation")
        actQuit.setToolTip("Quit File")
        
        # Zone centrale de la MainWindow
        self.textEdit = QTextEdit()
        textEditor = self.setCentralWidget(self.textEdit)
    
        # Barre de status         
        status = self.statusBar()
    
        # Connecter les slots aux actions correspondantes
        actNew.triggered.connect( self.newFile )
        actSavet.triggered.connect( self.saveFile )        
        actSavei.triggered.connect( self.saveCanvas )
        actOpen.triggered.connect( self.openFile ) 
        actOpeni.triggered.connect( self.openC )  
        actAnim.triggered.connect( self.animation ) 
        actQuit.triggered.connect(self.quitApp)
        
        """# Bonus pour le TP1
        # Implementation d'un QPushButton
        button = QPushButton("Hello World !", self)
        button.clicked.connect( self.helloWorld )
        button.resize(100,20)
        button.move(0, 100)
        
        # Intégration d'éléments QLabel (un texte labelA et une image labelB)
        labelA = QLabel(self)
        labelB = QLabel(self)
        labelA.setText('Le joli panda !') # On ajoute ce texte en haut
        image = QPixmap('panda.jpg') # Ainsi qu'une image
        labelB.setPixmap(image)
        labelB.resize(image.size()) # On met l'image à la bonne taille
        self.setWindowTitle('Un panda !') # Et on change le nom de la fenêtre
        self.setGeometry(100, 100, 300, 200)
        labelA.move(120, 50)
        labelB.move(120, 120)"""
        
        bar = self.menuBar()
        fileMenu = bar.addMenu("Actions")

        colorMenu = bar.addMenu("Colors")
        actPen = fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))
        actWidth = fileMenu.addAction(QIcon("./icons/epaisseur.png"), "&Width", self.width, QKeySequence("Ctrl+W"))
        actRectangle = fileMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = fileMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actLine = fileMenu.addAction(QIcon("./icons/line.png"), "&Line", self.line)
        actFree = fileMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)
        actSupp = fileMenu.addAction(QIcon("./icons/poubelle.png"), "&Supp", self.supprimer)
        actRetour = fileMenu.addAction(QIcon("./icons/retour.png"), "&Retour", self.retour) # Ajout du retour
        actRetour.setShortcut( QKeySequence("Ctrl+Z" ) )
        actClear = fileMenu.addAction(QIcon("./icons/clear.png"), "&Clear", self.clear)
        
        colorMenu.addAction( actPen )
        colorMenu.addAction( actBrush )
        
        colorToolBar = QToolBar("Modifications")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )
        colorToolBar.addAction( actWidth )
        colorToolBar.addAction( actSupp )
        colorToolBar.addAction( actClear )

        shapeMenu = bar.addMenu("Shape")
        
        
        shapeMenu.addAction( actRectangle )
        shapeMenu.addAction( actEllipse )
        shapeMenu.addAction( actLine )
        shapeMenu.addAction( actFree )
        
        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actLine )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)
        actLasso = modeMenu.addAction(QIcon("./icons/lasso.png"), "&Lasso", self.lasso) # Ajout du lasso
        
        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )
        modeToolBar.addAction( actLasso ) # Ajout du lasso
        modeToolBar.addAction( actRetour ) # Ajout du retour
        
        # Une instance de Canvas dans la zone centrale de la fenêtre
        #self.setCentralWidget(Canvas())
        
        # Une instance de Canvas et une de QTextEdit
        self.textEdit = QTextEdit()
        self.canvas = Canvas()
        
        # Créons un layout avec un canvas en haut et une zone de texte en dessous
        v_layout = QVBoxLayout() 
        v_layout.addWidget(self.canvas) 
         
        v_layout.addWidget(self.textEdit) 
        
        # Utilisons un QWidget comme container
        container = QWidget() 
        container.setLayout(v_layout) 
        self.setCentralWidget(container)
        
    def newFile(self):
        print("New")
        
    def openFile(self):
        print("Open text")
        # Le slot openFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
        fileName = QFileDialog.getOpenFileName( self, "Open File", "/home/jana","*.txt") 
        print(fileName)
        
        if len(fileName[0]) >  0:
            # Lire le fichier via la boîte de dialogue et faire apparaître son contenu dans le QTextEdit
            fichier = open(fileName[0], "rt")
            texte = fichier.read()
            self.textEdit.setPlainText(str(texte)) 
            fichier.close()
	

    def saveFile(self):
        print("Save text")	
        # Le slot saveFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
        fileName = QFileDialog.getSaveFileName()      
        print(fileName)
        
        if len(fileName[0]) >  0:
            # Sauvegarde le contenu du QTextEdit dans le fichier indiqué par la boîte de dialogue
            fichier = open(fileName[0] + ".txt", "wt")
            fichier.write(str(self.textEdit.toPlainText()))
            fichier.close()
     
    #Redefinition de la méthode closeEvent() pour que celle-ci se comporte comme quitApp
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to close the window?',QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            if len(self.canvas.cursorPosPress) > 0:
                reply2 = QMessageBox.question(self, 'Save', 'Do you wanna save the canvas?',QMessageBox.Yes | QMessageBox.No)
                if reply2 == QMessageBox.Yes:
                    self.saveCanvas()

            event.accept()
            print('Window closed')
        else:
            event.ignore()

    # Appuyer sur le bouton Quit a pour effet d’ouvrir un QMessageBox comportant des boutons
    # “Yes” et “No” permettant de demander confirmation avant de sortir de l’application
    def quitApp(self):
        print("Quit")
        
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to close the window?',QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            if len(self.canvas.cursorPosPress) > 0:
                reply2 = QMessageBox.question(self, 'Save', 'Do you wanna save the canvas?',QMessageBox.Yes | QMessageBox.No)
                if reply2 == QMessageBox.Yes:
                    self.saveCanvas()
                
            QApplication.quit()
            
    # Méthode associée au bouton Hello World     
    def helloWorld(self):
        print("Hello World")

        


    ##############                   
    def pen_color(self):
        self.log_action(False, "choose pen color")
        
        # Pour choisir la couleur nous-même
        color = QColorDialog.getColor()

        if color.isValid():
            self.canvas.setPenColor([color.red(), color.green(), color.blue()])
        else:
            print("Couleur invalide")

    def brush_color(self):
        self.log_action(False, "choose brush color")
        
        # Pour choisir la couleur nous-même
        color = QColorDialog.getColor()

        if color.isValid():
            self.canvas.setBrushColor([color.red(), color.green(), color.blue()])
        else:
            print("Couleur invalide")
            
    def width(self):
        self.log_action(False, "choose width")
        #Version 1:
        #self.canvas.changeWidth() # Pour l'instant on augmente de 5 dès que l'utilisateur clique
        
        #Version 2:
        # Pour choisir l'épaisseur nous-même avec un slider
        # slider = QSlider(None)
        # slider.valueChanged.connect(self.canvas.setWidth)
        
        nb, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter width:')

        if ok :
            if int(nb)<15: # On définit l'épaisseur maximale à 15
                self.canvas.setWidth(int(nb)) 
            if int(nb)>=15:
                print("L'épaisseur maximale est de 14")
                self.canvas.setWidth(14)

    def rectangle(self):
        self.log_action(False, "Shape mode: rectangle")
        self.canvas.setForme("Rect")

    def ellipse(self):
        self.log_action(False, "Shape Mode: circle")
        self.canvas.setForme("Elli")

    def line(self):
        self.log_action(False, "Shape mode: line")
        self.canvas.setForme("Line")
        
    def free_drawing(self):
        self.log_action(False, "Mode: freeDrawing")
        self.canvas.freedrawing()

    def move(self):
        self.log_action(False, "Mode: move")
        self.canvas.move()

    def draw(self):
        self.log_action(False, "Mode: draw")
        self.canvas.draw()
        
    def select(self):
        self.log_action(False, "Mode: select")
        self.canvas.select()
        
    # Ajout du lasso
    def lasso(self):
        self.log_action(False, "Mode: lasso")
        self.canvas.lasso()
        
    # Ajout du retour
    def retour(self):
        self.log_action(False, "Retour")
        self.canvas.retour()
        
    # Ajout de la suppression
    def supprimer(self):
        self.log_action(False, "Supprimer")
        self.canvas.supprime() 
        
    # Ajout du clear
    def clear(self):
        print("Sure to clear ?")
        buttonReply = QMessageBox.question(self, 'Sure to clear ?', "Do you want to clear the canvas ?", QMessageBox.Yes | QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:
            self.log_action(False, "Clear")
            self.canvas.clear()
            
    # Pour sauvegarder le canvas
    def saveCanvas(self):
        if len(self.canvas.cursorPosPress) > 0: # Si on a dessiné qqch, on l'enregistre
            strCursorPosPress = ""
            for i in range(len(self.canvas.cursorPosPress)-1):
                strCursorPosPress += str(self.canvas.cursorPosPress[i].x()) + "," + str(self.canvas.cursorPosPress[i].y()) + ","
            strCursorPosPress += str(self.canvas.cursorPosPress[len(self.canvas.cursorPosPress)-1].x()) + "," +str(self.canvas.cursorPosPress[len(self.canvas.cursorPosPress)-1].y())
            
            strCursorPosRelease = ""
            for i in range(len(self.canvas.cursorPosRelease)-1):
                strCursorPosRelease += str(self.canvas.cursorPosRelease[i].x()) + "," + str(self.canvas.cursorPosRelease[i].y()) + ","
            strCursorPosRelease += str(self.canvas.cursorPosRelease[len(self.canvas.cursorPosRelease)-1].x()) + "," + str(self.canvas.cursorPosRelease[len(self.canvas.cursorPosRelease)-1].y())
            
            
            strFormes = ""
            for i in range(len(self.canvas.Formes)-1):
                strFormes += str(self.canvas.Formes[i])  + ","
            strFormes += str(self.canvas.Formes[len(self.canvas.Formes)-1])
            
            strColorsPen = ""
            for i in range(len(self.canvas.ColorsPen)-1):
                strColorsPen += str(self.canvas.ColorsPen[i])  + ","
            
            strColorsPen += str(self.canvas.ColorsPen[len(self.canvas.ColorsPen)-1]) 
            
            strColorsBrush = ""
            for i in range(len(self.canvas.ColorsBrush)-1):
                strColorsBrush += str(self.canvas.ColorsBrush[i])  + ","
            
            strColorsBrush += str(self.canvas.ColorsBrush[len(self.canvas.ColorsBrush)-1])
            
            strWidths = ""
            for i in range(len(self.canvas.Widths)-1):
                strWidths += str(self.canvas.Widths[i])  + ","
            strWidths += str(self.canvas.Widths[len(self.canvas.Widths)-1])
            
            self.log_action(True, strCursorPosPress+";"+strCursorPosRelease+";"+strFormes+";"+strColorsPen+";"+strColorsBrush+";"+strWidths)
        else:
            print("Canvas vide, rien a sauvegarder")
        
    def openC(self):
        # On vérifie si l'utilisateur veut sauvegarder son canvas
        if len(self.canvas.cursorPosPress) > 0:
            reply2 = QMessageBox.question(self, 'Save', 'Do you wanna save the canvas?',QMessageBox.Yes | QMessageBox.No)
            if reply2 == QMessageBox.Yes:
                self.saveCanvas()
                
        print("Open canvas")	
        # Le slot saveFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
        fileName = QFileDialog.getOpenFileName( self, "Open File", "/home/jana","*.txt")
            
        if len(fileName[0]) >  0:
            self.canvas.openCanvas(fileName[0])
        
    def animation(self):
        folderpath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        for element in os.listdir(folderpath):
            time.sleep(0.1)
             
            self.canvas.openCanvas(folderpath + "/" + element)
            self.canvas.repaint() #update() 
        
    def log_action(self, close, string):
        
        if close == True:
            print("Save canvas")	
            # Le slot saveFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
            fileName = QFileDialog.getSaveFileName()
            
            if len(fileName[0]) >  0:
                # Sauvegarde le contenu du canvas dans le fichier indiqué par la boîte de dialogue
                fichier = open(fileName[0] + ".txt", "wt")
                fichier.write(string)
                fichier.close()
            
        else:
            content = self.textEdit.toPlainText()
            self.textEdit.setPlainText( content + "\n" + string)
        

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    
    window.show()
    app.exec_()
