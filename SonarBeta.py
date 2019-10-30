
###################################
# Name: Kenneth Duncan
# Date: 5/23/19
# Description: Ultrasonic sort
###################################


#import RPi.GPIO as GPIO
from time import sleep, time
from Tkinter import *
import math

#constants
DEBUG = False               # debug mode?
SETTLE_TIME = 2             # seconds to let the sensor settle
CALIBRATIONS = 5            # number of calibration measurements to take
CALIBRATION_DELAY = 1       # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001      # seconds needed to trigger the sensor (to get a measurement)
SPEED_OF_SOUND = 343        # speed of sound in m/s
ROTATION_ANGLE = 15

'''#list

numbers = []
'''

'''#set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)

#GPIO pins
TRIG = 18      # the sensor's TRIG pin
ECHO = 27      # the sensor's ECHO pin

GPIO.setup(TRIG, GPIO.OUT)      # TRIG is an output
GPIO.setup(ECHO, GPIO.IN)       # ECHO is an input
'''
# calibrates the sensor
# tehnically, it returns a correction factor to use in our calculations

#additional variablees
rotation_counter = 0
angle = ROTATION_ANGLE * rotation_counter

class Point(object):
    #constructor
    def __init__(self, distance, angle):
        self.xcoord = distance * (math.cos(math.radians(angle)))
        self.ycoord = distance * (math.sin(math.radians(angle)))
    
    #mutator for x-coordinate
    @property
    def xcoord(self):
        return self._xcoord
    
    #setter for x-coordinate    
    @xcoord.setter
    def xcoord(self, xcoord):
        self._xcoord = xcoord
    
    #mutator for y-coordinate
    @property
    def ycoord(self):
        return self._ycoord
    
    #setter for y-coordinate
    @ycoord.setter
    def ycoord(self, ycoord):
        self._ycoord = ycoord

    #magic print function
    def __str__(self):
        return "({},{})".format(float(self.xcoord), float(self.ycoord))

# the canvas class
class CoordinateSystem(Canvas):
  ptRadius = 1
  ptColor = "black"
  
  def __init__(self, window):
    Canvas.__init__(self, window, bg="white")
    self.pack(fill = Y, expand = 1)

  def plotPoints(self, points):
    for i in range(len(points)):
      self.plotPoint(points[i])

  def plotPoint(self, pt):
    self.create_oval(pt.x, pt.y, pt.x + \
                     CoordinateSystem.ptRadius * 2, \
                     pt.y + CoordinateSystem.ptRadius * 2, \
                     fill=CoordinateSystem.ptColor, \
                     outline = CoordinateSystem.ptColor)
  
class Sensor(Frame):
  # the layout
  # O O O C
  # O O O S
  # O O O Q
  
  # the constructor
  def __init__(self, parent):
    # call the constructor in the superclass
    Frame.__init__(self, parent, bg="white")
    self.setupGUI()

  # sets up the GUI
  def setupGUI(self):
    # organize the GUI
    self.display = Label(self, text="", anchor=E,\
                         bg="white", height=2, font=("", 50))
    self.display.grid(row=0, column=0, columnspan=4, sticky=E+W+N+S)

    for row in range(1):
      Grid.rowconfigure(self, row, weight=1)
    for col in range(3):
      Grid.columnconfigure(self, col, weight=1)

    # calibrate
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Calibrate")
    button.grid(row=0, column=0, sticky=N+S+E+W)

    # start
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Start")
    button.grid(row=0, column=1, sticky=N+S+E+W)

    # stop
    button = Button(self, bg="white", \
                    borderwidth=0, highlightthickness=0,\
                    activebackground="white", text="Stop")
    button.grid(row=0, column=2, sticky=N+S+E+W)

    self.pack(fill=BOTH, expand=1)

    #sonar = CoordinateSystem(window)
    
    
    '''
    # setup input on the right side of the screen
    Sensor.player_input = Entry(self, bg="white")
    Sensor.player_input.bind("<Return>", self.process)
    Sensor.player_input.pack(side=RIGHT, expand=True, fill=BOTH)
    Sensor.player_input.focus()

    # setup the display on the left of the GUI
    sonar = CoordinateSystem(window)
    Sensor.sonar = Label(self, width=WIDTH / 2)
    Sensor.sonar.sonar = sonar
    Sensor.sonar.pack(side=LEFT, fill=Y)
    Sensor.sonar.pack_propagate(False)

    # setup buttons on the right side
    '''
    
  # process the input
  def process(self, event):
    pass


'''def calibrate():
    print "Calibrating..."
    # prompt the user for an object's known distance
    print "-Place the sensor a measured distance away from an object."
    known_distance = input("-What is the measured distance (cm)?")

    # measure the distance to the object with the sensor
    # do this seeral times and get an average
    print "-Getting calibration measurements..."
    distance_avg = 0

    for i in range(CALIBRATIONS) :
        distance= getDistance()
        if (DEBUG):
            print "--Got {}cm".format(distance)
        #  keep a running sum
        distance_avg += distance
        # delay a short time before using the sensor again
        sleep(CALIBRATION_DELAY)
    # calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print "--Average is {}cm".format(distance_avg)

    #calculate the correction factor
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print "--Correction factor is {}".format(correction_factor)
    print "Done"
    print

    return correction_factor

# uses the sensor to calculate the distance to an object
def getDistance():
    # trigger the sensor by seting it high for a short time and then setting it low
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)

    # wait for the echo pin to read high
    # once the ECHO pin is high, the start time is set
    # once the ECHO pin is low again, the end time is set
    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
        end = time()

    # calcuate the duration that the ECHO pin was high
    # this is how long the pulse took to get from the sensor to the object -- and back again

    duration = end - start
    # calculate the total distance that the pulse traveled by factoring in the speed of sound (m/s)
    distance = duration * SPEED_OF_SOUND
    # the distance from the sensor is half of the total distance traveled
    distance /= 2
    # convert from meters to centimeters
    distance *= 100

    return distance
'''
'''def sort():

    if (len(numbers) == 0):
        return

    else:
    
        n = len(numbers)

        for i in  range(0, n-1):
            minPosition = i

            for j in range(i + 1, n):
                if (numbers[j] < numbers[minPosition]):
                    minPosition = j

            temp = numbers[i]
            numbers[i] = numbers[minPosition]
            numbers[minPosition] = temp'''
    

########
# MAIN #
########

'''# first, allow the sensor to settle for the bit

print "Waiting for sensor to settle ({}s)...".format(SETTLE_TIME)
GPIO.output(TRIG, GPIO.LOW)
sleep(SETTLE_TIME)

# next, calibrate the sensor

correction_factor = calibrate()

# then, measure
raw_input("Press enter to begin...")
print "Getting measurements:"
while (True):
    # get the distance to an object and correct it with the correction factor
    print "-Measuring..."
    distance = getDistance() * correction_factor
    sleep(1)

    # and round to our decimal places
    distance = round(distance, 4)

    # append distane to the end of the list
    numbers.append(distance)

    # display the distances in an unsorted list
    print "--Unsorted distances measured(in cm): {}".format(numbers)

    # sort the list
    sort()

    # display the distances in a sorted list
    print "--Sorted distances measured(in cm): {}".format(numbers)

    #prompt for another measurement
    i = raw_input("--Get another measurement (Y/n)? ")
    # stop measuring if desired
    if (not i in ["y", "Y", "yes", "Yes", "YES", ""]):
        break


# finally, cleanup the GPIO pins
print "Done."
GPIO.cleanup()

'''

####################################
# setup GUI
####################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Sonar Sonic Sensor")

# creat the GUI as a Tkinter canvas inside the window
s = Sensor(window)
c = CoordinateSystem(window)

####################################
# rotate the sonar sensor and take distance measurements
####################################
#spin()
distances = [ 5, 6, 7, 8, 9, 10, 11, 12 ]
angles = [2, 4, 6, 8, 10, 12, 14, 16]
points = []

####################################
# calculate 2D points with distances
####################################

for i in range(len(distances)):# example list
    points.append(Point(distances[i], angles[i]))

####################################
# plot 2D points to GUI
####################################
  # pass in a list of points

c.plotsPoints(points)

# wait for the window to close
window.mainloop()


# NOTES
# We should just worry about text in the GUI for now
# We can add buttons to start and stop later















