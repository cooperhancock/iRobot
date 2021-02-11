# Robot Command Line Program
# Cooper Hancock
# February 2021
# some Robot Class code provided in CSCI Lab by Nabil Khan

import random
import time
import os
import sys
import msvcrt
import threading

###################
# UTILS & STARTUP #
###################

# terminal window size
size = os.get_terminal_size()

# commands
commands = 'commands: t: teleop, n: navigate, p: play game, c: coordinates (row, col), g: set goal, q: quit'

# console clear
def clear(num=100, kind='line'):
    if kind == 'line':
        print('\b'*num,end='',flush=True)
    elif kind == 'clear':
        os.system('cls')

# available command line args:
#
# GENERAL (may run multiple together)
# 'fast': sets loading flourishes to instant load (FAST)
# 'kinda-fast': sets loading flourishes to double time
# 'debug': runs #DEBUG# code before startup
#
# INITIAL COMMAND 
# 'no-render': does not render world after startup
# 'teleop': enters teleop mode automatically after startup
# 'game': enters game mode after startup
#
# STARTUP (bypass startup options)
# 'default': 10x10 world with robot at 0,0 and goal at 9,9
# 'auto': auto create largest world, robot and goal in opposite corners
# 

# GENERAL - FAST
if 'fast' in sys.argv: 
    qtr = 0.25 # quarter second
    half = 0.5 # half second
    denominator = 100 # shorten sleep times
elif 'kinda-fast' in sys.argv:
    qtr = 0.25/2 # quarter second
    half = 0.5/2 # half second
    denominator = 2 # shorten sleep times
else:
    qtr = 0
    half = 0
    denominator = 1
# INITIAL COMMAND
if 'no-render' in sys.argv: 
    startmode = ''
elif 'teleop' in sys.argv: 
    startmode = 't'
elif 'game' in sys.argv:
    startmode = 'p'
else:
    startmode = 'r' # by default, render world on startup

# loading bar flourish with given character length
def loading_bar(size):
    for i in range(size-1):
        print('['+'#'*i+'.'*(size-2-i)+']',end='', flush=True)
        time.sleep(random.randrange(1,10)/(10*denominator))
        clear(size)
    print()

# startup sequence returns world irobot
def startup():
    clear(1,'clear')
    options = ['default','auto','custom']
    print('welcome to iRobot')
    print('*****loading*****')
    loading_bar(17)
    if 'default' in sys.argv:
        irobot = init_wizard('default')
    elif 'auto' in sys.argv:
        irobot = init_wizard('auto')
    else:
        startup_option = input("choose a world creation option: "+str(options)+' ')
        while not startup_option in options:
            print('not a valid option')
            startup_option = input("choose a world creation option: "+str(options)+' ')
        irobot = init_wizard(startup_option)
    time.sleep(1-half*2)
    clear(1,'clear')
    print(commands)
    return irobot


# shutdown flourish
def shutdown():
    print('shutting down', end='', flush=True)
    for i in range(4):
        print('.', end='', flush=True)
        time.sleep(0.25-qtr)
    print()
    print('code by Cooper Hancock')
    time.sleep(0.5-half)
    print('goodbye!')
    time.sleep(0.5)

# breaker variable to manage game
breaker = [False]
points = 0

###############
# ROBOT CLASS #
###############

class Robot:
    def __init__(self,x,y,n):
        self.pos_x = x
        self.pos_y = y
        self.world = []
        self.size = n
        self.goal_x = n-1
        self.goal_y = n-1
        for i in range(n):
            row = []
            for j in range(n):
                row.append('*')
            self.world.append(row)
        self.world[x][y] = 'R'
        self.world[self.goal_x][self.goal_y] = 'G'

    # single step of a robot in the direction given as input (actions = w, a, s, d)
    def step(self, action):
        if action == 'a' and self.pos_y != 0:
            self.world[self.pos_x][self.pos_y] = '*'
            self.pos_y -= 1
            self.world[self.pos_x][self.pos_y] = 'R'
        elif action == 'd' and self.pos_y != self.size-1:
            self.world[self.pos_x][self.pos_y] = '*'
            self.pos_y += 1
            self.world[self.pos_x][self.pos_y] = 'R'
        elif action == 'w' and self.pos_x != 0:
            self.world[self.pos_x][self.pos_y] = '*'
            self.pos_x -= 1
            self.world[self.pos_x][self.pos_y] = 'R'
        elif action == 's' and self.pos_x != self.size-1:
            self.world[self.pos_x][self.pos_y] = '*'
            self.pos_x += 1
            self.world[self.pos_x][self.pos_y] = 'R'

    # multiple steps to the goal location
    def navigate(self):
        #self.world[self.goal_x][self.goal_y] = 'G'
        while (self.goal_x != self.pos_x):
            if self.goal_x < self.pos_x:
                action = 'w'
            elif self.goal_x > self.pos_x:
                action = 's'
            self.step(action)
            clear(1, 'clear')
            print(self)
            #print(self.goal_x, self.pos_x)
            time.sleep(0.25)
        while (self.goal_y != self.pos_y):
            if self.goal_y < self.pos_y:
                action = 'a'
                #print('a')
            elif self.goal_y > self.pos_y:
                action = 'd'
                #print('d')
            self.step(action)
            clear(1, 'clear')
            print(self)
            #print(self.goal_y, self.pos_y)
            time.sleep(0.25)

    def __str__(self):
        s = '\n'
        for i in range(self.size):
            for j in range(self.size):
                s += self.world[i][j] + ' '
            s += '\n'
        return s

    # teleop control of passed in robot, render refresh after each command
    # w, a, s, d for move, q for quit, r for re-render
    def teleop(self):
        print(self)
        actions = ['w', 'a', 's', 'd']
        action = 'r'
        while action != 'q':
            print('<iRobot Teleop> move with w,a,s,d; q: quit; r: render')
            action = msvcrt.getwch()
            if action == 'q':
                break
            elif action == 'r':
                print(self)
            elif action in actions:
                self.step(action)
                clear(1, 'clear')
                print(self)
            else:
                print('invalid')
                continue

    # renders world in game mode with given score
    def render(self, time):
        global points
        s = '\n'
        s += 'score: ' + str(points) + '\t' + str(time) + '\n'
        for i in range(self.size):
            for j in range(self.size):
                s += self.world[i][j] + ' '
            s += '\n'
        clear(1,'clear')
        print(s)

#######################
# NON-CLASS FUNCTIONS #
#######################

# goal set to given goal array [[row], [col]]
def goal_set(goal, robot):
    robot.world[robot.goal_x][robot.goal_y] = '*'
    robot.goal_x = goal[0]
    robot.goal_y = goal[1]
    robot.world[robot.goal_x][robot.goal_y] = 'G'
    robot.world[robot.pos_x][robot.pos_y] = 'R'

def game_listener(robot,timerStart,timerEnd):
    actions = ['w', 'a', 's', 'd']
    action = ''
    global points
    while time.perf_counter()-timerStart < timerEnd:
        action = msvcrt.getwch()
        if action in actions:
            robot.step(action)
            clear(1,'clear')
            robot.render(time.perf_counter()-timerStart)
        elif action == 'q':
            global breaker
            breaker = [True]
            time.sleep(2)
            print('stopping')
            return
        if robot.goal_x == robot.pos_x and robot.goal_y == robot.pos_y:
            points += 1
            goal_set([random.randint(0,robot.size),random.randint(0,robot.size)],robot)
            clear(1,'clear')
            robot.render(time.perf_counter()-timerStart)

# game
def game(robot):
    global breaker
    global points
    print('loading game')
    loading_bar(12)
    print('use w,a,s,d to move your robot and collect as many G\'s as you can in 1 minute')
    start = input('press enter to start: ')
    timerStart = time.perf_counter()
    clear(1,'clear')
    robot.render(time.perf_counter()-timerStart)
    listener = threading.Thread(target=game_listener,name='listener',args=(robot,timerStart,60,))
    listener.start()
    while time.perf_counter()-timerStart < 60:
        clear(1, 'clear')
        robot.render("{:.2f}".format(time.perf_counter()-timerStart))
        time.sleep(1)
        if True in breaker:
            listener.join()
            break
    listener.join()
    clear(1,'clear')
    robot.render(60)
    time.sleep(1)
    print('end of game: you earned',points,'points!')
    breaker = [False]
    endgame_command = input('press p to play again or r to return to iRobot Home: ')
    return endgame_command

# runs initialization wizard for new robot, returns new robot
def init_wizard(mode=''):
    print('welcome to the world initialization wizard')
    time.sleep(0.5-half)
    print('loading: ', end='', flush=True)
    loading_bar(17)
    max_size = min(size.columns, size.lines)-4
    print('available world size is ', max_size)
    if mode == 'auto':
        print('auto build ',end='',flush=True)
        loading_bar(10)
        robot = Robot(0,0,max_size)
        print('***building world***')
        loading_bar(20)
        return robot
    elif mode == 'default':
        print('default build ',end='',flush=True)
        loading_bar(10)
        robot = Robot(0,0,10)
        print('***building world***')
        loading_bar(20)
        return robot
    print('custom build ',end='',flush=True)
    loading_bar(10)
    chosen_size = input('enter world size up to max size: ')
    while True:
        try:
            chosen_size = int(chosen_size)
        except:
            chosen_size = 1000
        if chosen_size<max_size:
            break
        else:
            chosen_size = input('invalid size, try again: ')
    while True:
        robotInfo = list(map(int,input('enter robot starting [row] [col]: ').strip().split()))
        if robotInfo[0]>-1 and robotInfo[0]<chosen_size and robotInfo[1]>-1 and robotInfo[1]<chosen_size:
            robot = Robot(robotInfo[0], robotInfo[1], chosen_size)
            break
        else:
            print('invalid coordinates')
    while True:
            goal = list(map(int,input('enter goal location [row] [col]: ').strip().split()))
            if goal[0]<robot.size and goal[0]>-1 and goal[1]<robot.size and goal[1]>-1:
                goal_set(goal, robot)
                break
            else:
                print('invalid coordinates')
    print('***building world***')
    loading_bar(20)
    return robot

#########
# DEBUG #
#########

if 'debug' in sys.argv: # debug code to run
    startmode = ''
    # enter debug code here:
    print('hi')
    time.sleep(1)
    clear()
    time.sleep(1)
    print('test')
    #inthing = msvcrt.getwch()
    #print(inthing)
    #clear(10, 'clear')   

########
# MAIN #
########

def main(): 
    # set from command line args
    mode = startmode

    # initialize irobot
    irobot = startup()
    
    # main command interface
    while mode != 'q':
        if mode == 'r':
            print(irobot)
        elif mode == 't':
            irobot.teleop()
        elif mode == 'n':
            irobot.navigate()
        elif mode == 'p':
            mode = game(irobot)
        elif mode == 'c':
            print(irobot.pos_x, irobot.pos_y)
        elif mode == 'h' or mode == 'help':
            print(commands)
        elif mode == 'g':
            while mode == 'g':
                goal = list(map(int,input('enter [row] [col]: ').strip().split()))
                if goal[0]<irobot.size and goal[0]>-1 and goal[1]<irobot.size and goal[1]>-1:
                    goal_set(goal, irobot)
                    mode = 'r'
                else:
                    print('invalid coordinates')
                    mode = 'g'
        elif mode == 'easter egg':
            print("i'm an easter egg lol")
            print('p.s. i had way too much fun writing this code')
        elif mode == '':
            pass
        else:
            print('invalid command - enter h for help')
            continue
        mode = input('iRobot> ') 
    shutdown()

main()