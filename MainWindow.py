# KOHLER Hector & BIEGAS Emilie

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Création d'une barre de menu
        menu = self.menuBar()
        fileMenu = menu.addMenu( "Fichier" ) 
        
        # Création de l'action New et ajout de cette action à la barre de menu
        actNew = QAction(QIcon("Images/new.png"), "New…", self)
        fileMenu.addAction(actNew)
        
        # Création de l'action Open et ajout de cette action à la barre de menu
        actOpen = QAction(QIcon("Images/open.png"), "Open…", self)
        fileMenu.addAction(actOpen)
        
        # Création de l'action Save et ajout de cette action à la barre de menu
        actSave = QAction(QIcon("Images/save.png"), "Save…", self)
        fileMenu.addAction(actSave)
        # Création de l'action Quit et ajout de cette action à la barre de menu
        actQuit = QAction(QIcon("Images/quit.png"), "Quit…", self)
        fileMenu.addAction(actQuit)
        # Création d'une barre d'outils
        tool = QToolBar("Barre")
        tool.addAction(actSave)
        tool.addAction(actNew)
        tool.addAction(actOpen)
        tool.addAction(actQuit)
        
        ToolBar = self.addToolBar(tool)
        
        # Accélérateurs clavier  
        actNew.setShortcut( QKeySequence("Ctrl+N" ) )
        actSave.setShortcut( QKeySequence("Ctrl+S" ) )
        actOpen.setShortcut( QKeySequence("Ctrl+O" ) )
        actQuit.setShortcut(QKeySequence("Ctrl+Q"))
        
        # Bulles d’aides
        actNew.setToolTip("New File")
        actSave.setToolTip("Save File")
        actOpen.setToolTip("Open File")
        actQuit.setToolTip("Quit File")
        
        # Zone centrale de la MainWindow
        self.textEdit = QTextEdit();
        textEditor = self.setCentralWidget(self.textEdit)
    
        # Barre de status         
        status = self.statusBar()
    
        # Connecter les slots aux actions correspondantes
        actNew.triggered.connect( self.newFile )
        actSave.triggered.connect( self.saveFile )
        actOpen.triggered.connect( self.openFile ) 
        actQuit.triggered.connect(self.quitApp)
        
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
        labelB.move(120, 120)
        
    def newFile(self):
        print("New")
        
    def openFile(self):
        print("Open")
        # Le slot openFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
        fileName = QFileDialog.getOpenFileName( self, "Open File", "/home/jana","*.txt") 
        print(fileName)
        
        # Lire le fichier via la boîte de dialogue et faire apparaître son contenu dans le QTextEdit
        fichier = open(fileName[0], "rt")
        texte = fichier.read()
        self.textEdit.setPlainText(str(texte)) 
        fichier.close()
	

    def saveFile(self):
        print("Save")	
        # Le slot saveFile() ouvre une boîte de dialogue permettant de récupérer un nom de fichier
        fileName = QFileDialog.getSaveFileName()      
        print(fileName)
        
        # Sauvegarde le contenu du QTextEdit dans le fichier indiqué par la boîte de dialogue
        fichier = open(fileName[0], "wt")
        fichier.write(str(self.textEdit.toPlainText()))
        fichier.close()
        
    #Redefinition de la méthode closeEvent() pour que celle-ci se comporte comme quitApp
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to close the window?',QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

    # Appuyer sur le bouton Quit a pour effet d’ouvrir un QMessageBox comportant des boutons
    # “Yes” et “No” permettant de demander confirmation avant de sortir de l’application
    def quitApp(self):
        print("Quit")	
        buttonReply=QMessageBox.question(self, 'Quit', "Do you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if buttonReply==QMessageBox.Yes:
            QApplication.quit()
            
    # Méthode associée au bouton Hello World     
    def helloWorld(self):
        print("Hello World")

def main(args):
    # Création d'une instance de QApplication
    app = QApplication(args)
    fenetre = MainWindow()      
    
    fenetre.show()
    app.exec_()


if __name__ == "__main__":
	main(sys.argv) 
    
