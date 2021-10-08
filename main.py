from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os, sys
import win32api, win32print

path = ""

class win(QMainWindow):
    def __init__(self):
        super(win, self).__init__()
        uic.loadUi("editor.ui", self)
        self.show()

        self.actions()
    
    def actions(self):
        self.actionNew_File.triggered.connect(self.new_file)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionExitApp.triggered.connect(self.exit_app)
        self.actionCut.triggered.connect(self.textBody.cut)
        self.actionCopy.triggered.connect(self.textBody.copy)
        self.actionPaste.triggered.connect(self.textBody.paste)
        self.actionUndo.triggered.connect(self.textBody.undo)
        self.actionRedo.triggered.connect(self.textBody.redo)
        self.actionBold.triggered.connect(self.bold_text)
        self.actionItalic.triggered.connect(self.italic_text)
        self.actionUnderline.triggered.connect(self.underline_text)
        self.actionNormal.triggered.connect(self.normal_text)
        self.actionSelect_All.triggered.connect(self.textBody.selectAll)

        self.actionTB_NewFile.triggered.connect(self.new_file)
        self.actionTB_OpenFile.triggered.connect(self.open_file)
        self.actionTB_Save.triggered.connect(self.save_file)
        self.actionTB_Print.triggered.connect(self.print_file)
        self.actionTB_Undo.triggered.connect(self.textBody.undo)
        self.actionTB_Redo.triggered.connect(self.textBody.redo)
        self.actionTB_Cut.triggered.connect(self.textBody.cut)
        self.actionTB_Copy.triggered.connect(self.textBody.copy)
        self.actionTB_Paste.triggered.connect(self.textBody.paste)
        self.actionTB_SelectAll.triggered.connect(self.textBody.selectAll)

    def about(self):
        pass

    def new_file(self):
        if path != "":
            self.textBody.setPlainText("")
        else:
            mb = QMessageBox()
            mb.setWindowTitle("Note+ Dialog")
            mb.setText("Are you sure you would like your changes?")

            mb.addButton(QPushButton("Save"), QMessageBox.YesRole)
            mb.addButton(QPushButton("Don't Save"), QMessageBox.NoRole)
            mb.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

            a = mb.exec_()

            if a == 0:
                self.save_file()
            elif a == 1:
                self.textBody.setPlainText("")

    def open_file(self):
        op = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 
        "Open File", "C:\\", 
        "Note+ File (*.np);;Text Documents (*.txt);;All Files (*)", options=op)
        if file != "":
            with open(file, "r") as f:
                self.setWindowTitle(f"{file} - Note+")
                self.textBody.setPlainText(f.read())
                global path
                path = file

    def save_file(self):
        global path
        if path != "":
            file = open(path, "w")
            file.write(self.textBody.toPlainText())
        else:
            op = QFileDialog.Options()
            file, _ = QFileDialog.getSaveFileName(self, 
            "Save File", "C:\\", 
            "Note+ File (*.np);;Text Documents (*.txt);;All Files (*)", options=op)
            if file != "":
                with open(file, "w") as f:
                    f.write(self.textBody.toPlainText())
                    path = file

    def print_file(self):
        name = win32print.GetDefaultPrinter()
        print(name)

        if path != "":
            win32api.ShellExecute(0, "print", path, None, ".", 0)
        else:
            self.save_file()
            self.print_file()

    def exit_app(self):
        mb = QMessageBox()
        mb.setWindowTitle("Note+ Dialog")
        mb.setText("Do you want to save your file?")

        mb.addButton(QPushButton("Yes"), QMessageBox.YesRole)
        mb.addButton(QPushButton("No"), QMessageBox.NoRole)
        mb.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        a = mb.exec_()

        if a == 0:
            self.save_file()
        elif a == 1:
            quit(0)
    
    def bold_text(self):
        if self.textBody.fontWeight() != QFont.Bold:
            self.textBody.setFontWeight(QFont.Bold)
            return
        self.textBody.setFontWeight(QFont.Normal)
    
    def italic_text(self):
        state = self.textBody.fontItalic()
        self.textBody.setFontItalic(not(state))
    
    def underline_text(self):
        state = self.textBody.fontUnderline()
        self.textBody.setFontUnderline(not(state))
    
    def normal_text(self):
        self.textBody.setFontWeight(QFont.Normal)
        self.textBody.setFontUnderline(QFont.Normal)
        self.textBody.setFontItalic(QFont.Normal)

def main():
    app = QApplication([])
    window = win()
    app.exec_()

if __name__ == "__main__":
    main()