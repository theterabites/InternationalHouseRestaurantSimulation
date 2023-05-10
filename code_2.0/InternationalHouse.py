import numpy.random as rd

N_DISHES = 8
N_DRINKS = 8
N_DESERT = 8
N_ENTRIES = 8
N_SOUP = 2
ENTRIES_LIST = [
    f'entry_{i}' for i in range(N_ENTRIES)
]
HOT_DISH_LIST = [
    f'hot_dish_{i}' for i in range(N_DISHES)
]
DRINK_LIST = [
    f'drink_{i}' for i in range(N_DRINKS)
]

DESERT_LIST = [
    f'desert_{i}' for i in range(N_DESERT)
]
SOUP_LIST = [
    f'soup_{i}' for i in range(N_SOUP)
]
class Dining_Hall :
    def __init__(self) -> None:
        self.student_list: list[Student] = [] # students present in the dining hall

        #-------SOUP----------------#
        self.soups_list = HOT_DISH_LIST
        self.soups_queue :list[Student] = []
        self.soups_student_serving :list[(Student,int)] = []

        #-------ENTRY---------------#
        self.entries_list = HOT_DISH_LIST
        self.entries_queue :list[Student] = []
        self.entries_student_serving :list[(Student,int)] = []

        #-------HOT_DISHES---------------#
        self.hot_dishes_list = HOT_DISH_LIST
        self.hot_dishes_queue :list[Student] = []
        self.hot_dishes_student_serving :list[(Student,int)] = []

        #-------DRINKS---------------#
        self.drinks_list = DRINK_LIST
        self.drinks_queue :list[Student] = []
        self.drinks_student_serving :list[(Student,int)] = []

        #-------DESERT---------------#
        self.deserts_list = DRINK_LIST
        self.deserts_queue :list[Student] = []
        self.deserts_student_serving :list[(Student,int)] = []

        self.isClose = False
        self.student_eating_list :list[Student] = []

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
        
            
    def process_eating(self, time) :
        for stud in self.student_eating_list :
            stud.eat(time)


class Student :
    def __init__(self, sid, dining_hall) :
        self.sid = sid
        self.dining_hall : Dining_Hall = dining_hall
        self.wait_time : int = 0 # wait time in seconds
        self.move : int = rd.normal(20, 5, 1) # time to go to the restaurant
        self.move_time : int = self.move
        self.is_moving : bool = False
        self.time_to_eat : int = rd.normal(1000, 300) # time the student has been eating
        self.eat_time : int = 0
        self.random_hot_dishes : int = rd.randint(0,8,size = int(4*rd.random())+1)
        self.entries = self.dining_hall.entries_list
        self.hot_dishes = self.dining_hall.hot_dishes_list[self.random_hot_dishes]
        self.drinks = self.dining_hall.drinks_list
        self.deserts = self.dining_hall.deserts_list
        self.soups = self.dining_hall.soups_list

        self.serve_time : int = 0
        self.time_to_serve: int = 20 
    
    def wants_to_eat(self) :
        return len(self.entries) > 0 or len(self.hot_dishes) > 0 or len(self.drinks) > 0 or len(self.deserts) or len(self.soups) > 0
    
    def eat(self, time) :
        self.eat_time += 1
        if self.time_to_eat <= self.eat_time :
            self.eat_time = 0
            self.hot_dishes.pop(0)
            # the student leaves either because he does not want anything else or the access to the food is close
            if self.wants_to_eat()  or time > 10800:
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
            

        
