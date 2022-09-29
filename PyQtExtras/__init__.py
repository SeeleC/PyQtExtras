from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QMouseEvent, QContextMenuEvent, QCursor, QPixmap
from PyQt5.QtWidgets import QLabel, QMenu, QAction, QWidget, QHBoxLayout, QPushButton, QVBoxLayout

__all__ = [
    'SelectableLabel',
    'ClickableLabel',
    'QLocker',
    'QLockerButton'
]


class SelectableLabel(QLabel):
    def __init__(self, *__args):
        super(SelectableLabel, self).__init__(*__args)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.context_menu = QMenu()

    def contextMenuEvent(self, ev: QContextMenuEvent) -> None:
        self.context_menu.exec_(QCursor.pos())

    def setContextMenu(self, context_menu: QMenu):
        self.context_menu = context_menu


class ClickableLabel(SelectableLabel):
    clicked = pyqtSignal()
    mouseEnter = pyqtSignal()
    mouseLeave = pyqtSignal()

    def __init__(self, *__args):
        super(ClickableLabel, self).__init__(*__args)

    def enterEvent(self, a0: QEvent) -> None:
        self.setText('<u>%s</u>' % self.text())
        self.mouseEnter.emit()

    def leaveEvent(self, a0: QEvent) -> None:
        self.setText(self.text()[3:-4])
        self.mouseLeave.emit()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()


class QLockerButton(QPushButton):
    def __init__(self, *__args):
        super(QLockerButton, self).__init__(*__args)

        self.layout = QHBoxLayout()
        self.image = QLabel()
        self.title = QLabel()
        self.pixmap_expand = None
        self.pixmap_fold = None

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.image.setFixedWidth(20)
        self.image.setScaledContents(True)
        self.image.setStyleSheet('background: transparent;')
        self.layout.addWidget(self.image)

        self.title.setStyleSheet('background: transparent;')
        self.layout.addWidget(self.title)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def setPixmap(self, pixmap_expand: QPixmap, pixmap_fold: QPixmap):
        self.pixmap_expand = pixmap_expand
        self.pixmap_fold = pixmap_fold
        self.image.setPixmap(pixmap_fold)

    def setText(self, a0: str):
        self.title.setText(a0)

    def setExpand(self, a0: bool):
        if a0 and self.pixmap_expand is not None:
            self.image.setPixmap(self.pixmap_expand)
        elif not a0 and self.pixmap_fold is not None:
            self.image.setPixmap(self.pixmap_fold)


class QLocker(QWidget):
    def __init__(self, parent=None):
        super(QLocker, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.content = QWidget()
        self.button = QLockerButton()

        self.button.setStyleSheet(
            'background: transparent;border: transparent;'
        )
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def setPixmap(self, pixmap_expand: QPixmap, pixmap_fold: QPixmap):
        self.button.setPixmap(pixmap_expand, pixmap_fold)

    def setText(self, a0: str):
        self.button.setText(a0)

    def setContentWidget(self, a0: QWidget):
        self.content = a0
        self.content.setVisible(False)
        self.button.clicked.connect(self.switch_visible)
        self.layout.addWidget(self.content)

    def switch_visible(self):
        if self.content.isVisible():
            self.content.setVisible(False)
            self.button.setExpand(False)
        else:
            self.content.setVisible(True)
            self.button.setExpand(True)
