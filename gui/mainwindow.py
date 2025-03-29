
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QListView, QPushButton, QRadioButton, QButtonGroup, \
    QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget
from PyQt6.QtGui import QGuiApplication, QAction, QStandardItemModel, QStandardItem
import pyqtgraph as pg
# from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .PlotSetting import CustomYAxis, CustomAxis
from .argoform import Ui_ArgoForm
from Algorithm.SoundVelocityProfile import SoundVelocityProfile

class Ui_MainWindow(QMainWindow):

    svps = []
    cur_index = -1

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
        self.svp_plot = pg.PlotWidget(axisItems={'top': CustomAxis(orientation='top'),
                                                 'left': CustomAxis(orientation='left')})
        self.set_plot_axes()
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

        # 地图显示
        self.webview = QWebEngineView()

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
        self.h_layout_2.addWidget(self.webview, 3)
        self.h_layout_2.addLayout(self.v_layout_1, 1)


        # 主布局添加到窗体
        self.center_widget = QWidget()
        self.center_widget.setLayout(self.h_layout_2)
        self.setCentralWidget(self.center_widget)

        self.svp_model = QStandardItemModel()
        self.svp_listView.setModel(self.svp_model)

        self.svp_listView.clicked.connect(self.on_svpItem_clicked)
        self.btn_grp.buttonClicked.connect(self.on_radioBtn_clicked)


    def on_argoAct_triggered(self):
        self.argoForm.show()


    def receive_data(self, data):
        for ds in data:
            for i in range(ds.sizes['TIME']):
                svp = SoundVelocityProfile()
                svp.fromDatasetAt(ds, i)
                svp.preprocess()
                self.svps.append(svp)
                item = QStandardItem(svp.name)
                self.svp_model.appendRow(item)


    def on_svpItem_clicked(self, index):
        self.cur_index = index.row()
        svp = self.svps[self.cur_index]
        self.svp_plot.clear()
        self.svp_plot.plot(svp.speed, -1.0*svp.pressure)

    def set_plot_axes(self):
        # 创建 PlotWidget
        plotItem = self.svp_plot.getPlotItem()
        plotItem.showAxis('top')
        plotItem.showAxis('left')
        plotItem.hideAxis('bottom')

        plotItem.setLabel('top', '声速', units='m/s')
        plotItem.setLabel('left', '水深', units='m')

        plotItem.getAxis('top').enableAutoSIPrefix(False)
        plotItem.getAxis('left').enableAutoSIPrefix(False)

    def on_radioBtn_clicked(self, button):
        self.svp_plot.clear()
        if self.cur_index < 0:
            return
        v_axis_data = -1.0*self.svps[self.cur_index].pressure
        match self.btn_grp.id(button):
            case 0:
                self.svp_plot.getPlotItem().setLabel('top', '温度', units='°C')
                h_axis_data = self.svps[self.cur_index].temperature
            case 1:
                self.svp_plot.getPlotItem().setLabel('top', '盐度', units='‰')
                h_axis_data = self.svps[self.cur_index].salinity
            case 2:
                self.svp_plot.getPlotItem().setLabel('top', '声速', units='m/s')
                h_axis_data = self.svps[self.cur_index].speed
            case _:
                self.svp_plot.getPlotItem().setLabel('top', '声速', units='m/s')
                h_axis_data = self.svps[self.cur_index].speed

        self.svp_plot.plot(h_axis_data,v_axis_data)