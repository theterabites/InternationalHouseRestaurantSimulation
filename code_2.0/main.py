import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from InternationalHouse import *

N_STUDENT = 600
OPERATING_SECONDS = 12_600
SID = [30386*1000+i for i in range(N_STUDENT)]
arrival_time_distrib : list = 10_800-rd.gamma(shape=5, scale = 3600/5, size=N_STUDENT)
arrival_time_distrib = np.vectorize(lambda x: x if x >= 0 else 0)(arrival_time_distrib)
arrival_time_distrib = sorted(arrival_time_distrib) 
dining_hall = Dining_Hall()
student_list :list[Student] = []
for n in range(N_STUDENT) :
    stud = Student(SID[n], dining_hall, arrival_time = arrival_time_distrib[n])
    student_list.append(stud)
student_counter = 0
time = 0

plt.hist(arrival_time_distrib, 12)
plt.show()



while time < 12600 :
    time += 1
    if time%10 == 0 :
        print(f'processed at {time/OPERATING_SECONDS*100}%')
    if student_counter<N_STUDENT and arrival_time_distrib[student_counter] < time :
        stud = student_list[student_counter]
        dining_hall.student_list.append(stud)
        stud.go_to_queue()
        student_counter += 1
    dining_hall.process_queue()
    dining_hall.process_eating()

wait_list = [stud.wait_time for stud in student_list]

df_out = pd.DataFrame({
        "sid":list([student_list[i].sid for i in range(N_STUDENT)]),
        "arrival_time":arrival_time_distrib,
        "waiting_time":list([student_list[i].wait_time for i in range(N_STUDENT)]),
        "number_of_plate":list([len(student_list[i].hot_dishes) for i in range(N_STUDENT)]),
        })

# plot 
# plt.hist(wait_list,10)
# plt.show()

#csv
# df_out.to_csv("out.csv")
# print(df_out)