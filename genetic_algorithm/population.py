import copy
import random

import constants as cs
from virtual_machine import VirtualMachine


class Individual:

    def __init__(self, program=[]):
        self.program = program

    def get_program(self):
        return copy.copy(self.program)


class GeneticAlgorithm:

    #počet jedincov programu, typ selekcie, (prípadne typ kríženia) pravdepodobnosť mutácie
    # (každého použitého typu), elitarizmus (áno/nie, prípadne počet), počet generácií
    # na koniec/prerušenie, ak nenájdem všetky poklady skôr

    def __init__(self, number_of_individuals, selection, crossing, p_mutation, elitarism, number_of_generations):
        """

        :param number_of_individuals: int
        :param selection: function
        :param crossing:
        :param p_mutation: array?  # FIXME
        :param elitarism:
        :param number_of_generations:
        """
        self.number_of_individuals = number_of_individuals
        self.selection = selection
        self.crossing = crossing
        self.p_mutation = p_mutation
        self.elitarism = elitarism
        self.number_of_generations = number_of_generations
        self.individuals = []
        self.virtual_machine = VirtualMachine()

    def create_first_generation(self):
        # RANDOM
        for _ in range(self.number_of_individuals):
            self.individuals.append(Individual([{'program': random.randint(0, 255), 'fitness': 0}
                                                for _ in range(cs.INDIVIDUAL_MEMORY)]))

    def test_generation(self):

        for ind in self.individuals:
            ind['fitness'] = self.virtual_machine.evaluate(ind['program'])

        return

