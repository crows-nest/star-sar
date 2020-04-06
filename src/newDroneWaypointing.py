#                Nolan Ferguson
#       Drone Waypointing and Searching
##################################################

# Script initializations
import airsim
import threading
import numpy as np
import json
import threading
import pprint


class Drone:
    numDrone = 0 #How many instances

    def __init__(self, name, wpFile): #Self, Name of Drone, Way Pointing file name 
        self.name = name
        self.wpFile = wpFile
        Drone.numDrone += 1  

def initializeDrones(droneName,client):
    droneName = "Drone1"
    f11 = client.takeoffAsync(vehicle_name= droneName)
    f11.join()

    f12 = client.hoverAsync(vehicle_name= droneName)
    f12.join()

def moveExecute(droneName, droneFile, client): # Drone Name, Drone waypoint file # Here we create a loop to move our Drones. We can multi thread with this.
   
    with open(droneFile, 'r') as rf:
        distros_dict = json.load(rf)

    for distro in distros_dict:
       f1 = client.moveToPositionAsync(int(distro['x']), int(distro['y']), int(distro['z']), (distro['velocity'])) # movetoPos(self, x, y, z, velocity,)
       #print("stuck")
       f1.join()

    rf.close()

# We can have multiple drones initiated using a drone class, but note  the settings.json will have to be modified if this is the case. See below:
"""
{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
	"SettingsVersion": 1.2,
	"SimMode": "Multirotor",
	"ClockSpeed": 1,
	
	"Vehicles": {
		"Drone1": {
		  "VehicleType": "SimpleFlight",
		  "X": 4, "Y": 0, "Z": -2
		},
		"Drone2": {
		  "VehicleType": "SimpleFlight",
		  "X": 8, "Y": 0, "Z": -2
		}
    }
}

"""

# Client/Engine Initializations
client = airsim.MultirotorClient()
client.confirmConnection()

# Drone Initializations 
dr1 = Drone("Drone1",'C:\\Users\\Nolan\\Documents\\AirSim\\TestClap.json' )
client.enableApiControl(True, dr1.name)
client.armDisarm(True, dr1.name)

# Drone Executions
airsim.wait_key('Press any key to initialize takeoffs')
t1 = threading.Thread(target= initializeDrones, args=(dr1.name, client)) # New thread to execute the take of Drone 1.
t1.start()
t1.join() # Wait until the drone is fully initialzed and thread is complete

# Thread initialization
airsim.wait_key('Press any key to move vehicles')
t2 = threading.Thread(target= moveExecute, args=(dr1.name, dr1.wpFile, client)) # New thread to execute the move-to-positions of the Drone 1 
t2.start()

# Pull state while executing example...
kickOut = 1
while kickOut != 0:
    chekDesire = input("Get state 1, else leave loop 0")

    if chekDesire == 1:
        state1 = client.getMultirotorState(vehicle_name="Drone1")
        s = state1.kinematics_estimated.position
        print("state: %s" % s)
    else:
        break