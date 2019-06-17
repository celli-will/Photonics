#
# Author: Marcel Willig
# Date: 10.06.2019
#
# Description: This program simulates an oven, whose heating
# current is set by a PID controller and plots its temperature.
# The settings of the PID controller can be changed by the user.
#

import sys

from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QSlider, QWidget, QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from Oven import Controller

#
# Define the GUI which the user will see.
#

class PIDdrawer(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PID-Controller Animation'
        self.width = 640
        self.height = 400
        self.c = Controller()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        self.lbl_p = QLabel("P = {0}".format(self.c.P))
        self.lbl_p.setFixedWidth(100)
        sld_p = QSlider(Qt.Horizontal)
        sld_p.valueChanged.connect(self.changeP)
        grid.addWidget( self.lbl_p, 0, 0 )
        grid.addWidget( sld_p, 0, 1 )

        self.lbl_i = QLabel("I = {0}".format(self.c.I))
        sld_i = QSlider(Qt.Horizontal)
        sld_i.valueChanged.connect(self.changeI)
        grid.addWidget( self.lbl_i, 1, 0 )
        grid.addWidget( sld_i, 1 ,1 )

        self.lbl_d = QLabel("D = {0}".format(self.c.D))
        sld_d = QSlider(Qt.Horizontal)
        sld_d.valueChanged.connect(self.changeD)
        grid.addWidget( self.lbl_d, 2, 0 )
        grid.addWidget( sld_d, 2, 1 )

        self.canvas = PlotCanvas(width=5, height=4)
        self.canvas.plot( [self.c.oven.temperature for i in range(2)])

        vButtonBox = QVBoxLayout()
        self.button_start = QPushButton('Start')
        self.button_start.setToolTip('Start/Stop Drawing')
        self.button_start.clicked.connect( self.startStop )
        self.button_start.resize(140,100)
        button_restart = QPushButton('Reset')
        button_restart.setToolTip('Stop and Reset Drawing')
        button_restart.clicked.connect( self.restart )
        button_restart.resize(140,100)
        vButtonBox.addWidget(self.button_start)
        vButtonBox.addWidget(button_restart)

        hbox_canvas = QHBoxLayout()
        hbox_canvas.addWidget( self.canvas )
        hbox_canvas.addLayout( vButtonBox )

        vbox = QVBoxLayout()
        vbox.addLayout( grid )
        vbox.addLayout( hbox_canvas )

        self.setLayout(vbox)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.timer = QBasicTimer()

        self.show()

    def changeP(self, p):
        p /= 50
        self.lbl_p.setText("P = {0}".format(p))
        self.c.setP(p)

    def changeI(self, i):
        i /= 1000
        self.lbl_i.setText("I = {0}".format(i))
        self.c.setI(i)

    def changeD(self, d):
        d /= 1000
        self.lbl_d.setText("D = {0}".format(d))
        self.c.setD(d)

    def startStop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button_start.setText('Continue')
        else:
            self.timer.start(100, self)
            self.button_start.setText('Stop')

    def restart(self):
        self.timer.stop()
        self.button_start.setText('Start')
        p = self.c.P
        i = self.c.I
        d = self.c.D
        self.c = Controller()
        self.c.setP(p)
        self.c.setI(i)
        self.c.setD(d)
        self.canvas.plot( [self.c.oven.temperature for i in range(2)])

    def timerEvent(self, e):
        self.c.timeStep()
        self.canvas.plot( self.c.data )



#
# A canvas widget which will be redrawn after each time step to animate the temperature change.
#

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        self.axes.clear()
        self.axes.set_title("Temperature over Time")
        self.axes.set_xlabel("Time (A.U.)")
        self.axes.set_ylabel("Temperature (°C)")
        self.axes.plot( data )
        self.axes.plot([0,len(data)-1],[25,25])
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PIDdrawer()
    sys.exit(app.exec_())
