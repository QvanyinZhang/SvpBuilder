

from PyQt6.QtWidgets import  QApplication
from gui.mainwindow import Ui_MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    # argo_form = Ui_ArgoForm()



    window.show()
    sys.exit(app.exec())

