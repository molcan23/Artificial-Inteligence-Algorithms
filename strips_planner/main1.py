import pyddl
from pyddl import Domain, Problem, Action, neg, planner
import sys
import simulator

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
                    self.__totalGold+=1
                if char == '@':
                    self.__startX = x
                    self.__startY = y
                x+=1
            y+=1

    def getProblem(self):
        
        init = list() #list predikatov

        
        #list pozicii a co sa tam nachadza
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if(self.__map[(i,j)] == '#'):
                   init.append(["at",str(i),str(j), '#'])
                elif(self.__map[(i,j)] == 'A'):
                    init.append(["at",str(i),str(j), 'A'])
                    init.append(["at",str(i),str(j), "blank"])
                elif(self.__map[(i,j)] == 'W'):
                    init.append(["at",str(i),str(j), 'W'])
                elif(self.__map[(i,j)] == 'g'):
                    init.append(["at",str(i),str(j), 'g'])
                    init.append(["at",str(i),str(j), "blank"])
                elif(self.__map[(i,j)] == ' '):
                    init.append(["at",str(i),str(j), "blank"])
                elif(self.__map[(i,j)] == '@'): #startovna pozicia
                    init.append(["at",str(i),str(j), '@'])


        #inicializacia poctu zlata a sipov
        init.append(['=', ('arrow',), 0])
        init.append(['=', ('gold',), 0])

        #decrements
        for i in range(max(self.__maxX, self.__maxY)):
            init.append(["inc",  str(i), str(i+1)])
            init.append(["dec", str(i+1), str(i)])


	#    goal = list()
	#    goal.append(['at', str(self.__startX), str(self.__startY), '@'])
	#    goal.append(['=', ('gold',), self.__totalGold])

        # goal = list((['at', str(self.__startX), str(self.__startY), '@'],['=', ('gold',), self.__totalGold]))
        goal = list()
        goal.append(('at', str(self.__startX), str(self.__startY), '@'))
        goal.append(('=', ('gold',), self.__totalGold))



        positions = list()
        #lst stringov, vsetkych moznych pozicii (iba jednu poziciu,
        #teda max z Y a X)
        for i in range(max(self.__maxX, self.__maxY)):
            positions.append(["position", str(i)])

        #treba si pamatat poziciu lovca - zadefinovat predikat kde prave stoji

        print(init)
        print(goal)


        domain = pyddl.Domain((
             Action(
                'move-up', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('dec', 'by', 'py'),
                    ('at', 'px', 'by', 'blank'),
                ),
                effects=(
                     neg(('at', 'px', 'by', 'blank')),
                    neg(('at', 'px', 'py','@')),
                    ('at', 'px', 'py', 'blank'),
                    ('at', 'px', 'by', '@'),
                ),
            ),
            Action(
                'move-down', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'by'),
                ),
                preconditions=(
                    ('inc', 'by', 'py'),
                    ('at', 'px', 'py', 'blank'),
                ),
                effects=(
                    neg(('at', 'px', 'by', "blank")),
                    neg(('at', 'px', 'py', '@')),
                    ('at', 'px', 'py', "blank"),
                    ('at', 'px', 'by', '@'),
                ),
            ),
            Action(
                'move-left', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('dec', 'bx', 'px'),
                    ('at', 'px', 'py', "blank"),
                ),
                effects=(
                    neg(('at', 'bx', 'py', "blank")),
                    neg(('at', 'px', 'py', '@')),
                    ('at', 'px', 'py', "blank"),
                    ('at', 'bx', 'py', '@'),
                ),
            ),
            Action(
                'move-right', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('inc', 'bx', 'px'),
                    ('at', 'px', 'py', "blank"),
                ),
                effects=(
                    neg(('at', 'bx', 'py', "blank")),
                    neg(('at', 'px', 'py', '@')),
                    ('at', 'px', 'py', "blank"),
                    ('at', 'bx', 'py', '@'),
                ),
            ),
            Action(
                'take-gold', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                ),
                preconditions=(
                    ('at' 'px', 'py', 'g'),
                ),
                effects=(
                    neg(('at', 'px', 'py','g')),
                    ('+=',("gold",), 1)
                ),
            ),
            Action(
                'take-arrow', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                ),
                preconditions=(
                    ('at', 'px', 'py', 'A'),
                ),
                effects=(
                    neg(('at', 'px', 'py','A')),
                    ('+=',("arrow",), 1)
                ),
            ),
            Action(
                'shoot-wumpus-down', #todo
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('inc', 'bx', 'px'),
                    ('at', 'bx', 'py', 'W'),
                    ('at', 'px', 'py', '@'),
                    ('>', ("arrow",), 0),
                    
                ),
                effects=(
                    neg(('at', 'bx', 'py','W')),
                    
                    ('-=', ("arrow",), 1),
                    ('at', 'bx', 'py', "blank"),
                ),
            ),
            Action(
                'shoot-wumpus-left', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('inc', 'bx', 'px'),
                    ('at', 'bx', 'py', 'W'),
                    ('at', 'px', 'py', '@'),
                    ('>', ("arrow",), 0),
                ),
                effects=(
                    neg(('at', 'px', 'py','W')),
                    ('-=', ("arrow",), 1),
                    ('at', 'bx', 'py', "blank"),
                ),
            ),
            Action(
                'shoot-wumpus-up', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('inc', 'bx', 'px'),
                    ('at', 'bx', 'py', 'W'),
                    ('at', 'px', 'py', '@'),
                    ('>', ("arrow",), 0),
                ),
                effects=(
                    neg(('at', 'bx', 'py', 'W')),
                    ('-=', ("arrow",), 1),
                    ('at', 'bx', 'py', "blank"),
                ),
            ),
            Action(
                'shoot-wumpus-down', #done
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'bx'),
                ),
                preconditions=(
                    ('inc', 'bx', 'px'),
                    ('at', 'bx', 'py', 'W'),
                    ('at', 'px', 'py', '@'),
                    ('>', ("arrow",), 0),
                ),
                effects=(
                    neg(('at', 'bx', 'py', 'W')),
                    ('-=', ("arrow",), 1),
                    ('at', 'bx', 'py', "blank"),
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
    
    #if len(sys.argv) < 2:
    #    print("Map file needs to be specified!")
    #    print("Example: python3 " + sys.argv[0] + " world1.txt")
    #    sys.exit(1)
    w = world()
    #w.load(sys.argv[1])
    w.load("world1.txt")
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
        #simulator.simulate(sys.argv[1], sys.argv[1] + ".solution")
        simulator.simulate("world1.txt", "world1.txt" + ".solution")

