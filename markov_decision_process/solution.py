import simulator
import sys
import math
from enum import Enum
import random

gamma = 0.99  # gamma in (0, 1), update this value as needed

# possible actions
class Actions(Enum):
    Up = 1
    Left = 2
    Down = 3
    Right = 4

moves_dir = {1: Actions.Up, 2: Actions.Left, 3: Actions.Down, 4: Actions.Right}


class world:
    __map = {}  # world map, each (x,y) cell also represents one state
    __golds = {}  # values of golds
    __steps = 0  # maximum allowed steps
    __moveR = 0  # movement reward
    __deathR = 0  # death reward
    __maxX = 0  # size of world x axis
    __maxY = 0  # size of world y axis
    __startX = 0  # treasure hunter start x coordinate
    __startY = 0  # treasure hunter start y coordinate
    __policy = {}  # action selection policy, a map from state (position x,y) to action (Actions class)

    def load(self, file):
        f = open(file, 'r')
        data = f.read().split('\n')
        f.close()
        self.__parse(data)

    # map data parser, do not touch this!
    # it will fill the variables of the world class
    def __parse(self, data):
        self.__moveR = float(data[0])
        self.__deathR = float(data[1])
        self.__steps = int(data[2])
        golds = int(data[3])
        for i in range(4, 4 + golds):
            posVal = data[i].split(' ')
            self.__golds[(int(posVal[0]), int(posVal[1]))] = float(posVal[2])
        startFrom = 4 + golds
        y = 0
        for i in range(startFrom, len(data)):
            x = 0
            for c in data[i]:
                if c == 'H':
                    self.__startX = x
                    self.__startY = y
                    self.__map[(x, y)] = ' '
                else:
                    self.__map[(x, y)] = c
                x += 1
            self.__maxX = max(self.__maxX, x)
            y += 1
        self.__maxY = y

    def print_map(self, V):
        for y in range(self.__maxY):
            line = []
            for x in range(self.__maxX):
                line.append("%10.03f" % V[(x, y)])
                # line.append("%d" % V[(x, y)])
            # map.append(line)
            print(line)

    def print_policy(self, V):
        for y in range(self.__maxY):
            line = []
            for x in range(self.__maxX):
                # line.append("%10.03f" % V[(x, y)])
                line.append("%d" % V[(x, y)])
            # map.append(line)
            print(line)

    def value_iteration(self, pos, action, V_i):
        value = 0
        a = self.__newPosition(pos, moves_dir[action])
        b = self.__getBadMovesForAction(pos, moves_dir[action])
        possible_moves = [a] + b
        for move, probability in zip(possible_moves, [.8, .1, .1]):
            value += probability * (self.__getStateChangeReward(move) + gamma * V_i[move])
        return value

    def trainPolicy(self):
        V_i = {}
        for key in self.__map:
            V_i[key] = self.__getStateChangeReward(key) if self.__getStateChangeReward(key) != self.__moveR else 0

        change = True
        count = 0

        while change and count < self.__steps:
            V_i_prime = {}
            count += 1
            change = False
            for x in range(self.__maxX):
                for y in range(self.__maxY):
                    if self.__map[(x, y)] == '#':
                        V_i_prime[(x, y)] = 0
                        self.__policy[(x, y)] = -1
                        continue
                    if self.__map[(x, y)] == 'G':
                        V_i_prime[(x, y)] = V_i[(x, y)]
                        self.__policy[(x, y)] = 0
                        continue
                    d = {}
                    for a in range(1, 5):
                        d[a] = self.value_iteration((x, y), a, V_i)
                    max_key = max(d, key=d.get)
                    self.__policy[(x, y)] = max(d, key=d.get)   # max(d.iteritems(), key=operator.itemgetter(1))[0]
                    V_i_prime[(x, y)] = d[max_key]
                    if V_i[(x, y)] != V_i_prime[(x, y)]:
                        change = True

            for key in V_i_prime:
                V_i[key] = V_i_prime[key]

    # returns new position according to the direction of choosen action,
    # may return the same position if the target is a wall
    def __newPosition(self, pos, action):
        if action == Actions.Up:
            newPos = (pos[0], pos[1] - 1)
        elif action == Actions.Down:
            newPos = (pos[0], pos[1] + 1)
        elif action == Actions.Left:
            newPos = (pos[0] - 1, pos[1])
        else:
            newPos = (pos[0] + 1, pos[1])

        if self.__map[newPos] == '#':
            return pos
        else:
            return newPos

    # returns list of two position which can be reached in case of failure of the selected action
    def __getBadMovesForAction(self, pos, action):
        if action == Actions.Up:
            return [self.__newPosition(pos, Actions.Left), self.__newPosition(pos, Actions.Right)]
        elif action == Actions.Down:
            return [self.__newPosition(pos, Actions.Left), self.__newPosition(pos, Actions.Right)]
        elif action == Actions.Right:
            return [self.__newPosition(pos, Actions.Up), self.__newPosition(pos, Actions.Down)]
        else:
            return [self.__newPosition(pos, Actions.Up), self.__newPosition(pos, Actions.Down)]

    # returns reward for moving the selected position
    def __getStateChangeReward(self, posTo):
        if self.__map[posTo] == ' ':
            return self.__moveR
        elif self.__map[posTo] == 'G':
            if posTo in self.__golds:
                return self.__golds[posTo]
            else:
                return self.__moveR
        elif self.__map[posTo] == 'O':
            return self.__deathR
        else:
            return 0

    def findTreasures(self):
        pos = (self.__startX, self.__startY)
        steps = [pos]

        stepsCount = 0

        while stepsCount < self.__steps:
            stepsCount += 1

            action = self.__getPolicyAction(pos)
            pos = self.__invokeAction(pos, action)
            steps.append(pos)

            if pos in self.__map and (self.__map[pos] == 'O' or self.__map[pos] == 'G'):
                break

        return steps

    def __getPolicyAction(self, pos):
        if pos in self.__policy:
            return self.__policy[pos]
        else:
            return Actions.Up

    # performs action invokation from current position, will return new position
    def __invokeAction(self, pos, action):
        goodPos = self.__newPosition(pos, moves_dir[action])
        badPositions = self.__getBadMovesForAction(pos, action)

        p = random.uniform(0, 1)

        if p < 0.8:
            return goodPos
        elif p >= 0.8 and p < 0.9:
            return badPositions[0]
        else:
            return badPositions[1]


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("Map file need to be specified!")
    #     print("Example: python3 " + sys.argv[0] + " world1.txt")
    #     sys.exit(1)
    w = world()
    # w.load(sys.argv[1])
    w.load('mapa1.txt')
    w.trainPolicy()
    steps = w.findTreasures()
    # simulator.simulate(sys.argv[1], steps)
    simulator.simulate('mapa1.txt', steps)
