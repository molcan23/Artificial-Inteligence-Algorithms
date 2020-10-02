import colorama
import os
import sys
import time

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


class simulator:
    __map = {}
    __golds = {}
    __moveR = 0
    __deathR = 0
    __maxX = 0
    __maxY = 0

    def loadWorld(self, file):
        f = open(file, 'r')
        data = f.read().split('\n')
        f.close()
        self.__parse(data)

    def __parse(self, data):
        self.__moveR = float(data[0])
        self.__deathR = float(data[1])
        golds = int(data[3])
        for i in range(4, 4 + golds):
            posVal = data[i].split(' ')
            self.__golds[(int(posVal[0]), int(posVal[1]))] = float(posVal[2])
        startFrom = 4 + golds
        y = 0
        for i in range(startFrom, len(data)):
            x = 0
            for c in data[i]:
                self.__map[(x, y)] = c
                x += 1
            self.__maxX = max(self.__maxX, x)
            y += 1
        self.__maxY = y

    def simulate(self, positions):
        score = 0
        steps = 0
        proceed = True
        for pos in positions:
            takeGold = False
            if steps > 0:
                c = self.__map[(pos[0], pos[1])]
                if c == 'O':
                    proceed = False
                    score += self.__deathR
                elif c == 'G':
                    takeGold = True
                    if (pos[0], pos[1]) in self.__golds:
                        score += self.__golds[(pos[0], pos[1])]
                else:
                    score += self.__moveR
            self.__printWorld(pos[0], pos[1], score, steps)
            steps += 1
            time.sleep(.05)
            if takeGold == True:
                self.__map[(pos[0], pos[1])] = ' '
            if proceed == False:
                break

    def __printWorld(self, hX, hY, score, steps):
        for y in range(1, self.__maxY + 1):
            for x in range(1, self.__maxX + 1):
                print(pos(x, y), end='')
                if hX == x - 1 and hY == y - 1:
                    print(colorama.Fore.RED + '@' + colorama.Fore.RESET, end='')
                    continue
                c = self.__map[(x - 1, y - 1)]
                if c == '#':
                    print(colorama.Fore.WHITE + '█' + colorama.Fore.RESET, end='')
                elif c == 'O':
                    print(colorama.Back.RED + colorama.Fore.BLACK + '▓' + colorama.Style.RESET_ALL, end='')
                elif c == 'G':
                    print(colorama.Fore.LIGHTYELLOW_EX + '■' + colorama.Fore.RESET, end='')
                else:
                    print(colorama.Fore.GREEN + '░' + colorama.Fore.RESET, end='')
            print()
        print(pos(1, self.__maxY + 1) + ("Reward: {:+.4f} - Steps: {:d}".format(score, steps)) + "        ", end='')


def simulate(mapFile, moves):
    colorama.init()
    print('\x1b[2J', end='')
    hide_cursor()

    sim = simulator()
    sim.loadWorld(mapFile)
    sim.simulate(moves)

    show_cursor()
    input()
    print('\x1b[2J', end='')
    colorama.deinit()


if __name__ == "__main__":
    simulate("mapa1.txt",
             [(3, 2), (3, 3), (4, 3), (5, 3), (6, 3), (6, 4), (7, 4), (8, 4), (9, 4), (9, 5), (10, 5), (11, 5), (12, 5),
              (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6), (19, 5), (20, 5), (20, 4),
              (21, 4), (22, 4), (23, 4), (24, 4), (25, 4), (26, 4), (27, 4), (28, 4), (28, 3), (28, 2), (29, 2),
              (30, 2), (31, 2), (32, 2)])
