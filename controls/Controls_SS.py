from spherov2 import scanner # turning works on relative direction, need to update code to match
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import multiprocessing
import threading
import time
import sys

def toy_manager(toy, id):
    global commands
    with SpheroEduAPI(toy) as api:
        while True:
            print(id)
            global allReady
            global commands

            choosenColor = Color(r = 0, g = 255, b = 0)
            
            magBase = 0
            direction = 0   
            numIterations = 0

            while True and commands[id] != []:
                print("{}: {}".format(id, commands[id][0]))
                if (commands[id][0] == "%"): # be very careful with this - needs to be the absolute last command!
                    return
                elif (commands[id][0] == "CALIBRATE"):
                    api.calibrate_compass() # not perfect - need feedback
                    magBase = api.get_compass_direction()
                    api.set_main_led(choosenColor)
                elif (commands[id][0][0] == "M"): #MOVE:XXX:YYY    - Moves in preset direction at XXX speed for YYY seconds
                    api.roll(magBase + direction, int(commands[id][0][2:4]), float(commands[id][0][6:]))
                    time.sleep(0.5)
                elif (commands[id][0][0] == "R"): #ROTATE: R:XXX
                    direction += int(commands[id][0][2:])
                    # probably need to graph sphero turning in order to get a good idea of what the rotate command should be
                elif (commands[id][0][0] == "C"): #COLOR CHANGE: C:RRR:GGG:BBB    - sets color to these rgb vals
                    choosenColor = Color(r = int(commands[id][0][2:4]), g = int(commands[id][0][6:8]), b = int(commands[id][0][10:12]))
                    api.set_main_led(choosenColor)
                    api.set_front_led(choosenColor)
                    api.set_back_led(choosenColor)
                elif (commands[id][0][0] == "D"):
                    time.sleep(float(commands[id][0][2:]))
                else:
                    print(commands[id][0] + " in ball {} is an invalid command!".format(id))
                commands[id].pop(0) #Pops the command that was just executed
                allReady[id][numIterations] = 1
                while True:
                    ready = True
                    for readiness in allReady:
                        if (readiness[numIterations] == 0):
                            ready = False
                            break
                    if (ready):
                        break
                numIterations += 1
                time.sleep(1)

def commandInputs(toys): # needs to be able to consistently take in data
    global commands
    global allReady
    
    commands = []
    allReady = []

    #commands = [[], [], []]

    command =  ["CALIBRATE", "C:000:255:120", "M:155:0.25", "R:90", "M:255:0.25", "R:30", "D:2", "M:100:0.5", "%"]
    for toy in toys:
        commands.append(command) # matrix is needed for more complex commands
        allReady.append([0] * len(command))

def commandReading(toys):
    pass

def run_toy_threads(toys):
    id = 0
    threads = []
    
    global commands
    global allReady

    commandInputs(toys)

    #commands = [["Cblack", "c", "m", "R90", "m", "%"]] #["Cblack", "c", "m", "R90", "m", "%"]]
    #allReady = ([0] * len(commands[0])) * len(commands)
    #print(allReady)

    for toy in toys:
        thread = threading.Thread(target=toy_manager, args=[toy, id])
        threads.append(thread)
        thread.start()
        id += 1
    
    for thread in threads:
        thread.join()
        
    print("Ending function...")

toys = scanner.find_toys() # can't use normal find toy in conjunction "SB-76B3", "SB-1840", "SB-B11D"
# seems to raise bleak exception errors if it is done that way 

print(toys)

try: 
    for toy in toys: # fighting back against the bleak error exceptions
        with SpheroEduAPI(toy) as api:
            api.calibrate_compass()
            api.reset_aim()
except:
    print("Error!")
    sys.exit()

run_toy_threads(toys)