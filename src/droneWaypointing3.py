#              CROWSAR                  #
#           Nolan Ferguson              #
# Drone Waypointing and Searching rev 3 #
#########################################

# Script initializations
print('Begin!')
import airsim
import threading
import numpy as np
import json
import collections #for circulat buffer
import threading
import pprint

# Class, object, function initialization

class drone_controller(object): 

    def __init__(self, drone_name, client, buffer_length=10):
        self.pose_buff = collections.deque(maxlen=10)
        self.drone_name = drone_name
        client.enableApiControl(True, drone_name)
        client.armDisarm(True, drone_name)

    def load_waypoints(self, filename): #Self call or usage as input, assuming it is name of Drone. Note, drone call must be changed in settings JSON file for AIRSIM. 
       
        with open(filename, 'r') as rf:
          waypoint_list = json.load(rf) #waypoint_list = []
        rf.close()
        return waypoint_list
    
    def execute_waypoints(self, waypoint_list, client):
        f11 = client.takeoffAsync(vehicle_name= self.drone_name)
        f11.join()
        f12 = client.hoverAsync(vehicle_name= self.drone_name)
        f12.join()

        for distro in waypoint_list:
            f1 = client.moveToPositionAsync(int(distro['x']), int(distro['y']), int(distro['z']), (distro['velocity'])).join() # movetoPos(self, x, y, z, velocity,)
            print("Executing move to Position")
            f1.join()
    
    def start_callback(self):
        pass

    def stop_callback(self):
        pass

    def _pose_callback(self, freq):
        #TODO create thread for drone pose callback
        #TODO record into circular buffer? pose + timestamp?
        pass

# Client/Engine Initializations
client = airsim.MultirotorClient()
client.confirmConnection()

# Initialize Drone Objects (Must be initiated after Client/Engine in this configuration)
dObj1 = drone_controller( "Drone1", client, 10)
wayPointObj1 = dObj1.load_waypoints('C:\\Users\\Nolan\\Documents\\AirSim\\TestClap.json')

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
# Drone Executions
airsim.wait_key('Press any key to initialize takeoffs')
t1 = threading.Thread(target= dObj1.execute_waypoints, args=(wayPointObj1, client)) # New thread to execute the take of Drone 1.
t1.start()
t1.join() # Wait until the drone is fully initialzed and thread is complete

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