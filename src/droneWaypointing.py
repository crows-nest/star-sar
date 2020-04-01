# Nolan Ferguson
# Drone Waypointing and Searching
# Lets make Jeff proud!
print('Begin!')
## Initializations
import airsim
#import time
#import string
#import msgpackrpc
import numpy as np
import json # Initialize the ability to use and get JSONs
       # Some basic commands:  .dump, serializes (byte-ifies data) to a "fp", a writable file format

#import JSONArray # We either call a large JSON array here, or we pull that information individually from elsewhere
with open('C:\\Users\\Nolan\\Documents\\AirSim\\TestClap.json', 'r') as rf:
    distros_dict = json.load(rf)

# Drone Initialization (Subject to change depending on number of drones) (see https://github.com/microsoft/AirSim/blob/master/PythonClient/multirotor/multi_agent_drone.py)

    # connect to the AirSim simulator 
client = airsim.MultirotorClient()# Multirotorclient is literally C:\Users\Nolan\Desktop\AirSim-master\PythonClient\airsim\client.py
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)# Unsure of the purpose of this line
      #Here, in we change the initial location or spawn of the drone

client.takeoffAsync().join() # Drone take off 
airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')

client.hoverAsync().join()
airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')

 #End of Drone Initialization

print("Take Off initialized!")
# Basic Waypointing Loop (Initial thought, we either assign new directions to go in here, or the JSON is configured in order with those locations)
    #Keep in mind, applicability to real drones will Require Drone Shell and Drone server (https://microsoft.github.io/AirSim/docs/custom_drone/#droneserver-and-droneshell)
for distro in distros_dict:
    client.moveToPositionAsync(int(distro['x']), int(distro['y']), int(distro['z']), (distro['velocity'])).join # movetoPos(self, x, y, z, velocity,)
    client.hoverAsync().join() #This may excute our que'd or apparently unconducted asyncs.
    state = client.getMultirotorState() 
    # print(state)
    # print(, type(state))
    # print("Nolan Here! ", int(state.kinematics_estimated.position.x_val) #dict keys: 'collision', 'kinematics_estimated', 'gps_location', 'timestamp', 'landed_state', 'rc_data
    # tupTups = parse(state)
    # print("state: %s" % pprint.pformat(state))
    # print()
    # print(tupTups)

    current_pos_norm = np.array([int(state.kinematics_estimated.position.x_val), int(state.kinematics_estimated.position.y_val), int(state.kinematics_estimated.position.z_val)])
    desired_pos_norm = np.array([int(distro['x']), int(distro['y']), int(distro['z'])])
    # print(current_pos_norm-desired_pos_norm)
    diff = np.absolute(current_pos_norm-desired_pos_norm)
    print(diff[0])

    while diff[0] > .001 and diff[1] > .001 and diff[2] > .001: # while loop will hold us in our "move to position" until command until executed
        state = client.getMultirotorState() # Error position check (are we where we expect to be)
        current_pos_norm = [int(state.kinematics_estimated.position.x_val), int(state.kinematics_estimated.position.y_val), int(state.kinematics_estimated.position.z_val)]
        print("HIL")

    print("Iterated")
# End Basic Waypointing Loop



import collections #for circulat buffer
import threading

#TODO multi drone capability https://github.com/microsoft/AirSim/blob/master/PythonClient/multirotor/multi_agent_drone.py
#TODO thread the pose function https://realpython.com/intro-to-python-threading/

class drone_controller(object):

    def __init__(self, drone_name="drone_1", buffer_length=10):
        #TODO initialize the API and control
        self.pose_buff = collections.deque(maxlen=10)
        pass

    def load_waypoints(self, filename):
        waypoint_list = []
        return waypoint_list
    
    def execute_waypoints(self, waypoint_list):
        pass
    
    def start_callback(self):
        pass

    def stop_callback(self):
        pass

    def _pose_callback(self, freq):
        #TODO create thread for drone pose callback
        #TODO record into circular buffer? pose + timestamp?
        pass

