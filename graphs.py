import pickle
import matplotlib.pyplot as plt

labels = ['SUMO Fixed Time Traffic Controller', 'Fuzzy Logic Traffic Controller']
avg_vehicle_waiting_time = [3062, 1854]
avg_emv_waiting_time = [26.82, 5.3]

width = 0.15

fig, ax = plt.subplots()

ax.bar(labels, avg_vehicle_waiting_time, width, label='Avg vehicle waiting time')
ax.bar(labels, avg_emv_waiting_time, width,  bottom=avg_vehicle_waiting_time,
       label='Avg Emergency vehicle waiting time')

ax.set_ylabel('Time (s)')
ax.set_title('Waiting time by controller and vehicle type')
ax.legend()

plt.show()