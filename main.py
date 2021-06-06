import os, sys
import numpy as np


def check_for_emv(vehicleIDList):
    for vehicleID in vehicleIDList:
        if vehicleID.startswith('emergency-route'):
            return vehicleID
    return 0


def calculate_waiting_time():
    totalWaitingTime = 0
    for eachLane in laneIDs:
        totalWaitingTime += traci.lane.getWaitingTime(eachLane)
    return totalWaitingTime


# check if sumo home is defined
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "4-junction.sumocfg", "--start"]

import traci

traci.start(sumoCmd)

step = 0

waiting_time_G2H1 = 0
waiting_time_D1B2 = 0

lanes_in_G2H1 = ['F2_0', 'F2_1', 'G2_0', 'G2_1', 'H1_0', 'H1_1', 'I1_0', 'I1_1']
lanes_in_D1B2 = ['A2_0', 'A2_1', 'B2_0', 'B2_1', 'D1_0', 'D1_1', 'E1_0', 'E1_1']

accumulated_waiting_time =[]

totalWaitingTime = 0
vehicleWaitingTime = 0
emergencyVehicleWaitingTime = 0


trafficLightID = traci.trafficlight.getIDList()
print('trafficLightID')
print(trafficLightID)
laneIDs = traci.lane.getIDList()
laneCount = traci.lane.getIDCount
routeIDs = traci.route.getIDList()

print('laneIDs')
print(laneIDs)


vehicleIDList = []
# while step < 16000:
while step < 1500:
    # vehicleIDList = traci.vehicle.getIDList()
    # emv = check_for_emv(vehicleIDList);

    # run traffic ight code after five steps ( to optimize speed)
    # TODO get current lane the traffic light is passing

    if step % 5 == 0:

        vehicleIDList = traci.vehicle.getIDList()
        for each_vehicle in vehicleIDList:
            vehicle_lane = traci.vehicle.getLaneID(each_vehicle)
            # if vehicle is in the stopped lane
            if vehicle_lane in lanes_in_G2H1 or vehicle_lane in lanes_in_D1B2:
                vehicle_accumulated_waiting_time = traci.vehicle.getAccumulatedWaitingTime(each_vehicle)
                if vehicle_accumulated_waiting_time > 0:
                    accumulated_waiting_time.append(vehicle_accumulated_waiting_time)
                    print('Accumulated waiting time => ' + str(vehicle_accumulated_waiting_time))




    # if emv != 0:
    #    print('!!!WARNING EMV ON THE ROAD OVER' + emv)
    # lightColor = traci.trafficlight.getRedYellowGreenState(trafficLightID[0]);
    # print('lightColor type')
    # print(lightColor)

    # laneWaitingTime = traci.lane.getWaitingTime("H1_0")
    # print('totalWaitingTime => ' + str(totalWaitingTime))
    traci.simulationStep()
    step += 1


print('Accumulated waiting time ')
print(accumulated_waiting_time)
print('\n\n\n\n')
print(np.sort(accumulated_waiting_time))
# print('laneCount')
# print(laneCount)
# print('totalWaitingTime')
# print(totalWaitingTime)
# print("vehicleIDList")
# print(vehicleIDList)
traci.close()

