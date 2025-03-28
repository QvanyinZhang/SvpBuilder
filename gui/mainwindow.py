
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QListView, QPushButton, QRadioButton, QButtonGroup, \
    QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget
from PyQt6.QtGui import QGuiApplication, QAction, QStandardItemModel, QStandardItem
import pyqtgraph as pg

from .PlotSetting import CustomXAxis, CustomYAxis
from .argoform import Ui_ArgoForm
from Algorithm.SoundVelocityProfile import SoundVelocityProfile

class Ui_MainWindow(QMainWindow):

    svps = []

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

        self.svp_model = QStandardItemModel()
        self.svp_listView.setModel(self.svp_model)

        self.svp_listView.clicked.connect(self.on_svpItem_clicked)


    def on_argoAct_triggered(self):
        self.argoForm.show()


    def receive_data(self, data):
        for ds in data:
            for i in range(ds.sizes['TIME']):
                svp = SoundVelocityProfile()
                svp.fromDatasetAt(ds, i)
                self.svps.append(svp)
                item = QStandardItem(svp.name)
                self.svp_model.appendRow(item)


    def on_svpItem_clicked(self, index):
        svp = self.svps[index.row()]
        self.svp_plot.clear()
        self.svp_plot.plot(svp.pressure, svp.temperature)

    def set_plot_axes(self):
        # 创建 PlotWidget

        plotItem = self.svp_plot.getPlotItem()

        # 移除默认的底部和左侧轴
        plotItem.layout.removeItem(plotItem.getAxis('bottom'))
        plotItem.layout.removeItem(plotItem.getAxis('left'))

        # 创建新的自定义轴：
        # 将原本用于显示 X 数据的轴放在左侧（orientation='left'）
        newXAxis = CustomXAxis(orientation='left')
        # 将原本用于显示 Y 数据的轴放在上方（orientation='top'）
        newYAxis = CustomYAxis(orientation='top')

        # 将自定义轴添加到 PlotItem 的布局中
        # 注意：布局中 row=0 在上，col=0 在左
        plotItem.layout.addItem(newXAxis, 1, 0)  # 新 X 轴放在左侧
        plotItem.layout.addItem(newYAxis, 0, 1)  # 新 Y 轴放在上方

        # 关联视图，使轴能正确响应缩放和平移
        newXAxis.linkToView(plotItem.vb)
        newYAxis.linkToView(plotItem.vb)

        # 隐藏其他多余的轴（右侧和底部）
        plotItem.showAxis('right', show=False)
        plotItem.showAxis('bottom', show=False)