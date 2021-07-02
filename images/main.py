################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

clicked = False
# GUI FILE
from grid_layout_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.ui = Ui_MainWindow()

        self.ui.btnResizeWindow.clicked.connect(self.resizeMainWindow)
        self.ui.exitButton.clicked.connect(lambda:self.close())

        # SHOW WINDOW
        self.show()
    
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
            self.animation.setDuration(1000)
            self.animation.setEndValue(QtCore.QSize(431,94))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()
            clicked = False
        else:
            self.animation = QPropertyAnimation(self, b"size")
            self.animation.setDuration(1000)
            self.animation.setEndValue(QtCore.QSize(431,601))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
            self.animation.start()
            clicked = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())