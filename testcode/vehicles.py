from random import randint
import time

#creating a Class for cars
class Car:
    # initliazing empty array
    tracks=[]
    #constructor for class Car
    def __init__(self,i,xi,yi,max_age):
        self.i=i
        self.x=xi
        self.y=yi
        self.tracks=[]
        # random colors
        self.R=randint(0,255)
        self.G=randint(0,255)
        self.B=randint(0,255)
        self.done=False
        self.state='0'
        self.age=0
        self.max_age=max_age
        # for direction of the car
        #initliazing to none
        self.dir=None

    #for the RGB color
    def getRGB(self):
        return (self.R,self.G,self.B)

    def getTracks(self):
        return self.tracks

    def getId(self): #For the ID
        return self.i

    def getState(self):
        return self.state

    def getDir(self): # for direction of the car
        return self.dir

    def getX(self):  #for x coordinate
        return self.x

    def getY(self):  #for y coordinate
        return self.y

        #adding all the centroids to the list tracks for tracking system in main.py
    def updateCoords(self, xn, yn):
        self.age = 0
        #appending to the list tracks
        self.tracks.append([self.x, self.y])
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    def going_UP(self, line_down, line_up):
        #if list track has more than 2 elements i.e. more than 2 coordinates
        #implies that car is not stationary
        if len(self.tracks)>=2:
            if self.state=='0':
                #comparing the last two y coordinate to detect if vechile is moving up or down
                #tracks[sefl.x][self.y]
                if self.tracks[-1][1]<line_up and self.tracks[-2][1]>=line_up:
                    state='1'
                    #vehicle is moving in direction up
                    self.dir='up'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def going_DOWN(self,line_down,line_up):
        #if list track hsa more than 2 elements i.e. more than 2 coordinates
        #implies that car is not stationary
        if len(self.tracks)>=2:
            if self.state=='0':
                #comparing the last to y coordinate to detect if vechile is moving  down or up
                #tracks[sefl.x][self.y]
                if self.tracks[-1][1]>line_down and self.tracks[-2][1]<=line_down:
                    start='1'
                    #vehicle is moving in direction down
                    self.dir='down'
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def age_one(self):
        self.age+=1
        if self.age>self.max_age:
            self.done=True
        return  True

#Class2 for multiple cars object

class MultiCar:
    def __init__(self,cars,xi,yi):
        self.cars=cars
        self.x=xi
        self.y=yi
        self.tracks=[]
        self.R=randint(0,255)
        self.G=randint(0,255)
        self.B=randint(0,255)
        self.done=False
