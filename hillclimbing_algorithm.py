import numpy as np
from random import randrange

NUMBER_OF_VECTORS = 10

def fitness(x, y, cor, moves):
    treasures = 0
    for m in moves:

        if m == 0:
            x = (x-1) % NUMBER_OF_VECTORS
            if (x, y) in cor:
                treasures += 1
                cor.remove((x,y))
                
        if m == 1:
            y = (y-1) % NUMBER_OF_VECTORS
            if (x, y) in cor:
                treasures += 1
                cor.remove((x,y))

        if m == 2:
            x = (x+1) % NUMBER_OF_VECTORS
            if (x, y) in cor:
                treasures += 1
                cor.remove((x,y))

        if m == 3:
            y = (y+1) % NUMBER_OF_VECTORS
            if (x, y) in cor:
                treasures += 1
                cor.remove((x,y))

    return treasures


def find_best_set_of_moves(moves):
    fit_score = []

    for m in moves:
        fit_score.append(fitness(x1, y1, cor.copy(), m))
        
    return max(fit_score, key = lambda k: fit_score[k]), max(fit_score)


def mod_best(best_moves_yet):
    new_moves = []
    for _ in range(NUMBER_OF_VECTORS):
        current = best_moves_yet.copy()
        pos = randrange(20)
        pos_val = current[pos]
        shift = -1
        while True:
            shift = randrange(4)
            if pos_val != shift:
                current[pos] = shift
                break
        new_moves.append(current)

    return new_moves        
             



    
x1, y1 = input().split()
x1 = int(x1)
y1 = int(y1)
number_of_treasures = int(input())

cor = []
for _ in range(number_of_treasures):
    x, y = input().split()
    cor.append((int(x), int(y)))


moves = []

for _ in range(NUMBER_OF_VECTORS):
    moves.append(np.random.randint(4, size=20))

change = True
    
while change:
    change = False
    for i in range(NUMBER_OF_VECTORS):
        os = fitness(x1, y1, cor.copy(), moves[i])
        new_moves = mod_best(moves[i])
        index, fs = find_best_set_of_moves(new_moves)
        ns = fitness(x1, y1, cor.copy(), new_moves[index])
        if os < ns:
            moves[i] = new_moves[index]
            change = True
        
    if not change:
        break


index, fs = find_best_set_of_moves(moves)
moves = mod_best(moves[index])
print(fs, fs, moves[index])

