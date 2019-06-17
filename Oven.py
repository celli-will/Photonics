#
# Author: Marcel Willig
# Date: 10.06.2019
#
# Description: This file defines the classes to simulate
# an oven which can be heated and a PID controller which
# controls a heating current.
#


import numpy as np
import matplotlib.pyplot as plt

#
# An oven is placed in an environment with a certain room temperature.
# The difference between this temp and the ovens temp decides how much
# energy the oven loses (or gains) by convection/conduction.
# A heating current can be change the temperature of the oven.
#

class Oven:

    def __init__(self, rTemp=18):
        self.roomTemp = rTemp
        self.temperature = self.roomTemp
        self.current = 0

    def setCurrent(self, I):
        self.current = I
        return I

    def increaseCurrent(self, deltaI):
        self.current += deltaI
        return self.current

    # After each time step the oven changes it's temperature according to the following function
    def timeStep(self):
        self.temperature += 0.5*self.current-1e-1*(self.temperature-self.roomTemp)**2
        return self.temperature



#
# A controller is controlling it's very own oven. It measures the oven's temperature
# and compares this to a target temperature. The controller changes the oven's heating
# current accordingly. Therefore, the controller has certain P-, I-, and D-coefficients
# The controller also remembers all temperatures
#

class Controller:

    def __init__(self, targetTemp=25):
        self.oven = Oven()
        self.target = targetTemp
        self.P = 0
        self.I = 0
        self.D = 0
        self.data  = np.array([])
        self.data = np.append( self.data, self.oven.timeStep() )

    def setP(self, p):
        self.P = p
        return p

    def setI(self, i):
        self.I = i
        return i

    def setD(self, d):
        self.D = d
        return d

    # After each time step the current of the controller's oven is adjusted.
    def timeStep(self):
        correctionCurrent = self.P * (self.target-self.data[-1])
        correctionCurrent += self.I * (self.target-self.data).sum()
        if self.data.size > 1:
            correctionCurrent += self.D * (self.data[-1]-self.data[-2])
        curr = self.oven.setCurrent( correctionCurrent )
        self.data = np.append( self.data, self.oven.timeStep() )
        return curr

#
# The part below is just for testing and plotting
#
if __name__ == "__main__":
    c = Controller()
    current = [0]
    for i in range(50):
        current.append( c.timeStep() )
    plt.plot(c.data)
    plt.plot(current)
    plt.show()
