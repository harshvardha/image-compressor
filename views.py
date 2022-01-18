import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image
import os
from struct import *
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Image Compressor"
        self.left = 500
        self.top = 50
        self.width = 400
        self.height = 600
        self.imageWidth = 0
        self.fileName = ""
        self.bitLength = 0
        self.files = []
        self.setFixedSize(self.width, self.height)
        self.setObjectName("mainWindow")
        self.statusBar().setObjectName("status")
        with open("design.qss", 'r') as designFile:
            self.setStyleSheet(designFile.read())
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # main window first option for compressing single file
        self.singleFileCompressOptionFrame = QFrame(self)
        self.singleFileCompressOptionFrame.setObjectName("optionFrame")
        self.singleFileCompressOptionFrame.move(50, 10)
        self.singleFileCompressOptionFrame.mousePressEvent = self.singleImageFileOption

        # label for single file compress frame
        self.singleFileLabel = QLabel(self.singleFileCompressOptionFrame)
        self.singleFileLabel.setText("Compress Single Image File")
        self.singleFileLabel.move(35, 50)
        self.singleFileLabel.setObjectName("selectOption")

        # main window second option for compressing a directory containing multiple images
        self.directoryCompressOptionFrame = QFrame(self)
        self.directoryCompressOptionFrame.setObjectName("optionFrame")
        self.directoryCompressOptionFrame.move(50, 160)
        self.directoryCompressOptionFrame.mousePressEvent = self.imageDirectoryCompressOption

        # label for directory compress option frame
        self.fileDirectoryLabel = QLabel(self.directoryCompressOptionFrame)
        self.fileDirectoryLabel.setText("Compress a complete directory")
        self.fileDirectoryLabel.move(18, 50)
        self.fileDirectoryLabel.setObjectName("selectOption")

        # main window third option for compressing a single text file
        self.singleTextFileCompress = QFrame(self)
        self.singleTextFileCompress.setObjectName("optionFrame")
        self.singleTextFileCompress.move(50, 310)
        self.singleTextFileCompress.mousePressEvent = self.singleTextFileOption

        # label for single text file compress frame
        self.singleTextFileLabel = QLabel(self.singleTextFileCompress)
        self.singleTextFileLabel.setText("Compress a single text file")
        self.singleTextFileLabel.move(35, 50)
        self.singleTextFileLabel.setObjectName("selectOption")

        # main window 4th option to compress text files directory
        self.textFileDirectoryCompress = QFrame(self)
        self.textFileDirectoryCompress.setObjectName("optionFrame")
        self.textFileDirectoryCompress.move(50, 460)
        self.textFileDirectoryCompress.mousePressEvent = self.textFilesDirectoryOption

        # label for 4th option to compress text files directory
        self.textFilesDirectoryLabel = QLabel(self.textFileDirectoryCompress)
        self.textFilesDirectoryLabel.setText("Compress multiple text files")
        self.textFilesDirectoryLabel.move(35, 50)
        self.textFilesDirectoryLabel.setObjectName("selectOption")
        self.show()
 
    def singleImageFileOption(self, event):
        self.singleFileCompressOptionFrame.close()
        self.directoryCompressOptionFrame.close()
        self.singleTextFileCompress.close()
        self.textFileDirectoryCompress.close()

        # creating a new container frame for selecting the image file
        self.selectSingleFileFrame = QFrame(self)
        self.selectSingleFileFrame.setObjectName("selectFileFrame")
        self.selectSingleFileFrame.move(50, 150)

        # back arrow to navigate back to main window
        self.backArrowLabel = QLabel(self.selectSingleFileFrame)
        self.backArrowLabel.setTextFormat(Qt.RichText)
        self.backArrowLabel.setText("&#8592;")
        self.backArrowLabel.move(10, 10)
        self.backArrowLabel.setObjectName("backArrow")
        self.backArrowLabel.mousePressEvent = self.navigateBack1

        # header label
        self.headerLabel = QLabel(self.selectSingleFileFrame)
        self.headerLabel.setText("Compress Image")
        self.headerLabel.setObjectName("frameHeaderLabel")
        self.headerLabel.move(73, 15)

        # choose image label
        self.chooseImageLabel = QLabel(self.selectSingleFileFrame)
        self.chooseImageLabel.setText("Choose Image")
        self.chooseImageLabel.setObjectName("selectionLabel")
        self.chooseImageLabel.move(30, 60)

        # image path edit text
        self.pathEditText = QLineEdit(self.selectSingleFileFrame)
        self.pathEditText.setObjectName("pathEditText")
        self.pathEditText.move(30, 93)

        # file browse button
        self.fileBrowseButton = QPushButton(self.selectSingleFileFrame)
        self.fileBrowseButton.setText("...")
        self.fileBrowseButton.setObjectName("browseButton")
        self.fileBrowseButton.clicked.connect(self.browseImageFile)
        self.fileBrowseButton.move(250, 93)

        # choose image quality label
        self.chooseImageQualityLabel = QLabel(self.selectSingleFileFrame)
        self.chooseImageQualityLabel.setText("Choose Quality")
        self.chooseImageQualityLabel.setObjectName("selectionLabel")
        self.chooseImageQualityLabel.move(30, 140)

        # image width edit text
        self.imageWidthEditText = QLineEdit(self.selectSingleFileFrame)
        self.imageWidthEditText.setObjectName("imageWidthEditText")
        self.imageWidthEditText.move(30, 170)

        # image quality combobox
        self.qualityCombobox = QComboBox(self.selectSingleFileFrame)
        self.qualityCombobox.addItem("High")
        self.qualityCombobox.addItem("Medium")
        self.qualityCombobox.addItem("Low")
        self.qualityCombobox.move(130, 170)
        self.qualityCombobox.currentIndexChanged.connect(self.qualityCurrentValue)
        self.qualityCombobox.setObjectName("qualityCombobox")

        # compress image button
        self.compressImageButton = QPushButton(self.selectSingleFileFrame)
        self.compressImageButton.setText("Compress")
        self.compressImageButton.setObjectName("compressButton")
        self.compressImageButton.move(93, 250)
        self.compressImageButton.clicked.connect(self.compressImage)
        self.selectSingleFileFrame.show()
    
    def singleTextFileOption(self, event):
        self.singleFileCompressOptionFrame.close()
        self.directoryCompressOptionFrame.close()
        self.singleTextFileCompress.close()
        self.textFileDirectoryCompress.close()

        # creating a new container frame for selecting the text file
        self.singleTextFileFrame = QFrame(self)
        self.singleTextFileFrame.setObjectName("selectFileFrame")
        self.singleTextFileFrame.move(50, 150)

        # back arrow to navigate back to main window
        self.backArrowLabel = QLabel(self.singleTextFileFrame)
        self.backArrowLabel.setTextFormat(Qt.RichText)
        self.backArrowLabel.setText("&#8592;")
        self.backArrowLabel.move(10, 10)
        self.backArrowLabel.setObjectName("backArrow")
        self.backArrowLabel.mousePressEvent = self.navigateBack3

        # header label
        self.headerLabel = QLabel(self.singleTextFileFrame)
        self.headerLabel.setText("Compress Text File")
        self.headerLabel.setObjectName("frameHeaderLabel")
        self.headerLabel.move(73, 15)

        # choose text file label
        self.chooseTextFileLabel = QLabel(self.singleTextFileFrame)
        self.chooseTextFileLabel.setText("Choose Text File")
        self.chooseTextFileLabel.setObjectName("selectionLabel")
        self.chooseTextFileLabel.move(30, 60)

        # text file path edit text
        self.pathEditText = QLineEdit(self.singleTextFileFrame)
        self.pathEditText.setObjectName("pathEditText")
        self.pathEditText.move(30, 93)

        # file browse button
        self.fileBrowseButton = QPushButton(self.singleTextFileFrame)
        self.fileBrowseButton.setText("...")
        self.fileBrowseButton.setObjectName("browseButton")
        self.fileBrowseButton.clicked.connect(self.browseTextFile)
        self.fileBrowseButton.move(250, 93)

        # choose bit length label
        self.chooseBitLengthLabel = QLabel(self.singleTextFileFrame)
        self.chooseBitLengthLabel.setText("Choose bit length")
        self.chooseBitLengthLabel.setObjectName("selectionLabel")
        self.chooseBitLengthLabel.move(30, 140)

        # bit length edit text
        self.bitLengthEditText = QLineEdit(self.singleTextFileFrame)
        self.bitLengthEditText.setObjectName("imageWidthEditText")
        self.bitLengthEditText.setText("1024")
        self.bitLengthEditText.move(30, 170)

        # bit length combobox
        self.bitLengthCombobox = QComboBox(self.singleTextFileFrame)
        self.bitLengthCombobox.addItem("High")
        self.bitLengthCombobox.addItem("Medium")
        self.bitLengthCombobox.addItem("Low")
        self.bitLengthCombobox.move(130, 170)
        self.bitLengthCombobox.currentIndexChanged.connect(self.bitLengthCurrentValue)
        self.bitLengthCombobox.setObjectName("qualityCombobox")

        # compress text file button
        self.compressFileButton = QPushButton(self.singleTextFileFrame)
        self.compressFileButton.setText("Compress")
        self.compressFileButton.setObjectName("compressButton")
        self.compressFileButton.move(93, 250)
        self.compressFileButton.clicked.connect(self.compressTextFile)
        self.singleTextFileFrame.show()
    
    def imageDirectoryCompressOption(self, event):
        self.singleFileCompressOptionFrame.close()
        self.directoryCompressOptionFrame.close()
        self.singleTextFileCompress.close()
        self.textFileDirectoryCompress.close()

        # creating a new container frame for selecting the directory to compress
        self.selectDirectoryFrame = QFrame(self)
        self.selectDirectoryFrame.setObjectName("selectDirectoryFrame")
        self.selectDirectoryFrame.move(50, 96)

        # back arrow to navigate back to main window
        self.backArrowLabel = QLabel(self.selectDirectoryFrame)
        self.backArrowLabel.setTextFormat(Qt.RichText)
        self.backArrowLabel.setText("&#8592;")
        self.backArrowLabel.move(10, 10)
        self.backArrowLabel.setObjectName("backArrow")
        self.backArrowLabel.mousePressEvent = self.navigateBack2

        # header label
        self.headerLabel = QLabel(self.selectDirectoryFrame)
        self.headerLabel.setText("Compress Image")
        self.headerLabel.setObjectName("frameHeaderLabel")
        self.headerLabel.move(73, 15)

        # choose images directory label
        self.chooseImageDirectoryLabel = QLabel(self.selectDirectoryFrame)
        self.chooseImageDirectoryLabel.setText("Choose source directory")
        self.chooseImageDirectoryLabel.setObjectName("selectionLabel")
        self.chooseImageDirectoryLabel.move(30, 60)

        # source directory path edit text
        self.sourceDirectoryPath = QLineEdit(self.selectDirectoryFrame)
        self.sourceDirectoryPath.setObjectName("pathEditText")
        self.sourceDirectoryPath.move(30, 93)

        # source directory browse button
        self.sourceDirectoryBrowseButton = QPushButton(self.selectDirectoryFrame)
        self.sourceDirectoryBrowseButton.setText("...")
        self.sourceDirectoryBrowseButton.setObjectName("browseButton")
        self.sourceDirectoryBrowseButton.clicked.connect(self.selectSourceDirectory)
        self.sourceDirectoryBrowseButton.move(250, 93)

        # destination directory label
        self.destinationDirectoryLabel = QLabel(self.selectDirectoryFrame)
        self.destinationDirectoryLabel.setText("Choose destination directory")
        self.destinationDirectoryLabel.setObjectName("selectionLabel")
        self.destinationDirectoryLabel.move(30, 140)

        # destination directory path edit text
        self.destinationDirectoryPath = QLineEdit(self.selectDirectoryFrame)
        self.destinationDirectoryPath.setObjectName("pathEditText")
        self.destinationDirectoryPath.move(30, 170)

        # destination directory browse button
        self.destinationBrowseButton = QPushButton(self.selectDirectoryFrame)
        self.destinationBrowseButton.setText("...")
        self.destinationBrowseButton.setObjectName("browseButton")
        self.destinationBrowseButton.clicked.connect(self.selectDestinationDirectory)
        self.destinationBrowseButton.move(250, 170)

        # choose image quality label
        self.chooseImageQualityLabel = QLabel(self.selectDirectoryFrame)
        self.chooseImageQualityLabel.setText("Choose Quality")
        self.chooseImageQualityLabel.setObjectName("selectionLabel")
        self.chooseImageQualityLabel.move(30, 217)

        # image width edit text
        self.imageWidthEditText = QLineEdit(self.selectDirectoryFrame)
        self.imageWidthEditText.setObjectName("imageWidthEditText")
        self.imageWidthEditText.move(30, 245)

        # image quality combobox
        self.qualityCombobox = QComboBox(self.selectDirectoryFrame)
        self.qualityCombobox.addItem("High")
        self.qualityCombobox.addItem("Medium")
        self.qualityCombobox.addItem("Low")
        self.qualityCombobox.move(130, 245)
        self.qualityCombobox.currentIndexChanged.connect(self.qualityCurrentValue)
        self.qualityCombobox.setObjectName("qualityCombobox")

        # compress image button
        self.compressImageButton = QPushButton(self.selectDirectoryFrame)
        self.compressImageButton.setText("Compress")
        self.compressImageButton.setObjectName("compressButton")
        self.compressImageButton.move(93, 340)
        self.compressImageButton.clicked.connect(self.compressImage)
        self.selectDirectoryFrame.show()

    def textFilesDirectoryOption(self, event):
        self.singleFileCompressOptionFrame.close()
        self.directoryCompressOptionFrame.close()
        self.singleTextFileCompress.close()
        self.textFileDirectoryCompress.close()

        # creating a new container frame for selecting the directory to compress
        self.selectDirectoryFrame = QFrame(self)
        self.selectDirectoryFrame.setObjectName("selectDirectoryFrame")
        self.selectDirectoryFrame.move(50, 96)

        # back arrow to navigate back to main window
        self.backArrowLabel = QLabel(self.selectDirectoryFrame)
        self.backArrowLabel.setTextFormat(Qt.RichText)
        self.backArrowLabel.setText("&#8592;")
        self.backArrowLabel.move(10, 10)
        self.backArrowLabel.setObjectName("backArrow")
        self.backArrowLabel.mousePressEvent = self.navigateBack4

        # header label
        self.headerLabel = QLabel(self.selectDirectoryFrame)
        self.headerLabel.setText("Compress Text Files")
        self.headerLabel.setObjectName("frameHeaderLabel")
        self.headerLabel.move(73, 15)

        # choose images directory label
        self.chooseTextFileDirectoryLabel = QLabel(self.selectDirectoryFrame)
        self.chooseTextFileDirectoryLabel.setText("Choose source directory")
        self.chooseTextFileDirectoryLabel.setObjectName("selectionLabel")
        self.chooseTextFileDirectoryLabel.move(30, 60)

        # source directory path edit text
        self.sourceDirectoryPath = QLineEdit(self.selectDirectoryFrame)
        self.sourceDirectoryPath.setObjectName("pathEditText")
        self.sourceDirectoryPath.move(30, 93)

        # source directory browse button
        self.sourceDirectoryBrowseButton = QPushButton(self.selectDirectoryFrame)
        self.sourceDirectoryBrowseButton.setText("...")
        self.sourceDirectoryBrowseButton.setObjectName("browseButton")
        self.sourceDirectoryBrowseButton.clicked.connect(self.textFilesSourceDirectory)
        self.sourceDirectoryBrowseButton.move(250, 93)

        # destination directory label
        self.destinationDirectoryLabel = QLabel(self.selectDirectoryFrame)
        self.destinationDirectoryLabel.setText("Choose destination directory")
        self.destinationDirectoryLabel.setObjectName("selectionLabel")
        self.destinationDirectoryLabel.move(30, 140)

        # destination directory path edit text
        self.destinationDirectoryPath = QLineEdit(self.selectDirectoryFrame)
        self.destinationDirectoryPath.setObjectName("pathEditText")
        self.destinationDirectoryPath.move(30, 170)

        # destination directory browse button
        self.destinationBrowseButton = QPushButton(self.selectDirectoryFrame)
        self.destinationBrowseButton.setText("...")
        self.destinationBrowseButton.setObjectName("browseButton")
        self.destinationBrowseButton.clicked.connect(self.selectDestinationDirectory)
        self.destinationBrowseButton.move(250, 170)

        # choose bit length label
        self.chooseBitLengthLabel = QLabel(self.selectDirectoryFrame)
        self.chooseBitLengthLabel.setText("Choose bit length")
        self.chooseBitLengthLabel.setObjectName("selectionLabel")
        self.chooseBitLengthLabel.move(30, 217)

        # bit length edit text
        self.bitLengthEditText = QLineEdit(self.selectDirectoryFrame)
        self.bitLengthEditText.setObjectName("imageWidthEditText")
        self.bitLengthEditText.move(30, 245)

        # bit length combobox
        self.bitLengthCombobox = QComboBox(self.selectDirectoryFrame)
        self.bitLengthCombobox.addItem("High")
        self.bitLengthCombobox.addItem("Medium")
        self.bitLengthCombobox.addItem("Low")
        self.bitLengthCombobox.move(130, 245)
        self.bitLengthCombobox.currentIndexChanged.connect(self.bitLengthCurrentValue)
        self.bitLengthCombobox.setObjectName("qualityCombobox")

        # compress text files directory button
        self.compressTextFileButton = QPushButton(self.selectDirectoryFrame)
        self.compressTextFileButton.setText("Compress")
        self.compressTextFileButton.setObjectName("compressButton")
        self.compressTextFileButton.move(93, 340)
        self.compressTextFileButton.clicked.connect(self.compressTextFile)
        self.selectDirectoryFrame.show()

    def navigateBack1(self, event):
        self.selectSingleFileFrame.close()
        self.singleFileCompressOptionFrame.setVisible(True)
        self.directoryCompressOptionFrame.setVisible(True)
        self.singleTextFileCompress.setVisible(True)
        self.textFileDirectoryCompress.setVisible(True)
        self.statusBar().showMessage("")
    
    def navigateBack2(self, event):
        self.selectDirectoryFrame.close()
        self.singleFileCompressOptionFrame.setVisible(True)
        self.directoryCompressOptionFrame.setVisible(True)
        self.singleTextFileCompress.setVisible(True)
        self.textFileDirectoryCompress.setVisible(True)
        self.statusBar().showMessage("")

    def navigateBack3(self, event):
        self.singleTextFileFrame.close()
        self.singleFileCompressOptionFrame.setVisible(True)
        self.directoryCompressOptionFrame.setVisible(True)
        self.singleTextFileCompress.setVisible(True)
        self.textFileDirectoryCompress.setVisible(True)
        self.statusBar().showMessage("")
    
    def navigateBack4(self, event):
        self.selectDirectoryFrame.close()
        self.singleFileCompressOptionFrame.setVisible(True)
        self.directoryCompressOptionFrame.setVisible(True)
        self.singleTextFileCompress.setVisible(True)
        self.textFileDirectoryCompress.setVisible(True)
        self.statusBar().showMessage("")
    
    def browseImageFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);; JPEG (*.jpg);; PNG (*.png)")
        if (self.fileName):
            self.pathEditText.setText(self.fileName)
            img = Image.open(self.fileName)
            self.imageWidth = img.width
            self.qualityCurrentValue()
    
    def browseTextFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "All Files (*);; (*.txt)")
        if(self.fileName):
            self.pathEditText.setText(self.fileName)
    
    def selectSourceDirectory(self):
        sourceDirectory = QFileDialog.getExistingDirectory(self, 'select source directory')
        self.sourceDirectoryPath.setText(sourceDirectory)
        self.files = os.listdir(sourceDirectory)
        img = Image.open(os.path.join(sourceDirectory, self.files[0]))
        self.imageWidth = img.width
        self.imageWidthEditText.setText(str(self.imageWidth//4))

    def textFilesSourceDirectory(self):
        sourceDirectory = QFileDialog.getExistingDirectory(self, 'select source directory')
        self.sourceDirectoryPath.setText(sourceDirectory)
        self.files = os.listdir(sourceDirectory)

    def selectDestinationDirectory(self):
        destinationDirectory = QFileDialog.getExistingDirectory(self, 'select destination directory')
        self.destinationDirectoryPath.setText(destinationDirectory)

    def qualityCurrentValue(self):
        if(self.qualityCombobox.currentText()=="High"):
            self.imageWidthEditText.setText(str(self.imageWidth//4))
        elif(self.qualityCombobox.currentText()=="Medium"):
            self.imageWidthEditText.setText(str(self.imageWidth//2))
        elif(self.qualityCombobox.currentText()=="Low"):
            self.imageWidthEditText.setText(str(self.imageWidth))
    
    def bitLengthCurrentValue(self):
        if(self.bitLengthCombobox.currentText()=="High"):
            self.bitLengthEditText.setText("1024")
        elif(self.bitLengthCombobox.currentText()=="Medium"):
            self.bitLengthEditText.setText("512")
        elif(self.bitLengthCombobox.currentText()=="Low"):
            self.bitLengthEditText.setText("256")
    
    def compressImage(self):
        self.imageWidth = int(self.imageWidthEditText.text())
        self.imageWidthEditText.setDisabled(True)
        self.qualityCombobox.setDisabled(True)
        self.compressImageButton.setDisabled(True)
        try:
            if(len(self.files)==0):
                img = Image.open(self.fileName)
                wPercent = (self.imageWidth/float(img.size[0]))
                hSize = int((float(img.size[1])*float(wPercent)))
                img = img.resize((self.imageWidth, hSize), Image.ANTIALIAS)
                img.save(self.fileName[: self.fileName.index('.')] + "Compressed" + self.fileName[self.fileName.index('.') :])
                self.statusBar().showMessage("Message : File Compressed")
            else:
                for file in self.files:
                    self.fileName = os.path.join(self.sourceDirectoryPath.text(), file)
                    destinationPath = os.path.join(self.destinationDirectoryPath.text(), file[:file.index('.')]+"Compressed"+file[file.index('.'):])
                    img = Image.open(self.fileName)
                    wPercent = (self.imageWidth/float(img.size[0]))
                    hSize = int((float(img.size[1])*float(wPercent)))
                    img = img.resize((self.imageWidth, hSize), Image.ANTIALIAS)
                    img.save(destinationPath)
                self.statusBar().showMessage("Message : Files Compressed")
        except:
            self.statusBar().showMessage("Message : Error Occured")
            return
        self.imageWidthEditText.setDisabled(False)
        self.qualityCombobox.setDisabled(False)
        self.compressImageButton.setDisabled(False)
    
    def compressTextFile(self):
        # taking the input file and the number of bits
        # defining the maximum table size
        # opening the input file
        # reading the input file and storing the file data into data variable
        try:       
            maximum_table_size = pow(2,int(self.bitLength))
            if(len(self.files)==0):
                print(self.fileName)   
                file = open(self.fileName)               
                data = file.read()                  

                # Building and initializing the dictionary.
                dictionary_size = 256                   
                dictionary = {chr(i): i for i in range(dictionary_size)}    
                string = ""             # String is null.
                compressed_data = []    # variable to store the compressed data.

                # iterating through the input symbols.
                # LZW Compression algorithm
                for symbol in data:                     
                    string_plus_symbol = string + symbol # get input symbol.
                    if string_plus_symbol in dictionary: 
                        string = string_plus_symbol
                    else:
                        compressed_data.append(dictionary[string])
                        if(len(dictionary) <= maximum_table_size):
                            dictionary[string_plus_symbol] = dictionary_size
                            dictionary_size += 1
                        string = symbol

                if string in dictionary:
                    compressed_data.append(dictionary[string])

                # storing the compressed string into a file (byte-wise).
                out = self.fileName.split(".")[0]
                output_file = open(out + ".lzw", "wb")
                for data in compressed_data:
                    output_file.write(pack('>H',int(data)))
    
                output_file.close()
                file.close()
            else:
                for file in self.files:
                    self.fileName = os.path.join(self.sourceDirectoryPath.text(), file)
                    fil = open(self.fileName)
                    data = fil.read()

                    # Building and initializing the dictionary.
                    dictionary_size = 256                   
                    dictionary = {chr(i): i for i in range(dictionary_size)}    
                    string = ""             # String is null.
                    compressed_data = []    # variable to store the compressed data.

                    # iterating through the input symbols.
                    # LZW Compression algorithm
                    for symbol in data:                     
                        string_plus_symbol = string + symbol # get input symbol.
                        if string_plus_symbol in dictionary: 
                            string = string_plus_symbol
                        else:
                            compressed_data.append(dictionary[string])
                            if(len(dictionary) <= maximum_table_size):
                                dictionary[string_plus_symbol] = dictionary_size
                                dictionary_size += 1
                            string = symbol

                    if string in dictionary:
                        compressed_data.append(dictionary[string])

                    # storing the compressed string into a file (byte-wise).
                    out = self.fileName.split(".")[0]
                    output_file = open(out + ".lzw", "wb")
                    for data in compressed_data:
                        output_file.write(pack('>H',int(data)))
        
                    output_file.close()
                    fil.close()

        except:
            self.statusBar().showMessage("Message : Error Ocurred")
        self.statusBar().showMessage("Message : File Compressed")

if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
