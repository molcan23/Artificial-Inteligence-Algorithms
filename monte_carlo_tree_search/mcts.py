from random import choice
from collections import defaultdict
import math


class MonteCarloTreeSearch:

    def __init__(self, weight=1):
        """Intuitivne si vo win/all budeme pamatat pocty viehier/vsetkych pokusov v danej pozicii pre konkretny
         postup hrou. Weight obsahuje vahu pre ucb a children je slovnik, ktory pre kazdeho syna obsahuje
          vsetky moznosti ako urobit dalsi tah (ktory je este mozne urobit - nebol urobeny pred tym)."""

        self.win = defaultdict(int)
        self.all = defaultdict(int)
        self.weight = weight
        self.children = {}

    def selection(self, configuration):
        """Vyberie toho syna, ktory ma najvacsi pomer vitazstiev k vsetkym a este nebol navstiveny
        (kedze v kazdom tahu mozeme zaskrtnut kazde policko, ktore este nie je zabrane).
         Chceme si byt zaroven isty, ze kazdy syn ma spravodlivu sancu byt vybrany - snazime sa vyberat
          optimalneho syna az po list, na spravny vyber sa pouziva UCBound.
          Vytvarame postupnost walk, pretoze pre expansion nam staci len vystupna konfiguracia tejto metody,
          pre backpropagaciu potrebujeme celu postupnost konfiguracii"""

        walk = []
        while True:

            walk.append(configuration)
            if configuration not in self.children or not self.children[configuration]:
                return walk

            not_visited = []
            for x in self.children[configuration]:
                if x not in self.children.keys():
                    not_visited.append(x)

            if not_visited:
                walk.append(not_visited.pop())
                return walk
            configuration = self.ucb_function(configuration)

    def expansion(self, configuration):
        """Rozsirime strom pridanim nasledujucej konfiguracie hry (ktora vznikla z danej "otcovskej" konfiguracie)"""

        if configuration not in self.children:
            self.children[configuration] = configuration.find_children()
        else:
            return

    @staticmethod
    def simulation(configuration):
        """Nahodne simulujeme hru az po koniec - list stromu."""

        on_move = True
        while True:
            if configuration.is_terminal():
                return 1 - configuration.score() if on_move else configuration.score()
            configuration = configuration.find_random_child()
            on_move = not on_move

    def back_propagation(self, walk, score):
        """Po dosiahnuti konca hry, zistime kto vyhral a splhame ku korenu pricom updatujeme skore
         (pre kazdu konfiguraciu, ktorou sme prechadzali)."""

        for configuration in walk:
            score = 1 - score
            self.all[configuration] += 1
            self.win[configuration] += score

    def find_best(self, configuration):
        """Najdeme moznost s najlepsim pomerom vyhier/celkovy pocet simulacii, s ktorou budeme pokracovat."""

        if configuration not in self.children:
            return configuration.find_random_child()

        best_board_win_ratio = 0
        best_configuration = None
        for x in self.children[configuration]:
            ratio = self.win[x] / self.all[x]
            best_configuration = x if ratio > best_board_win_ratio else best_configuration

        return best_configuration

    def mcst_iteration(self, configuration):
        """Jedna iteracia MCST - vsetky 4 kroky."""

        walk = self.selection(configuration)
        self.expansion(walk[-1])
        score = self.simulation(walk[-1])
        self.back_propagation(walk, score)

    def ucb_function(self, configuration):
        """Pre vsetkych synov (teda mozne tahy) vyberie podla Upper Confidence Bound najlepsieho -
         maximalneho v hodnote ucb."""

        def ucb(n):
            return self.win[n] / self.all[n] + self.weight * math.sqrt(math.log(self.all[configuration]) / self.all[n])
        return max(self.children[configuration], key=ucb)


class TicTacToeBoard:

    def __init__(self, tup, turn, winner, terminal):
        self.tup = tup
        self.turn = turn
        self.winner = winner
        self.terminal = terminal

    def find_children(self):
        if self.terminal:  # If the game is finished then no moves can be made
            return set()
        return {
            self.make_move(i) for i, value in enumerate(self.tup) if value is None
        }

    def find_random_child(self):
        if self.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = [i for i, value in enumerate(self.tup) if value is None]
        return self.make_move(choice(empty_spots))

    def score(self):
        if not self.terminal:
            raise RuntimeError(f"score called on nonterminal board {self}")
        if self.winner is self.turn:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"score called on unreachable board {self}")
        if self.turn is (not self.winner):
            return 0
        if self.winner is None:
            return 0.5
        raise RuntimeError(f"board has unknown winner type {self.winner}")

    def is_terminal(self):
        return self.terminal

    def make_move(self, index):
        tup = self.tup[:index] + (self.turn,) + self.tup[index + 1:]
        turn = not self.turn
        winner = _find_winner(tup)
        is_terminal = (winner is not None) or not any(v is None for v in tup)
        return TicTacToeBoard(tup, turn, winner, is_terminal)

    def to_pretty_string(self):
        def output_function():
            return lambda v: ("X" if v is True else ("O" if v is False else " "))
        to_char = output_function()
        rows = [
            [to_char(self.tup[3 * row + col]) for col in range(3)] for row in range(3)
        ]
        return (
            "\n  1 2 3\n"
            + "\n".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))
            + "\n"
        )


def play_game():
    tree1 = MonteCarloTreeSearch()
    tree2 = MonteCarloTreeSearch()
    board = new_tic_tac_toe_board()
    print(board.to_pretty_string())
    while True:
        for _ in range(50):
            tree1.mcst_iteration(board)
        board = tree1.find_best(board)
        print(board.to_pretty_string())
        if board.terminal:
            res = "First Monte Carlo Search Tree AI won." if _find_winner(board.tup) == True else \
                "DRAW"
            print(res)
            break

        for _ in range(50):
            tree2.mcst_iteration(board)
        board = tree2.find_best(board)
        print(board.to_pretty_string())
        if board.terminal:
            res = "Second Monte Carlo Search Tree AI won." if _find_winner(board.tup) == False else \
                "DRAW"
            print(res)
            break


def _winning_combos():
    for start in range(0, 9, 3):
        yield (start, start + 1, start + 2)
    for start in range(3):
        yield (start, start + 3, start + 6)
    yield (0, 4, 8)
    yield (2, 4, 6)


def _find_winner(tup):
    """Returns None if no winner, True if X wins, False if O wins"""
    for i1, i2, i3 in _winning_combos():
        v1, v2, v3 = tup[i1], tup[i2], tup[i3]
        if False is v1 is v2 is v3:
            return False
        if True is v1 is v2 is v3:
            return True
    return None


def new_tic_tac_toe_board():
    return TicTacToeBoard(tup=(None,) * 9, turn=True, winner=None, terminal=False)


if __name__ == "__main__":
    play_game()
