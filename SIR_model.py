import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import random
import time
import matplotlib.animation as animation

INFECTION_RATE = 0.3  #Probability that an infected pop passes on the infection to others in its radius
INFECTION_RADIUS = 1.0 #Distance between pops at which infection can spread

def main():

    xCity = 50
    yCity = 50
    pop = 50

    city1 = City(x=50,y=50,population=50)
    city1.Draw()


    
class City:

    def __init__(self,population=50,x=50,y=50,stepTime=0.1,walk_v=2):

        self.colormap = np.array(['DarkGreen','Crimson','DarkGray','Khaki'])

        self.pop = population
        self.s = 0
        self.i = 0
        self.r = 0
        self.popState = SetupPopState(self,pop = self.pop)
        self.popArray = SetupCity(x,y,self.pop)
        self.stepDist = stepTime*walk_v

        self.fig, self.ax = plt.subplots()
        self.sc = self.ax.scatter(self.popArray[0],self.popArray[1], c=self.colormap[self.popState])
        plt.xlim(0,x)
        plt.ylim(0,y)
        self.label = plt.text(0.5,0.5,'S={}, I={}, R={}'.format(self.s,self.i,self.r))

    def Animate(self,i):

        self.Update()
        self.sc.set_color(self.colormap[self.popState])
        self.label.set_text('S={}\nI={}\nR={}'.format(self.s,self.i,self.r))
        self.sc.set_offsets(np.transpose(self.popArray))

    def Draw(self):

        ani = animation.FuncAnimation(self.fig, self.Animate, 
                frames=2, interval=100, repeat=True)
        plt.show()

    def Update(self):

        popCount = len(self.popState)
        # distance is constant at stepDist, now we need to break it into x and y components
        # stepDist**2 = x**2 + y**2
        # set x = rand(-stepDist,stepDist)
        # y = sqrt(stepDist**2 - x**2)

        xStep = (np.random.random(popCount)*2-1) * self.stepDist
        yStep = np.sqrt(self.stepDist**2 - xStep**2)
        yStep = yStep*np.random.choice([-1,1],popCount)

        #TODO: figure out how to bound the pops to the proper area.

        self.popArray[0] = self.popArray[0]+xStep
        self.popArray[1] = self.popArray[1]+yStep

        # calculate the distance between all points
        dist = cdist(np.transpose(self.popArray),np.transpose(self.popArray))

        #Iterate through popState, if pop(N) is infectious, check distance array and infect 
        newlyInfected = list()

        for pop in range(popCount):
            if self.popState[pop] == 1: #infectious
                for neighbor in range(popCount):
                    if dist[pop,neighbor] <= INFECTION_RADIUS:
                        if (self.popState[neighbor]==0) and (random.random() < INFECTION_RATE): #ensure they are susceptible and the infection procs
                            newlyInfected.append(neighbor) #Don't update popState while we're iterating over it

        for z in newlyInfected:
            self.popState[z] = 1
            self.i += 1
            self.s -= 1

        #TODO: figure out how to have sick people get better



def SetupPopState(self, pop=50):

    # Susceptible = 0
    # Infectious = 1
    # Removed = 2
    # Deceased = 3? Might add later

    popState = [0]*pop
    popState[random.randrange(pop)] = 1
    self.i = 1
    self.s = pop-1

    return popState

def SetupCity(x=50, y=50, pop=50):
    
    #create a 2-D array with 2 columns: xFloat, yFloat
    popArrayLoc = np.random.random((2,pop))

    popArrayLoc[0] = popArrayLoc[0,:]*x
    popArrayLoc[1] = popArrayLoc[1,:]*y

    return popArrayLoc





if __name__ == '__main__':
    main()