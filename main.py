import os, sys
from fuzzy_traffic_controller import fuzzy_controller_function
from helper import *


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


lanes_in_G2H1 = ['F2_0', 'F2_1', 'G2_0', 'G2_1', 'H1_0', 'H1_1', 'I1_0', 'I1_1']
lanes_in_D1B2 = ['A2_0', 'A2_1', 'B2_0', 'B2_1', 'D1_0', 'D1_1', 'E1_0', 'E1_1']

total_vehicle_waiting_time = 0
emv_waiting_time = 0

trafficLightID = traci.trafficlight.getIDList()[0]

GREEN_TIME = 60
NS_GREEN_STATE = "GGGgrrrrGGGgrrrr"
NS_YELLOW_STATE = "YYYyrrrrYYYyrrrr"
WE_GREEN_STATE = "rrrrGGGgrrrrGGGg"
WE_YELLOW_STATE = "rrrrYYYyrrrrYYYy"

step = 0
while step < 16000:
    # The get current lane the traffic light is passing
    lanes_currently_moving, lanes_stopped_by_light = get_lane_lists(lanes_in_D1B2, lanes_in_G2H1, trafficLightID)

    # Get cars in both lanes lane
    vehicles_in_red_lanes = get_vehicles_in_lane(lanes_stopped_by_light)
    vehicles_in_green_lanes = get_vehicles_in_lane(lanes_currently_moving)

    # Get no of cars in both lane
    no_vehicles_in_red_lanes = len(vehicles_in_red_lanes)
    no_vehicles_in_green_lanes = len(vehicles_in_green_lanes)

    # Get waiting time of cars in red-light lane
    vehicles_waiting_time = vehicle_waiting_time_in_lane(vehicles_in_red_lanes)
    if vehicles_waiting_time != 0:
        vehicles_waiting_time.sort()
        max_waiting_time_in_red_lanes = vehicles_waiting_time[-1]
        total_vehicle_waiting_time += sum(vehicles_waiting_time)

    # waiting time of emergency vehicles in red light
    emv_waiting_time += get_emv_waiting_time(vehicles_in_red_lanes)

    print("sum_of_vehicle_waiting_time")
    print(total_vehicle_waiting_time)
    print("emv_waiting_time")
    print(emv_waiting_time)

    # Get emergency vehicles count
    emv_current_lane = get_emv(vehicles_in_green_lanes)
    emv_other_lane = get_emv(vehicles_in_red_lanes)

    no_emv_current_lane = len(emv_current_lane)
    no_emv_other_lane = len(emv_other_lane)


    # run traffic light controller code after every five steps ( to optimize speed)
    if (step > 0) and (step % 7) == 0:
        print('nov red lane' + str(no_vehicles_in_red_lanes))
        print('nov green lane' + str(no_vehicles_in_green_lanes))
        print('waiting time red lane' + str(max_waiting_time_in_red_lanes))
        print('emv red lane' + str(no_emv_other_lane))
        print('emv green lane'+ str(no_emv_current_lane))

        traffic_command = fuzzy_controller_function(no_vehicles_in_red_lanes,
                                                    no_vehicles_in_green_lanes,
                                                    max_waiting_time_in_red_lanes,
                                                    no_emv_current_lane, no_emv_other_lane)

        print(traffic_command)

        if traffic_command >= 0.5:
            if current_moving_lane(trafficLightID) == 'WE':
                yellow = True
                traci.trafficlight.setRedYellowGreenState("C", NS_GREEN_STATE)
            else:
                yellow = True
                traci.trafficlight.setRedYellowGreenState("C", WE_GREEN_STATE)

            print('sumo changed the traffic light')
    traci.simulationStep()
    step += 1

traci.close()
print("total_vehicle_waiting_time")
print(total_vehicle_waiting_time)
print("emv_waiting_time")
print(emv_waiting_time)
input('Press any key to exit')
