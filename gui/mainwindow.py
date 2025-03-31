import io

import folium
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QListView, QPushButton, QRadioButton, QButtonGroup, \
    QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget
from PyQt6.QtGui import QGuiApplication, QAction, QStandardItemModel, QStandardItem
import pyqtgraph as pg
# from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .PlotSetting import CustomYAxis, CustomAxis
from .argoform import Ui_ArgoForm
from Algorithm.SoundVelocityProfile import SoundVelocityProfile
import pyqtgraph.opengl as gl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Ui_MainWindow(QMainWindow):

    svps = []
    cur_index = -1
    cmap = pg.colormap.get("jet", source="matplotlib", skipCache=True)

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
        # 折线绘制
        self.svp_listView = QListView()
        self.svp_plot = pg.PlotWidget(axisItems={'top': CustomAxis(orientation='top'),
                                                 'left': CustomAxis(orientation='left')})
        self.set_plot_axes()

        # 数据选择
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
        self.show_map()

        # 三维显示
        self.gl_view = gl.GLViewWidget()
        self.gl_view.opts['distance'] = 4
        self.colorbar = pg.ColorBarItem(values=(0, 1), colorMap=self.cmap)
        self.colorbar_widget = pg.GraphicsLayoutWidget()
        self.colorbar_widget.addItem(self.colorbar)

        # 设置布局
        self.h_layout_1 = QHBoxLayout()
        self.h_layout_1.addWidget(self.temp_btn)
        self.h_layout_1.addWidget(self.sali_btn)
        self.h_layout_1.addWidget(self.sv_btn)
        self.h_layout_1.addStretch()

        self.v_layout_1 = QVBoxLayout()
        self.v_layout_1.addWidget(self.svp_plot)
        self.v_layout_1.addLayout(self.h_layout_1)

        self.h_layout_3 = QHBoxLayout()
        self.h_layout_3.addWidget(self.gl_view, 8)
        self.h_layout_3.addWidget(self.colorbar_widget, 1)

        self.v_layout_2 = QVBoxLayout()
        self.v_layout_2.addWidget(self.webview,1)
        self.v_layout_2.addLayout(self.h_layout_3,1)

        self.h_layout_2 = QHBoxLayout()
        self.h_layout_2.addWidget(self.svp_listView, 1)
        self.h_layout_2.addLayout(self.v_layout_2, 3)
        self.h_layout_2.addLayout(self.v_layout_1, 2)


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

    # ArgoForm导入后触发
    def receive_data(self, data):
        for ds in data:
            for i in range(ds.sizes['TIME']):
                svp = SoundVelocityProfile()
                svp.fromDatasetAt(ds, i)
                svp.preprocess()
                self.svps.append(svp)
                item = QStandardItem(svp.name)
                self.svp_model.appendRow(item)

        self.show_map()
        self.show_3d_pnt()


    def on_svpItem_clicked(self, index):
        self.cur_index = index.row()
        svp = self.svps[self.cur_index]
        self.svp_plot.clear()
        self.svp_plot.plot(svp.speed, -1.0*svp.pressure)

    # 设置声速曲线的坐标轴
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

    # 测区范围
    def survey_area(self):
        num_svp = len(self.svps)
        if num_svp == 0:
            return 0.0, 0.0, 0.0, 0.0
        lat = np.zeros(0)
        lon = np.zeros(0)
        for svp in self.svps:
            lat = np.append(lat, svp.latitude)
            lon = np.append(lon, svp.longitude)
        return np.min(lat), np.max(lat), np.min(lon), np.max(lon)

    # 显示地图
    def show_map(self):

        # 视角移到测区中心
        lat_min, lat_max, lon_min, lon_max = self.survey_area()
        center_lat = (lat_min + lat_max)/2.0
        center_lon = (lon_min + lon_max)/2.0
        m = folium.Map(location=[center_lat, center_lon], zoom_start=4)
        for svp in self.svps:
            folium.Marker(
                location=[svp.latitude, svp.longitude],
                popup=svp.name
            ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webview.setHtml(data.getvalue().decode())

    def show_3d_pnt(self):
        # 清空原有数据，self.gl_view.items()[:]复制原有列表，防止遍历过程中修改列表
        for item in self.gl_view.items[:]:
            self.gl_view.removeItem(item)

        pnts = np.empty(0)
        vals = np.empty(0)
        # 统计所有声速采样点的三维坐标
        for svp in self.svps:
            v = svp.speed[svp.speed_qc]
            if v.size == 0:
                continue
            z = -svp.depth[svp.speed_qc]

            x = np.full(v.shape, svp.east)
            y = np.full(v.shape, svp.north)

            p = np.c_[x,y,z]
            if pnts.size == 0:
                pnts = p
                vals = v
            else:
                pnts = np.vstack((pnts, p))
                vals = np.concatenate((vals, v))

        # 坐标归一化
        x_min, y_min, z_min = np.min(pnts, axis=0)
        x_max, y_max, z_max = np.max(pnts, axis=0)

        l_max = np.max([x_max-x_min, y_max-y_min, 1])
        d_max = z_max-z_min
        x_o = (x_max+x_min)/2
        y_o = (y_max+y_min)/2
        z_o = (z_max+z_min)/2

        pnts[:,0] = (pnts[:,0]-x_o)/l_max
        pnts[:,1] = (pnts[:,1]-y_o)/l_max
        pnts[:,2] = (pnts[:,2]-z_o)/d_max

        # 设置颜色
        v_min = vals.min()
        v_max = vals.max()
        v_mid = (v_min+v_max)/2
        norm = mcolors.Normalize(vmin=v_min, vmax=v_max)

        # ticks = [(v_min, f"{v_min:.2f}"), (v_mid, f"{v_mid:.2f}"), (v_max, f"{v_max:.2f}")]
        self.colorbar_widget.removeItem(self.colorbar)
        self.colorbar = pg.ColorBarItem(values=(v_min, v_max), colorMap=self.cmap)
        self.colorbar_widget.addItem(self.colorbar)
        colors = self.cmap.map(norm(vals),mode='float')
        # cmap = plt.cm.viridis
        # colors = cmap(norm(vals))

        # 显示
        svp_item = gl.GLScatterPlotItem(pos=pnts, color=colors, size=2)
        self.gl_view.addItem(svp_item)
