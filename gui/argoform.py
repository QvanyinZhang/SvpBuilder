from datetime import timezone

import numpy as np
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QListView, QTableView, \
    QPushButton, QFileDialog
from PyQt6.QtGui import QGuiApplication, QAction, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QDir, QAbstractTableModel, QModelIndex, pyqtSignal
from Algorithm.argoreader import SeaSoundField
import xarray as xr


class Ui_ArgoForm(QWidget):
    # 向父窗体发送声剖数据
    data_signal = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setWindowTitle("Argo")
        self.resize(800,600)

        self.file_listView = QListView()
        self.list_model = QStandardItemModel()
        self.file_listView.setModel(self.list_model)

        self.vars_listView = QListView()
        self.vars_model = QStandardItemModel()
        self.vars_listView.setModel(self.vars_model)

        self.info_tableView = QTableView()
        self.info_model = ArrayTableModel()
        self.info_tableView.setModel(self.info_model)

        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove")
        self.import_btn = QPushButton("Import")

        self.init_layout()
        self.init_connect()

        self.data = []
        self.file_index = -1
        self.var_name = ''





    def init_layout(self):
        # 按钮布局
        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.add_btn)
        layout_btn.addWidget(self.remove_btn)
        layout_btn.addWidget(self.import_btn)
        layout_btn.addStretch()

        layout_left = QVBoxLayout()
        layout_left.addWidget(self.file_listView)
        layout_left.addLayout(layout_btn)

        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left, 2)
        layout_main.addWidget(self.vars_listView, 1)
        layout_main.addWidget(self.info_tableView, 3)
        self.setLayout(layout_main)


    def init_connect(self):
        self.add_btn.clicked.connect(self.on_addBtn_clicked)
        self.remove_btn.clicked.connect(self.on_removeBtn_clicked)
        self.import_btn.clicked.connect(self.on_importBtn_clicked)
        self.file_listView.clicked.connect(self.on_item_clicked)
        self.vars_listView.clicked.connect(self.on_varItem_clicked)


    def showEvent(self, event):
        # 如果有父窗体，则计算居中位置
        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            dialog_geometry = self.frameGeometry()
            dialog_geometry.moveCenter(parent_geometry.center())
            self.move(dialog_geometry.topLeft())
        super().showEvent(event)

    def on_addBtn_clicked(self):
        file_paths,_ = QFileDialog.getOpenFileNames(self, "Select Argo data file(s)", r"D:\MBdata\DataSelection_804fac33", "NetCDF(*.nc);;CSV(*.csv)")
        if file_paths:
            for file_path in file_paths:
                ds = xr.open_dataset(file_path)
                self.data.append(ds)
                item = QStandardItem(file_path)
                self.list_model.appendRow(item)


    def on_removeBtn_clicked(self):
        indexes = self.file_listView.selectedIndexes()
        if indexes:
            row = indexes[0].row()
            self.data.pop(row)
            self.list_model.removeRow(row)
            self.vars_model.clear()
            self.info_model.clear()


    def on_importBtn_clicked(self):
        self.data_signal.emit(self.data)
        self.data.clear()
        self.list_model.clear()
        self.vars_model.clear()
        self.info_model.clear()
        self.close()


    def on_item_clicked(self, index):
        self.file_index = index.row()
        ds = self.data[self.file_index]
        self.vars_model.clear()
        self.info_model.clear()
        for var in ds.variables:
            if ds[var].dtype==object:
                continue
            item = QStandardItem(var)
            self.vars_model.appendRow(item)


    def on_varItem_clicked(self, index):
        ds = self.data[self.file_index]
        self.var_name = self.vars_model.data(index)
        data = ds[self.var_name]
        self.info_model.updateData(data)



class ArrayTableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        if data is None:
            data = xr.DataArray([[]])
        self.shape = data.shape
        self._data = data


    def rowCount(self, parent=QModelIndex()):
        return self.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            # 返回当前单元格数据的字符串形式
            element = self._data.data[index.row(), index.column()]
            if self._data.dtype == "datetime64[ns]":
                element = np.datetime_as_string(element, unit='s')
            return element.item()
        return None

    def updateData(self, new_data):
        """
        更新模型中的数据，并通知视图刷新
        """
        self.beginResetModel()
        if new_data.ndim == 1:
            new_data = new_data.expand_dims("x", axis=1)
        self._data = new_data.transpose()
        self.shape = self._data.shape
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self._data = xr.DataArray([[]])
        self.shape = self._data.shape
        self.endResetModel()