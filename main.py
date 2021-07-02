################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys       #text,tile,back = #2BAE66,#FCF6F5,#A2A2A1 - GREEEN   #FEE715
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import pickle

textColor = '#FEE715'
tileColor = '#1a1a1c'

clicked = False
# GUI FILE
from grid_layout_ui import Ui_MainWindow,Ui_TodoList

class TodoItem:
    def __init__(self, index,frame, header, content, delete):
        self.index = index
        self.frame = frame
        self.header = header
        self.content = content
        self.delete = delete

TodoList = []

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlag(QtCore.Qt.Tool)
        self.homeWindow()

    def homeWindow(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnResizeWindow.clicked.connect(self.resizeMainWindow)
        self.ui.exitButton.clicked.connect(lambda:self.myexit())

        self.ui._1todolistButton.clicked.connect(lambda :self.goto('todo'))
    
        # SHOW WINDOW
        self.show()
    
    def theme(self,t):
        if t=='dark':
            self.ui.textColor = '#FEE715'
            self.ui.tileColor = '#1a1a1c'
        if t=='light':
            self.ui.textColor = '#2BAE66'
            self.ui.tileColor = '#FCF6F5'
        self.ui.update()

    def myexit(self):
        sys.exit()

    def todo(self):
        global TodoList
        self.ui = Ui_TodoList()
        self.ui.setupUi(self)
        TodoList = []
        self.init_todoItems()
        self.ui.btnResizeWindow.clicked.connect(self.resizeMainWindow)
        self.ui.exitButton.clicked.connect(lambda:self.myexit())
        self.ui.addItem.clicked.connect(self.addItem)
        self.ui.backButton.clicked.connect(self.saveTODO)
        self.ui.darkButton.clicked.connect(lambda:self.theme('dark'))
        self.ui.lightButton.clicked.connect(lambda:self.theme('light'))
        self.ui.solarButton.clicked.connect(lambda:self.theme('solar'))
        self.show()

    def saveTODO(self):
        myTodo = []
        for i in TodoList:
            if i.frame.isHidden():
                pass
            else:
                myTodo.append(tuple([i.header.displayText(),i.content.toPlainText()]))
        with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump(myTodo, f)
        self.goto('home')

    def init_todoItems(self):
        try:
            with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
                My = pickle.load(f)
            for head,cont in My:
                self.addItem()
                self.ui.itemHeader.setText(head)
                self.ui.itemCONTENT.setPlainText(cont)
        except:
            pass


    def addItem(self):
        index = len(TodoList)
        self.ui.itemFrame = QFrame(self.ui.scrollAreaWidgetContents)
        self.ui.itemFrame.setMinimumSize(QSize(0, 121))
        self.ui.itemFrame.setStyleSheet("border-radius: 20px;\n"
"background-color: "+self.ui.tileColor+";\n"
"color:"+self.ui.textColor+";")
        self.ui.itemFrame.setFrameShape(QFrame.StyledPanel)
        self.ui.itemFrame.setFrameShadow(QFrame.Raised)
        self.ui.itemFrame.setObjectName("itemFrame")
        self.ui.itemHeader = QLineEdit(self.ui.itemFrame)
        self.ui.itemHeader.setGeometry(QRect(10, 0, 311, 41))
        self.ui.itemHeader.setStyleSheet("font: 18px \"Franklin Gothic Book\";font-weight:bold;\n"
"border-bottom: 1px solid white;\n"
"border-radius: 0px;\n"
"")
        self.ui.itemHeader.setAlignment(Qt.AlignCenter)
        self.ui.itemHeader.setObjectName("itemHeader")
        self.ui.itemHeader.setText("")
        self.ui.itemCONTENT = QPlainTextEdit(self.ui.itemFrame)
        self.ui.itemCONTENT.setGeometry(QRect(20, 50, 301, 51))
        self.ui.itemCONTENT.setStyleSheet("color:white;")
        self.ui.itemCONTENT.setObjectName("itemCONTENT")
        self.ui.itemCONTENT.setPlainText("")
        self.ui.itemDelete = QPushButton(self.ui.itemFrame)
        self.ui.itemDelete.setGeometry(QRect(10, 5, 20, 31))
        self.ui.itemDelete.setStyleSheet("color:red;")
        self.ui.itemDelete.setObjectName("itemDelete")
        self.ui.itemDelete.setText("X")
        self.ui.itemDelete.clicked.connect(lambda:self.deleteIt(index))
        thisItem = TodoItem(index,self.ui.itemFrame,self.ui.itemHeader,self.ui.itemCONTENT,self.ui.itemDelete)
        TodoList.append(thisItem)
        self.ui.verticalLayout.addWidget(self.ui.itemFrame)

    def deleteIt(self, i):
        TodoList[i].frame.hide()
        #if len(TodoList)==1:
        #    TodoList.pop(0).frame.hide()
        #else:
        #    TodoList.pop(i).frame.hide()


    def goto(self,link):
        global clicked
        if link=="todo":
            self.todo()
        elif link == "home":
            self.homeWindow()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()
    def mouseReleaseEvent(self, event):
        self.moveFlag = False
        self.setCursor(Qt.ArrowCursor)


    def resizeMainWindow(self):
        # CREATE ANIMATION
        global clicked
        if clicked:
            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(500)
            self.animation.setEndValue(QtCore.QSize(431,94))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()
            clicked = False
        else:
            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(500)
            self.animation.setEndValue(QtCore.QSize(431,601))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()
            clicked = True
        #RETRACT AND SHOW TRANSITION


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())