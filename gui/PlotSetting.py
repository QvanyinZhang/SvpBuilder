import sys
import pyqtgraph as pg
from pyqtgraph import PlotWidget, AxisItem
from PyQt6.QtWidgets import QApplication

# 可选：自定义 AxisItem，用于格式化刻度标签
class CustomAxis(AxisItem):
    def tickStrings(self, values, scale, spacing):
        # 格式化 X 轴标签
        return [f"{v:.0f}" for v in values]

class CustomYAxis(AxisItem):
    def tickStrings(self, values, scale, spacing):
        # 格式化 Y 轴标签
        return [f"{v:.2f}" for v in values]
