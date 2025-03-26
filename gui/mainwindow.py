
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QListView, QPushButton, QRadioButton, QButtonGroup, \
    QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget
from PyQt6.QtGui import QGuiApplication, QAction
import pyqtgraph as pg
from .argoform import Ui_ArgoForm

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.argoForm = Ui_ArgoForm(self)
        self.argoForm.data_signal.connect(self.receive_data)

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

        # 设置其他窗口控件
        self.svp_listView = QListView()
        self.svp_plot = pg.PlotWidget()
        self.temp_btn = QRadioButton()
        self.temp_btn.setText("Temperature")
        self.sali_btn = QRadioButton()
        self.sali_btn.setText("Salinity")
        self.sv_btn = QRadioButton()
        self.sv_btn.setText("SoundVelocity")
        self.btn_grp = QButtonGroup()
        self.btn_grp.addButton(self.temp_btn, 0)
        self.btn_grp.addButton(self.sali_btn, 1)
        self.btn_grp.addButton(self.sv_btn, 2)
        self.sv_btn.setChecked(True)


        # 设置布局
        self.h_layout_1 = QHBoxLayout()
        self.h_layout_1.addWidget(self.temp_btn)
        self.h_layout_1.addWidget(self.sali_btn)
        self.h_layout_1.addWidget(self.sv_btn)
        self.h_layout_1.addStretch()

        self.v_layout_1 = QVBoxLayout()
        self.v_layout_1.addWidget(self.svp_plot)
        self.v_layout_1.addLayout(self.h_layout_1)

        self.h_layout_2 = QHBoxLayout()
        self.h_layout_2.addWidget(self.svp_listView, 1)
        self.h_layout_2.addLayout(self.v_layout_1, 3)


        # 主布局添加到窗体
        self.center_widget = QWidget()
        self.center_widget.setLayout(self.h_layout_2)
        self.setCentralWidget(self.center_widget)


    def on_argoAct_triggered(self):
        self.argoForm.show()


    def receive_data(self, data):
        print(len(data))