
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu
from PyQt6.QtGui import QGuiApplication, QAction
from .argoform import Ui_ArgoForm

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.argoForm = Ui_ArgoForm(self)
        self.setWindowTitle("SvpBuilder")

        # 设置窗口大小
        # 窗口居中，大小为屏幕的80%
        screen = QGuiApplication.primaryScreen().geometry()
        width = screen.width()
        height = screen.height()
        self.setGeometry(int(0.1*width),int(0.1*height),int(0.8*width),int(0.8*height))

        # 设置菜单
        menubar = self.menuBar()
        dataMenu = menubar.addMenu('Data')

        argoAct = QAction('Argo', self)
        dataMenu.addAction(argoAct)
        argoAct.triggered.connect(self.on_argoAct_triggered)


    def on_argoAct_triggered(self):

        self.argoForm.show()