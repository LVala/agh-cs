from PyQt5.QtGui import QPainter, QPixmap, QColor, QBrush, QPen
from PyQt5.QtWidgets import QAbstractButton, QAction, QWidget, QVBoxLayout, QLabel, QApplication, QMenu
from PyQt5.QtCore import Qt
import pyfm.qrc_resources

import os

class PicButton(QAbstractButton):
    def __init__(self, pixmap, x, y, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap = pixmap.scaled(x, y, Qt.KeepAspectRatio)
        self.pixmap_copy = pixmap
        self.pixmap_copy = pixmap.scaled(x, y, Qt.KeepAspectRatio)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def highlight(self):
        mask = QPainter(self.pixmap)
        brush = QBrush(QColor(0,0,0,128))
        pen = QPen(QColor(0,0,0,0))
        mask.setBrush(brush)
        mask.setPen(pen)
        mask.drawRect(0,0,200,200)
        self.update()

    def dehighlight(self):
        self.pixmap = self.pixmap_copy.copy()
        self.update()

    def sizeHint(self):
        return self.pixmap.size()

class FileButton(QWidget):
    def __init__(self, path, x, y, parent=None):
        super().__init__()
        pixmap = QPixmap(":folder.svg") if os.path.isdir(path) else QPixmap(":file.svg")
        self.parent = parent;
        self.image = PicButton(pixmap, x, y, parent=self)
        self.image.setFixedSize(x, y)
        self.setFixedWidth(y+30)

        self.path = path
        self.label = QLabel(path.split(os.sep)[-1])
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.label)

        self.image.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.image.mouseReleaseEvent = self.mouseReleaseEvent

    def contextMenuEvent(self, event):
        context_menu = QMenu(self);

        separator1 = QAction(self)
        separator1.setSeparator(True)
        separator2 = QAction(self)
        separator2.setSeparator(True)
        separator3 = QAction(self)
        separator3.setSeparator(True)

        context_menu.addAction(self.parent.open_action)
        context_menu.addAction(separator1)
        context_menu.addAction(self.parent.cut_action)
        context_menu.addAction(self.parent.copy_action)
        context_menu.addAction(self.parent.remove_action)
        context_menu.addAction(separator2)
        context_menu.addAction(self.parent.rename_action)
        context_menu.addAction(separator3)
        context_menu.addAction(self.parent.get_prop_action)

        self.parent.manage_highlighted(self, False)
        context_menu.exec_(self.mapToGlobal(event.pos()))
    
    def highlight(self):
        self.image.highlight() 
    
    def dehighlight(self):
        self.image.dehighlight()
    
    def mouseDoubleClickEvent(self, event):
        self.parent.jump_to_dir(self.path, True)

    def mouseReleaseEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if self.parent.cur_path != self.path:
            self.parent.manage_highlighted(self, modifiers == Qt.ControlModifier)
