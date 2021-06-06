''' This is my first attempt to make a fuzzy controller for
Air conditioning system.... what a drag '''
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

no_vehicle_current_lane = ctrl.Antecedent(np.arange(0, 13, 1), 'no_vehicle_current_lane')
no_vehicle_other_lane = ctrl.Antecedent(np.arange(0, 13, 1), 'no_vehicle_D2B1')

waiting_time_current_lane = ctrl.Antecedent(np.arange(0, 60, 1), 'waiting_time_current_lane')
waiting_time_other_lane = ctrl.Antecedent(np.arange(0, 60, 1), 'waiting_time_other_lane')


emergency_vehicles_in_other_lane = ctrl.Antecedent(np.arange(0, 4, 1), 'emergency_vehicles_in_other_lane')
emergency_vehicles_in_current_lane = ctrl.Antecedent(np.arange(0, 4, 1), 'emergency_vehicles_in_current_lane')

traffic_light_signal = ctrl.Consequent(np.arange(0, 2, 1), 'traffic_light_signal')









no_vehicle_current_lane['Too-small'] = fuzz.trimf(no_vehicle_current_lane.universe, [0, 0, 4])
no_vehicle_current_lane['small'] = fuzz.trimf(no_vehicle_current_lane.universe, [2, 5, 8])
no_vehicle_current_lane['much'] = fuzz.trimf(no_vehicle_current_lane.universe, [5, 8, 10])
no_vehicle_current_lane['Too-much'] = fuzz.smf(no_vehicle_current_lane.universe, 8, 10)
no_vehicle_current_lane.view()


no_vehicle_other_lane['too-small'] = fuzz.trimf(no_vehicle_other_lane.universe, [0, 0, 4])
no_vehicle_other_lane['small'] = fuzz.trimf(no_vehicle_other_lane.universe, [2, 5, 8])
no_vehicle_other_lane['much'] = fuzz.trimf(no_vehicle_other_lane.universe, [5, 8, 10])
no_vehicle_other_lane['too-much'] = fuzz.smf(no_vehicle_other_lane.universe, 8, 10)




waiting_time_current_lane['negligible'] = fuzz.trimf(waiting_time_current_lane.universe, [0, 0, 10])
waiting_time_current_lane['okay'] = fuzz.trimf(waiting_time_current_lane.universe, [10, 20, 30])
waiting_time_current_lane['much'] = fuzz.trimf(waiting_time_current_lane.universe, [20, 32, 45])
waiting_time_current_lane['too-much'] = fuzz.smf(waiting_time_current_lane.universe, 30, 45)
waiting_time_current_lane.view()

waiting_time_other_lane['negligible'] = fuzz.trimf(waiting_time_other_lane.universe, [0, 0, 10])
waiting_time_other_lane['okay'] = fuzz.trimf(waiting_time_other_lane.universe, [10, 20, 30])
waiting_time_other_lane['much'] = fuzz.trimf(waiting_time_other_lane.universe, [20, 32, 45])
waiting_time_other_lane['too-much'] = fuzz.smf(waiting_time_current_lane.universe, 30, 45)






emergency_vehicles_in_current_lane['absent'] = fuzz.zmf(emergency_vehicles_in_current_lane.universe, 0, 1)
emergency_vehicles_in_current_lane['present'] = fuzz.smf(emergency_vehicles_in_current_lane.universe, 0, 1)
emergency_vehicles_in_current_lane['much'] = fuzz.smf(emergency_vehicles_in_current_lane.universe, 1, 2)
emergency_vehicles_in_current_lane['too-much'] = fuzz.smf(emergency_vehicles_in_current_lane.universe, 2, 3)
# emergency_vehicles_in_current_lane.view()

emergency_vehicles_in_other_lane['absent'] = fuzz.zmf(emergency_vehicles_in_other_lane.universe, 0, 1)
emergency_vehicles_in_other_lane['present'] = fuzz.smf(emergency_vehicles_in_other_lane.universe, 0, 1)
emergency_vehicles_in_other_lane['much'] = fuzz.smf(emergency_vehicles_in_other_lane.universe, 1, 2)
emergency_vehicles_in_other_lane['too-much'] = fuzz.smf(emergency_vehicles_in_other_lane.universe, 2, 3)





traffic_light_signal['need-switching'] = fuzz.smf(traffic_light_signal.universe, 0, 1)
traffic_light_signal['okay'] = fuzz.zmf(traffic_light_signal.universe, 0, 1)
#traffic_light_signal.view()



##### FUNCTIONS THAT PASSS IN THE INPUT ####

# fan_speed.view()
# input('Press Enter')


# rule1a = ctrl.Rule(temperature['hot'] | humidity['low'], fan_speed['high'])
# rule1b = ctrl.Rule(temperature['hot'] | humidity['high'], fan_speed['medium'])
#
# rule2 = ctrl.Rule(humidity['medium'], fan_speed['medium'])
#
# rule3a = ctrl.Rule(temperature['Too-hot'] | humidity['low'], fan_speed['high'])
# rule3b = ctrl.Rule(temperature['Too-hot'] |
#                    humidity['high'], fan_speed['medium'])
#
# rule4a = ctrl.Rule(temperature['cold'] | humidity['low'], fan_speed['low'])
# rule4b = ctrl.Rule(temperature['cold'] | humidity['high'], fan_speed['low'])
#
# rule5a = ctrl.Rule(temperature['warm'] | humidity['low'], fan_speed['medium'])
# rule5b = ctrl.Rule(temperature['warm'] | humidity['high'], fan_speed['low'])
#
# rule6a = ctrl.Rule(temperature['Too-cold'] | humidity['low'], fan_speed['low'])
# rule6b = ctrl.Rule(temperature['Too-cold'] |
#                    humidity['high'], fan_speed['low'])
#
# fan_speed_ctrl = ctrl.ControlSystem(
#     [rule1a, rule1b, rule2, rule3a, rule3b, rule4a, rule4b, rule5a, rule5b, rule6a, rule6b])
# speed = ctrl.ControlSystemSimulation(fan_speed_ctrl)
#
# speed.input['temperature'] = int(x)
# speed.input['humidity'] = int(y)
#
# speed.compute()
# print(speed.output['fan_speed'] + "RPM")
# fan_speed.view(sim=speed)
input('Press any key to exit')