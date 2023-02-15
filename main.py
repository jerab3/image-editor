from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QMessageBox,QErrorMessage, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout) #Widgety
from PyQt5.QtGui import QPixmap #Preview
from PyQt5.QtCore import Qt #Udrzeni rozliseni
import os #Prace se soubory
from PIL import Image #Zakladni prace s obrazky
from PIL import ImageFilter #Filtry pro obrazky

#Vytvoreni aplikace
app = QApplication([])
win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Easy Editor')

#Prvky aplikace
preview_image = QLabel()
btn_dir = QPushButton("Folder")
lw_files = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")

#Pozicovani
finalLayout = QHBoxLayout()
left_side = QVBoxLayout()
right_side = QVBoxLayout()

left_side.addWidget(btn_dir)
left_side.addWidget(lw_files)

right_side.addWidget(preview_image, 95)

row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
right_side.addLayout(row_tools)
 
finalLayout.addLayout(left_side, 20)
finalLayout.addLayout(right_side, 80)

win.setLayout(finalLayout)

win.show()




workdir = ''

class ImageProcessor():

    #Konstruktor
    def __init__(self): #Funkce se spusti pri nahrání classy do proměnné => Vytvorime objekt
        self.image = None #Ulozeny obrazek (objekt typu Image) v promenne
        self.dir = None #Ulozena cesta do otevrene slozky
        self.filename = None #Nazev obrazku (pomaha pri preview) .../images/$filename
        self.save_dir = "Modified_Pictures/" #Nazev slozky s upravenymi obrazky .../imgs/$save_dir/upravenyobrazek.jpg
    ############

    #Zpracovani aplikace a dat
    def loadImage(self, dir, filename): #Pod funkce pro nahrati promennych do classy,
        self.dir = dir #Z parametru nastavi do prommene v classe
        self.filename = filename #-||-
        image_path = os.path.join(dir, filename) #Spoji se nam cesta k slozce s cestou k souboru
        self.image = Image.open(image_path) #Pomoci cesty k souboru a slozce otevreme obrazek

    def showImage(self, path): #Podfunkce na vytvoreni pixmapy, ktera nam vykresli obrazek do labelu
        preview_image.hide() 
        pixelMap = QPixmap(path) #Vytvortime QPixmap a dame mu cestu k obrazku, aby vedel ktery vykreslit
        width, height = preview_image.width(), preview_image.height()#Zjistime vysku a sirku plochy na obrazek z aplikace
        pixelMap = pixelMap.scaled(width, height, Qt.KeepAspectRatio)#Nastavime mu rozliseni, ktere bude pevne
        preview_image.setPixmap(pixelMap) #Nastavime pixmapu do labelu 
        preview_image.show()
    
    def saveImage(self): #Uloz obrazek
        path = os.path.join(self.dir, self.save_dir) #Cesta k slozce, nemusi existovat
        if not(os.path.exists(path) or os.path.isdir(path)):#Pokud neexistuje vytvor slozku, pokud existuje, tak uz je vytvorena
            os.mkdir(path)#Vytvoreni mkdir = Make Direction
        image_path = os.path.join(path,self.filename)#Cesta k obrazku ktery neexistuje
        self.image.save(image_path)#Ale tady si ho ulozime a uz existuje
    ############

    #Uprava obrazku
    def do_bw(self):#Funkce na cernobily filtr

        #Oprava chyby pouziti filtru bez vybrani obrazku
        try:
            self.image = self.image.convert("L")#Konvertace na cernobily obrazek
            self.saveImage() #Ulozime
            image_path = os.path.join(self.dir, self.save_dir, self.filename) #Dostaneme se k obrazkuco jsme ulozili
            self.showImage(image_path) #Ukazeme obrazek ze slozky(existuje nekde u nas na disku)
        except:
            errorMsg = QMessageBox() #Vytvoreni okna upozorneni na chybu
            errorMsg.setWindowTitle("Error") #Nastaveni titulku
            errorMsg.setText("Please select image, before using filters") #Nastaveni textu
            errorMsg.setStandardButtons(QMessageBox.Ok) #Nastaveni tlacitek
            errorMsg.setIcon(QMessageBox.Critical) #Nastaveni ikonky
            errorMsg.exec() #Spusteni okna upozorneni

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT) #Filter
        self.saveImage() #Ulozime kvuli preview
        image_path = os.path.join(self.dir, self.save_dir, self.filename) #Cesta k ulozenemu obrazku
        self.showImage(image_path) #Za pomoci cesty, ukaze obrazek na preview

    #To same dokola, muzeme pridat opravu chyby jak u cernobileho filteru
    def do_rotation_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_rotation_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    ############
workimage = ImageProcessor()#Vytvorime is ImageProcessor, ktery nam bude pomahat s ukazkou obrazku

def chooseWorkDir():
    global workdir #globalni, protoze pouzivame ve funkci "showFilenamesList()"
    workdir = QFileDialog.getExistingDirectory() #otevre dialog na vyber slozky

def filter(files, extensions): #funkce chce list souboru a koncovky

    result = []

    for soubor in files: #za kazdy soubor v files (soubor napr obrazek.png)
        for ext in extensions: #zkusi kazdou koncovku (napr .png)
            if(soubor.endswith(ext)): #pokud konci s ext
                result.append(soubor)
    
    return result

def showFilenamesList():
    #Pripony
    extensions = ['.jpg','.png','.jpeg']

    chooseWorkDir() # <--- dostaneme cestu slozky s obrazky

    filenames = os.listdir(workdir) # <---- dostaneme navzvy souborů do listu napr.(obrazek.png)

    filteredFileNames = filter(filenames, extensions)

    lw_files.clear()

    lw_files.addItems(filteredFileNames)


def showChosenImage():#Funkce ktera je pripojena na listwidget s obrazky, a spusti se po rozkliknuti obrazku
    filename = lw_files.currentItem().text()#Zjistime s listwidgetu nazev obrazku, .text() pouzivame, protoze obrazky mame pojmenovane nazvem.pripona
    workimage.loadImage(workdir, filename)#Vyvolame podfunkci loadImage, ktera nam nastavi promenne v objektu, ktere pouzijeme dale
    image_path = os.path.join(workimage.dir, workimage.filename)#Tady je napr pouzivame, spojujeme cesty
    workimage.showImage(image_path)#Volame metodu, ktera vytvori pixelMapu a spusti preview

lw_files.itemClicked.connect(showChosenImage)#Pripojujeme funkci k udalosti

#Pripojovani funkci k prvkum
btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_rotation_left)
btn_right.clicked.connect(workimage.do_rotation_right)
app.exec_()