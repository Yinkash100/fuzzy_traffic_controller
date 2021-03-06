import pickle
from fuzzy_traffic_controller import fuzzy_controller_function
from helper_functions import *


# check if sumo home is defined
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "4-junction/4-junction.sumocfg", "--start"]

import traci
traci.start(sumoCmd)

lanes_in_G2H1 = ['F2_0', 'F2_1', 'G2_0', 'G2_1', 'H1_0', 'H1_1', 'I1_0', 'I1_1']
lanes_in_D1B2 = ['A2_0', 'A2_1', 'B2_0', 'B2_1', 'D1_0', 'D1_1', 'E1_0', 'E1_1']

total_vehicle_waiting_time = 0
emv_waiting_time = 0

trafficLightID = traci.trafficlight.getIDList()[0]

no_stopped = []
no_moving = []

step = 0
while step < 32000:
# while step < 100:
    # The get current lane the traffic light is passing
    lanes_currently_moving, lanes_stopped_by_light = get_lane_lists(lanes_in_D1B2, lanes_in_G2H1, trafficLightID)

    # Get cars in both lanes lane
    vehicles_in_red_lanes = get_vehicles_in_lane(lanes_stopped_by_light)
    vehicles_in_green_lanes = get_vehicles_in_lane(lanes_currently_moving)

    # Get no of cars in both lane
    no_vehicles_in_red_lanes = len(vehicles_in_red_lanes)
    no_vehicles_in_green_lanes = len(vehicles_in_green_lanes)
    no_moving.append(no_vehicles_in_green_lanes)
    no_stopped.append(no_vehicles_in_red_lanes)

    # Get waiting time of cars in red-light lane
    vehicles_waiting_time = vehicle_waiting_time_in_lane(vehicles_in_red_lanes)
    if vehicles_waiting_time != 0:
        vehicles_waiting_time.sort()
        max_waiting_time_in_red_lanes = vehicles_waiting_time[-1]
        sum_wt_time = sum(vehicles_waiting_time)
        total_vehicle_waiting_time += sum_wt_time
#        wt_vehicles.append(sum_wt_time)

    # waiting time of emergency vehicles in red light
    emv_waiting_time_red_lane = get_emv_waiting_time(vehicles_in_red_lanes)
    emv_waiting_time_green_lane = get_emv_waiting_time(vehicles_in_green_lanes)

    emv_waiting_time +=  emv_waiting_time_red_lane
    emv_waiting_time +=  emv_waiting_time_green_lane

    # Get emergency vehicles count
    emv_current_lane = get_emv(vehicles_in_green_lanes)
    emv_other_lane = get_emv(vehicles_in_red_lanes)

    no_emv_current_lane = len(emv_current_lane)
    no_emv_other_lane = len(emv_other_lane)
 #   wt_emv.append(emv_waiting_time_red_lane + emv_waiting_time_green_lane)

    if (step > 0) and (step % 7) == 0:
        traffic_command = fuzzy_controller_function(no_vehicles_in_red_lanes,
                                                    no_vehicles_in_green_lanes,
                                                    max_waiting_time_in_red_lanes,
                                                    emv_waiting_time_red_lane, emv_waiting_time_green_lane,
                                                    no_emv_current_lane, no_emv_other_lane)

        if traffic_command >= 0.5:
            current_phase = traci.trafficlight.getPhase("C")
            if current_phase < 5:
                traci.trafficlight.setPhase("C", 4)
            else:
                traci.trafficlight.setPhase("C", 9)
        print('done')
    traci.simulationStep()
    step += 1

traci.close()
print("total_vehicle_waiting_time")
print(total_vehicle_waiting_time)
print("emv_waiting_time")
print(emv_waiting_time)


# with open("combined_emv_waiting_time.txt", "wb") as fp:
#     pickle.dump(wt_emv, fp)
#
# with open("vehicles_waiting_time.txt", "wb") as fp:
#     pickle.dump(wt_vehicles, fp)

with open("amount_stopped_vehicles.txt", "wb") as fp:
    pickle.dump(no_stopped, fp)

with open("amount_moving_vehicles.txt", "wb") as fp:
    pickle.dump(no_moving, fp)

print('no o stopped')
print(len(no_stopped))
# print(no_stopped)


print('no o moving')
print(len(no_moving))
# print(no_moving)

input('Press any key to exit')