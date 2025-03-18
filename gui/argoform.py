

from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QListView, QTableView, \
    QPushButton, QFileDialog
from PyQt6.QtGui import QGuiApplication, QAction, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QDir


class Ui_ArgoForm(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setWindowTitle("Argo")
        self.resize(800,600)

        # 设置文件名列表
        self.file_listView = QListView()
        self.list_model = QStandardItemModel()
        self.file_listView.setModel(self.list_model)

        self.info_tableView = QTableView()
        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove")

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.add_btn)
        layout_btn.addWidget(self.remove_btn)
        layout_btn.addStretch()

        layout_left = QVBoxLayout()
        layout_left.addWidget(self.file_listView)
        layout_left.addLayout(layout_btn)

        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left, 1)
        layout_main.addWidget(self.info_tableView, 3)
        self.setLayout(layout_main)

        self.add_btn.clicked.connect(self.on_addBtn_clicked)


    def showEvent(self, event):
        # 如果有父窗体，则计算居中位置
        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            dialog_geometry = self.frameGeometry()
            dialog_geometry.moveCenter(parent_geometry.center())
            self.move(dialog_geometry.topLeft())
        super().showEvent(event)

    def on_addBtn_clicked(self):
        file_paths,_ = QFileDialog.getOpenFileNames(self, "Select Argo data file(s)", QDir.currentPath(), "NetCDF(*.nc);;CSV(*.csv)")
        if file_paths:
            for file_path in file_paths:
                item = QStandardItem(file_path)
                self.list_model.appendRow(item)