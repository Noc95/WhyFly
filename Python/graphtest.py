import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import numpy as np

app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True)
plot = win.addPlot()
curve = plot.plot(pen='y')

data = np.random.randn(1000)

def update():
    global data
    data = np.roll(data, -1)
    data[-1] = np.random.randn()
    curve.setData(data)  # 🔥 Blazing fast update

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)  # Update every 1ms (FAST)

app.exec_()
