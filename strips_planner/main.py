import pyddl
import sys
import simulator
from pyddl import Domain, Problem, Action, neg, planner


class world:
    __map = {}
    __totalGold = 0
    __maxX = 0
    __maxY = 0
    __startX = 0
    __startY = 0

    def load(self, file):
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
                    self.__totalGold += 1
                if char == '@':
                    self.__startX = x
                    self.__startY = y
                x += 1
            y += 1

    def getProblem(self):
        init = list()
        init.append(('=', ('arrows',), 0))
        init.append(('=', ('gold',), 0))
        init.append(('hunter', str(self.__startX), str(self.__startY)))
        a = max(self.__maxX, self.__maxY)

        for i in range(a):
            init.append(('dec', str(a - i), str(a - i - 1)))

        for i in range(self.__maxX+1):
            for j in range(self.__maxY+1):
                x = ()
                if self.__map[(i, j)] == '@':
                    x = ('at', '@', str(i), str(j))
                if self.__map[(i, j)] == 'W':
                    x = ('at', 'W', str(i), str(j))
                if self.__map[(i, j)] == 'A':
                    init.append(('at', 'blank', str(i), str(j)))
                    x = ('at', 'A', str(i), str(j))
                if self.__map[(i, j)] == 'g':
                    init.append(('at', 'blank', str(i), str(j)))
                    x = ('at', 'g', str(i), str(j))
                if self.__map[(i, j)] == '#':
                    x = ('at', '#', str(i), str(j))
                if self.__map[(i, j)] == ' ':
                    x = ('at', 'blank', str(i), str(j))

                init.append(x)

        goal = list()
        goal.append(('hunter', str(self.__startX), str(self.__startY)))
        goal.append(('=', ('gold',), self.__totalGold))

        positions = list()
        for x in range(a+1):
            positions.append(str(x))

        domain = pyddl.Domain((
            Action(
                'move-down',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('dec', 'by', 'py'),
                    ('at', 'blank', 'px', 'by'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'blank', 'px', 'by')),
                    neg(('hunter', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('hunter', 'px', 'by'),
                ),
            ),
            Action(
                'move-up',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('dec', 'py', 'by'),
                    ('at', 'blank', 'px', 'by'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'blank', 'px', 'by')),
                    neg(('hunter', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('hunter', 'px', 'by'),
                ),
            ),
            Action(
                'move-left',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('dec', 'px', 'bx'),
                    ('at', 'blank', 'bx', 'py'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'blank', 'bx', 'py')),
                    neg(('hunter', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('hunter', 'bx', 'py'),
                ),
            ),
            Action(
                'move-right',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('dec', 'bx', 'px'),
                    ('at', 'blank', 'bx', 'py'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'blank', 'bx', 'py')),
                    neg(('hunter', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('hunter', 'bx', 'py'),
                ),
            ),
            Action(
                'shoot-wumpus-down',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('dec', 'by', 'py'),
                    ('at', 'W', 'px', 'by'),
                    ('>', ('arrows',), 0),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'W', 'px', 'by')),
                    ('at', 'blank', 'px', 'by'),
                    ('-=', ('arrows',), 1)
                ),
            ),
            Action(
                'shoot-wumpus-up',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('dec', 'py', 'by'),
                    ('at', 'W', 'px', 'by'),
                    ('>', ('arrows',), 0),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'W', 'px', 'by')),
                    ('at', 'blank', 'px', 'by'),
                    ('-=', ('arrows',), 1)
                ),
            ),
            Action(
                'shoot-wumpus-right',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('dec', 'bx', 'px'),
                    ('at', 'W', 'bx', 'py'),
                    ('>', ('arrows',), 0),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'W', 'bx', 'py')),
                    ('at', 'blank', 'bx', 'py'),
                    ('-=', ('arrows',), 1)
                ),
            ),
            Action(
                'shoot-wumpus-left',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('dec', 'px', 'bx'),
                    ('at', 'W', 'bx', 'py'),
                    ('>', ('arrows',), 0),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'W', 'bx', 'py')),
                    ('at', 'blank', 'bx', 'py'),
                    ('-=', ('arrows',), 1)
                ),
            ),


            Action(
                'take-gold',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                ),
                preconditions=(
                    ('at', 'g', 'px', 'py'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'g', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('+=', ('gold',), 1)
                ),
            ),
            Action(
                'take-arrow',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                ),
                preconditions=(
                    ('at', 'A', 'px', 'py'),
                    ('hunter', 'px', 'py'),
                ),
                effects=(
                    neg(('at', 'A', 'px', 'py')),
                    ('at', 'blank', 'px', 'py'),
                    ('+=', ('arrows',), 1)
                ),
            ),
        ))

        problem = pyddl.Problem(
            domain,
            {
                'position': tuple(positions),
            },
            init=tuple(init),
            goal=tuple(goal),
        )

        return problem


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Map file need to be specified!")
        print("Example: python3 " + sys.argv[0] + " world1.txt")
        sys.exit(1)
    w = world()
    w.load(sys.argv[1])
    problem = w.getProblem()
    plan = pyddl.planner(problem, verbose=True)
    if plan is None:
        print('Hunter is not able to solve this world!')
    else:
        actions = [action.name for action in plan]
        print(", ".join(actions))
        f = open(sys.argv[1] + ".solution", "w")
        f.write("\n".join(actions))
        f.close()
        input()
        simulator.simulate(sys.argv[1], sys.argv[1] + ".solution")
