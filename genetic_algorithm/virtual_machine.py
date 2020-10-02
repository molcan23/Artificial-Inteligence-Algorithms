import copy

STEPS = 500


class VirtualMachine:

    def __init__(self, file_name="game_board.txt"):
        with open(file_name, "r") as board:
            # 1. riadok rozmery
            # 2. riadok start
            # dalsie: polohy pokladov
            lines = board.readlines()
            n, m = lines[0].split(' ')
            self.game_board = []
            for _ in range(int(n)):
                self.game_board.append([0 for _ in range(int(m))])

            self.n, self.m = int(n), int(m)
            self.s_x, self.s_y = lines[1].split(' ')
            self.a_x, self.a_y = int(self.s_x), int(self.s_y)

            for i in range(2, len(lines)):
                x, y = lines[i].split(' ')
                self.game_board[int(x)][int(y)] = 1

            self.original_game_board = copy.copy(self.game_board)
            self.out_of_bounds_penalty = self.number_of_treasures = len(lines) - 2
            self.collected_treasures = 0
            self.address = 0
            self.number_of_steps = 0
            self.program = []
            self.treasure_hunter_steps = 0

    def reset(self):
        self.game_board = copy.copy(self.original_game_board)
        self.collected_treasures = 0
        self.address = 0
        self.number_of_steps = 0
        self.program = []
        self.treasure_hunter_steps = 0

    def evaluate(self, program):
        self.program = program

        while self.number_of_steps < 500 or self.collected_treasures == self.number_of_treasures:
            self.number_of_steps += 1
            actual_instruction = "{0:b}".format(program[self.address])
            instruction = actual_instruction[0:2]
            action = actual_instruction[-2:]
            address = actual_instruction[2:]
            in_bounds = self.execute_action(action)
            if not in_bounds:
                return None
            # incrementujeme tu, pretoze mozeme aj skakat (pri instrukcii)
            self.address += 1 % 256
            self.execute_instruction(instruction, address)

        return self.fitness()

    def execute_instruction(self, instruction, address):
        if instruction == '00':
            address = int(address, 2)
            self.increment(address)
        elif instruction == '01':
            address = int(address, 2)
            self.decrement(address)
        elif instruction == '10':
            address = int(address, 2)
            self.jump(address)
        elif instruction == '11':
            self.print_out()
        return

    # FIXME instrukcie idu jedna po druhej ale kroky huntera su len ak je "print_out"???
    #  ak ano tak prerobit
    def execute_action(self, action):
        self.treasure_hunter_steps += 1
        # HORE
        if action == '00':
            self.a_x -= 1
            if self.a_x < 0:
                return False
        # DOLE
        elif action == '01':
            self.a_x += 1
            if self.n <= self.a_x:
                return False
        # PRAVO
        elif action == '10':
            self.a_y += 1
            if self.n <= self.a_y:
                return False
        # LAVO
        elif action == '11':
            self.a_y -= 1
            if self.a_y < 0:
                return False

        if self.game_board[self.a_x][self.a_y] == 1:
            self.collected_treasures += 1
            self.game_board[self.a_x][self.a_y] = 0

        return True

    def increment(self, address_):
        self.program[address_] += 1 % 256

    def decrement(self, address_):
        self.program[address_] -= 1 % 256

    def jump(self, address_):
        address = int(address_, 2)
        self.address = address_

    def print_out(self):
        sequence = ''
        for i in self.program:
            direction = "{0: b}".format(i)[-2:]
            # HORE
            if direction == '00':
                sequence += ' H'
            # DOLE
            elif direction == '01':
                sequence += ' D'
            # PRAVO
            elif direction == '10':
                sequence += ' P'
            # LAVO
            elif direction == '11':
                sequence += ' L'
        print(sequence)

    def fitness(self):
        # FIXME ako presne bude fitness vyzerat?
        score = self.collected_treasures - self.number_of_steps * 0.001 + self.treasure_hunter_steps * 0.001
        if not self.collected_treasures == self.number_of_treasures and not self.treasure_hunter_steps == STEPS:
            score -= self.out_of_bounds_penalty
        return score


if __name__ == '__main__':
    h = VirtualMachine("game_board.txt")
