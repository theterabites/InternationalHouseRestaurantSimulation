import numpy.random as rd
N_DISHES = 8
N_DRINKS = 8
HOT_DISH_LIST = [
    f'hot_dish_{i}' for i in range(N_DISHES)
]
DRINK_LIST = [
    f'drink_{i}' for i in range(N_DRINKS)
]


class Dining_Hall :
    def __init__(self) -> None:
        self.student_list: list[Student] = [] # students present in the dining hall
        self.hot_dishes_list = HOT_DISH_LIST
        self.hot_dishes_queue :list[Student] = []
        self.hot_dishes_student_serving :list[(Student,int)] = []
        self.isClose = False
        self.student_eating_list :list[Student] = []
        # start w/ students in the dining hall
        # then init hot dish list
        # init Q of hot dish w/ empty list
        

    def process_queue(self) :
        while len(self.hot_dishes_queue) != 0 :
            idx_list = [idx for stud, idx in self.hot_dishes_student_serving]
            idx = min(idx_list + [len(self.hot_dishes_list)])
            stud = self.hot_dishes_queue[0]
            stud_dish = stud.hot_dishes[0]
            if  stud_dish in self.hot_dishes_list[:idx] :
                self.hot_dishes_student_serving.append((stud, self.hot_dishes_list.index(stud_dish)))
                self.hot_dishes_queue.remove(stud)
            else : 
                break
        for stud,idx in self.hot_dishes_student_serving : 
            stud.serve()

        for stud in self.hot_dishes_queue :
            stud.wait()
        
            
    def process_eating(self) :
        for stud in self.student_eating_list :
            stud.eat()


class Student :
    def __init__(self, sid, dining_hall, arrival_time) :
        self.sid = sid
        self.dining_hall : Dining_Hall = dining_hall
        self.wait_time : int = 0 # wait time in seconds
        self.move : int = rd.normal(20, 5, 1) # time to go to the restaurant
        self.move_time : int = self.move
        self.is_moving : bool = False
        self.time_to_eat : int = rd.normal(1000, 300) # time the student has been eating
        self.eat_time : int = 0
        self.random : int = rd.randint(0,8,size = int(4*rd.random())+1)
        self.hot_dishes = [self.dining_hall.hot_dishes_list[i] for i in self.random] # list containing all the hot_dishes the student will take
        self.serve_time : int = 0
        self.time_to_serve: int = 20 
        #create a new param to store arrival time
        self.arrival_time : int = arrival_time

    
    def eat(self) :
        self.eat_time += 1
        if self.time_to_eat <= self.eat_time :
            self.eat_time = 0
            self.hot_dishes.pop(0)
            if len(self.hot_dishes) == 0 :
                self.leave_dining_hall()
            else : 
                self.go_to_queue()
                self.dining_hall.student_eating_list.remove(self)
        
    def serve(self) :
        self.serve_time += 1
        if self.time_to_serve <= self.serve_time :
            self.serve_time = 0
            self.dining_hall.hot_dishes_student_serving.remove((self,self.dining_hall.hot_dishes_list.index(self.hot_dishes[0])))
            self.go_to_eat()

    def go_to_queue(self) :
        self.dining_hall.hot_dishes_queue.append(self)

    def go_to_eat(self) :
        self.dining_hall.student_eating_list.append(self)

    def leave_dining_hall(self) :
        self.dining_hall.student_list.remove(self)
        self.dining_hall.student_eating_list.remove(self)
    
    def wait(self) :
        self.wait_time += 1
            

        
