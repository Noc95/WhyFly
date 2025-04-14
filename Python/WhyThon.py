import socket
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import numpy as np
import threading
import struct
from pyqtgraph.Qt import QtGui, QtCore

# These must match the Pico W's settings
WHYFLY_IP = "192.168.42.1"  # The AP's sacred address
PORT = 80                # The port of the Wi-Fi server

app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True)
plot = win.addPlot()
plot.showGrid(x=True, y=True, alpha=0.5)

# Define key press event
def keyPressEvent(event):
    if event.key() == QtCore.Qt.Key_C:  # Check if 'C' key is pressed
        plot.clear()  # Clear the plot
        # global motor_1 = []
        # motor_2 = []
        # motor_3 = []
        # motor_4 = []
        # print("Window cleared!")

# Assign the custom keyPressEvent to the window
win.keyPressEvent = keyPressEvent

x_curve = plot.plot(pen='r')
y_curve = plot.plot(pen='g')
z_curve = plot.plot(pen='b')

x_filtered_curve = plot.plot(pen='y', label="X Unfiltered")
y_filtered_curve = plot.plot(pen='w')
z_filtered_curve = plot.plot(pen='c')

motor_1_curve = plot.plot(pen=pg.mkPen(color=(255, 165, 0)))  # Orange
motor_2_curve = plot.plot(pen=pg.mkPen(color=(0, 128, 128)))  # Teal
motor_3_curve = plot.plot(pen=pg.mkPen(color=(148, 0, 211)))  # Violet
motor_4_curve = plot.plot(pen=pg.mkPen(color=(50, 205, 50)))  # Lime Green


dataList = []
x_dataList = []
y_dataList = []
z_dataList = []

alpha = 1-0.0625

x_filtered = [0]
y_filtered = [0]
z_filtered = [0]

motor_1 = []
motor_2 = []
motor_3 = []
motor_4 = []

maxDataPoints = 2000 * 10
limit_graph_length = True

data_list_size = []


def fetch_data():
    global dataList
    while True:

        try:
            # Create a TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                
                s.connect((WHYFLY_IP, PORT))
                print(s)
                
                while True:
                    raw_data = s.recv(2048)
                    # print(raw_data.decode())
                    if raw_data:
                        data_cunks = raw_data.split(b'D')
                        for cunk in data_cunks:

                            if len(cunk) == 24:
                                data = struct.unpack('<4i4h', cunk)
                                
                                scaled_data = [v / (2 ** 24) for v in data]

                                # pidx, pidy, filteredx, filteredy (32 bit), motor1, motor2, motor3, motor4 (16bit)

                                x_dataList.append(scaled_data[0])
                                y_dataList.append(scaled_data[1])
                                # z_dataList.append(scaled_data[2])

                                x_filtered.append(scaled_data[2])
                                y_filtered.append(scaled_data[3])
                                # z_filtered.append(scaled_data[4])

                                # x_filtered.append(x_filtered[-1] * alpha + x_dataList[-1] * (1-alpha))
                                # y_filtered.append(y_filtered[-1] * alpha + y_dataList[-1] * (1-alpha))
                                # z_filtered.append(z_filtered[-1] * alpha + z_dataList[-1] * (1-alpha))
                                
                                motor_1.append(data[4])
                                motor_2.append(data[5])
                                motor_3.append(data[6])
                                motor_4.append(data[7])


                        while len(x_dataList) > maxDataPoints and limit_graph_length:
                            try:
                                x_dataList.pop(0)
                                y_dataList.pop(0)
                                # z_dataList.pop(0)

                                x_filtered.pop(0)
                                y_filtered.pop(0)
                                # z_filtered.pop(0)

                                motor_1.pop(0)
                                motor_2.pop(0)
                                motor_3.pop(0)
                                motor_4.pop(0)
                            except:
                                pass
        
        except Exception as e:
            print("Alas! An error hath occurred:", e)

def update_plot():
    """Update the plot with new data"""
    # x_curve.setData(x_dataList)
    # y_curve.setData(y_dataList)
    # z_curve.setData(z_dataList)

    # x_filtered_curve.setData(x_filtered)
    # y_filtered_curve.setData(y_filtered)
    # z_filtered_curve.setData(z_filtered)

    motor_1_curve.setData(motor_1)
    motor_2_curve.setData(motor_2)
    motor_3_curve.setData(motor_3)
    motor_4_curve.setData(motor_4)


if __name__ == "__main__": 

    threading.Thread(target=fetch_data, daemon=True).start()

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update_plot)
    timer.start(1)  # Update every 1ms (FAST)
    
    app.exec_()
    
    



