import sys
import colorama
import copy
import time
import os

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def pos(x, y):
    return '\x1b[' + str(y) + ';' + str(x) + 'H'

class world:
    __map = {}
    __totalGold = 0
    __maxX = 0
    __maxY = 0
    __startX = 0
    __startY = 0

    __simMap = {}
    __simX = 0
    __simY = 0

    __stopSim = False

    __actions = []
    __arrows = 0

    def loadWorld(self, file):
        f = open(file, 'r')
        data = f.read().split('\n')
        f.close()
        self.__parse(data)

    def __parse(self, data):
        y = 0
        for line in data:
            self.__maxY = y
            x = 0
            for char in line:
                self.__maxX = max(self.__maxX, x)
                self.__map[(x,y)] = char
                if char == 'g':
                    self.__totalGold+=1
                if char == '@':
                    self.__startX = x
                    self.__startY = y
                x+=1
            y+=1

    def loadActions(self, file):
        f = open(file, 'r')
        self.__actions = f.read().split('\n')
        f.close()
        self.__actions = [action for action in self.__actions if len(action) > 0]

    def simulateInit(self):
        self.__simMap = copy.deepcopy(self.__map)
        self.__simX = self.__startX
        self.__simY = self.__startY
        self.__stopSim = False
        self.__arrows = 0
        self.__printSimulatedMap()

    def simulate(self, action):
        if action == 'move-right':
            if (self.__simMap[(self.__simX+1, self.__simY)] != '#'):
                self.__simX+=1
            else:
                self.__error("Moved into wall!")
        elif action == 'move-left':
            if (self.__simMap[(self.__simX-1, self.__simY)] != '#'):
                self.__simX -= 1
            else:
                self.__error("Moved into wall!")
        elif action == 'move-up':
            if (self.__simMap[(self.__simX, self.__simY-1)] != '#'):
                self.__simY -= 1
            else:
                self.__error("Moved into wall!")
        elif action == 'move-down':
            if (self.__simMap[(self.__simX, self.__simY+1)] != '#'):
                self.__simY += 1
            else:
                self.__error("Moved into wall!")
        elif action == 'shoot-wumpus-right':
            if (self.__simMap[(self.__simX + 1, self.__simY)] == 'W'):
                if (self.__arrows > 0):
                    self.__simMap[(self.__simX + 1, self.__simY)] = ' '
                    self.__arrows -= 1
                else:
                    self.__error("Hunter has no arrow to shoot!")
            else:
                self.__error("There is no Wumpus at right from the hunter to shoot!")
        elif action == 'shoot-wumpus-left':
            if (self.__simMap[(self.__simX - 1, self.__simY)] == 'W'):
                if (self.__arrows > 0):
                    self.__simMap[(self.__simX - 1, self.__simY)] = ' '
                    self.__arrows -= 1
                else:
                    self.__error("Hunter has no arrow to shoot!")
            else:
                self.__error("There is no Wumpus at left from the hunter to shoot!")
        elif action == 'shoot-wumpus-up':
            if (self.__simMap[(self.__simX, self.__simY - 1)] == 'W'):
                if (self.__arrows > 0):
                    self.__simMap[(self.__simX, self.__simY - 1)] = ' '
                    self.__arrows -= 1
                else:
                    self.__error("Hunter has no arrow to shoot!")
            else:
                self.__error("There is no Wumpus at up from the hunter to shoot!")
        elif action == 'shoot-wumpus-down':
            if (self.__simMap[(self.__simX, self.__simY + 1)] == 'W'):
                if (self.__arrows > 0):
                    self.__simMap[(self.__simX, self.__simY + 1)] = ' '
                    self.__arrows -= 1
                else:
                    self.__error("Hunter has no arrow to shoot!")
            else:
                self.__error("There is no Wumpus at down from the hunter to shoot!")
        elif action == 'take-gold':
            if (self.__simMap[(self.__simX, self.__simY)] == 'g'):
                self.__simMap[(self.__simX, self.__simY)] = ' '
            else:
                self.__error("There is no gold to take!")
        elif action == 'take-arrow':
            if (self.__simMap[(self.__simX, self.__simY)] == 'A'):
                self.__simMap[(self.__simX, self.__simY)] = ' '
                self.__arrows += 1
            else:
                self.__error("There is no arrow to take!")
        
        if (self.__simMap[(self.__simX, self.__simY)] == 'W'):
            self.__error("Wumpus killed the hunter!")

        self.__printSimulatedMap()

    def __printSimulatedMap(self):
        for y in range(0, self.__maxY + 1):
            for x in range(0, self.__maxX + 1):
                print(pos(x+1, y+1), end='')
                if self.__simMap[(x,y)] == '#':
                    print(colorama.Fore.WHITE + '#' + colorama.Fore.RESET, end='')
                else:
                    if self.__simMap[(x,y)] == 'W':
                        print(colorama.Fore.RED + 'W' + colorama.Fore.RESET)
                    elif self.__simMap[(x,y)] == 'g':
                        print(colorama.Back.YELLOW + ' ' + colorama.Back.RESET)
                    elif self.__simMap[(x,y)] == 'A':
                        print(colorama.Fore.GREEN + 'A' + colorama.Fore.RESET)
                    else:
                        print(' ', end='')
        if self.__simMap[(self.__simX, self.__simY)] == 'g':
            print(pos(self.__simX + 1, self.__simY + 1) + colorama.Fore.CYAN + colorama.Back.YELLOW + '@' + colorama.Back.RESET + colorama.Fore.RESET)
        else:
            print(pos(self.__simX + 1, self.__simY + 1) + colorama.Fore.CYAN + '@' + colorama.Fore.RESET)
        
    def __error(self, message):
        print(pos(1, self.__maxY + 2) + colorama.Fore.RED + "ERROR: " + message + colorama.Fore.RESET)
        self.__stopSim = True

    def __testNoGold(self):
        for y in range(0, self.__maxY + 1):
            for x in range(0, self.__maxX + 1):
                if (self.__simMap[(x,y)] == 'g'):
                    return False
        return True

    def __isBackOnStart(self):
        return self.__simX == self.__startX and self.__simY == self.__startY

    def endsimulation(self):
        if self.__testNoGold() and self.__isBackOnStart():
            print(pos(1, self.__maxY + 2) + colorama.Fore.GREEN + "FINISHED: Press ENTER to continue ..." + colorama.Fore.RESET)
            self.__stopSim = True
        elif not self.__testNoGold():
            self.__error("There is one or more gold pieces left in the world!")
        elif not self.__isBackOnStart():
            self.__error("Hunter is not there where he starts!")
        input()

    def isSimulationRunning(self):
        return not self.__stopSim

    def getActions(self):
        return copy.deepcopy(self.__actions)

def simulate(worldFile, actionsFile):
    colorama.init()
    print('\x1b[2J', end='')
    hide_cursor()
    w = world()
    w.loadActions(actionsFile)
    w.loadWorld(worldFile)
    w.simulateInit()
    for action in w.getActions():
        if w.isSimulationRunning():
            time.sleep(.1)
            w.simulate(action)
    show_cursor()
    if w.isSimulationRunning():
        w.endsimulation()
    else:
        input()
    print('\x1b[2J', end='')
    colorama.deinit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Program needs two arguments!")
        print("Example: python3 " + sys.argv[0] + " world1.txt world1.txt.solution")
        sys.exit(1)
    else:
        worldFile = sys.argv[1]
        actionsFile = sys.argv[2]
        simulate(worldFile, actionsFile)