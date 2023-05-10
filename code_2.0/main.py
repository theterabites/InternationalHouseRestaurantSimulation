import numpy as np
import matplotlib.pyplot as plt
from InternationalHouse import *

N_STUDENT = 60
SID = [30386*1000+i for i in range(600)]
arrival_time_distrib : list = rd.gamma(shape=5, scale = 3600/5, size=N_STUDENT)
arrival_time_distrib = sorted(arrival_time_distrib) 
dining_hall = Dining_Hall()
student_list :list[Student] = []
for n in range(N_STUDENT) :
    stud = Student(SID[n], dining_hall)
    student_list.append(stud)
student_counter = 0
time = 0

while time < 12600 :
    time += 1
    if time%10 == 0 :
        print(f'processed at {time/12600*100}%')
    if time == 10800 :
        dining_hall.isClose = True
    if student_counter<N_STUDENT and arrival_time_distrib[student_counter] < time :
        if not dining_hall.isClose :
            stud = student_list[student_counter]
            dining_hall.student_list.append(stud)
            stud.go_to_queue()
            student_counter += 1
    dining_hall.process_queue()
    dining_hall.process_eating(time)

wait_list = [stud.wait_time for stud in student_list]
plt.hist(wait_list,10)
plt.show()