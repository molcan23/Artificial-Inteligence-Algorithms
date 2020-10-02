import matplotlib.pyplot as plt

weather = ['snowfall', 'rain', 'moisture', 'dry']

SNOWFALL = {0: .7, 1: .25, 2: .05}
RAIN = {0: .15, 1: .75, 2: .1}
MOISTURE = {0: .05, 1: .65, 2: .3}
DRY = {0: .1, 1: .1, 2: .8}

OBSERVATIONS = {'snowfall': {0: .7, 1: .25, 2: .05},
                'rain': {0: .15, 1: .75, 2: .1},
                'moisture': {0: .05, 1: .65, 2: .3},
                'dry': {0: .1, 1: .1, 2: .8}}

TRANSITIONS = {'snowfall': {'snowfall': .4, 'rain': .2, 'moisture': .3, 'dry': .1},
               'rain': {'snowfall': .1, 'rain': .15, 'moisture': .67, 'dry': .08},
               'moisture': {'snowfall': .15, 'rain': .25, 'moisture': .25, 'dry': .35},
               'dry': {'snowfall': .05, 'rain': .45, 'moisture': 0, 'dry': .5}}

sequence1 = [0, 0, 0, 1, 0, 0, 0, 1, 1, 2, 2, 1, 2]
sequence2 = [2, 2, 2, 1, 1, 2, 2, 2]
sequence3 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 2, 2, 2, 1]


def viterbi(observation):
    weather_seq = []

    best_state_for_w0 = None
    # best_state_for_w0 = {'snowfall': 0, 'rain': 0, 'moisture': 0, 'dry': 0}
    for w1 in weather:
        state = {}
        for w2 in weather:
            state[w2] = .25 * TRANSITIONS[w1][w2] * OBSERVATIONS[w2][observation[0]]
            if best_state_for_w0 is None or \
                    max(state, key=state.get) > max(best_state_for_w0, key=best_state_for_w0.get):
                best_state_for_w0 = state
    weather_seq.append(best_state_for_w0)

    for o in observation[1:]:
        prev_state = max(weather_seq[-1], key=weather_seq[-1].get)

        prev_probability = weather_seq[-1][prev_state]
        state = {}
        for w in weather:
            state[w] = TRANSITIONS[prev_state][w] * prev_probability * OBSERVATIONS[w][o]
        weather_seq.append(state)

    return weather_seq


def most_probable(seq):
    probable_weather = []
    for o in seq:
        probable_weather.append(max(o, key=o.get))
    return probable_weather


def scale_viterbi(seq):
    for day in seq:
        den = sum([day[w] for w in weather])
        for w in weather:
            day[w] = day[w] / den
    return seq


def plot_probabilities(wet_seq, title):
    for w in weather:
        prob_line = []
        # print(wet_seq)
        for day in wet_seq:
            # print(day)
            prob_line.append(day[w])
        plt.plot(prob_line, label=w)

    plt.legend()
    plt.title(title)
    plt.show()


def all_for_task(sequence, title):
    weather_seq = viterbi(sequence)
    print(weather_seq[0])
    print('Best weather sequence for', title, ':', most_probable(weather_seq))
    weather_seq = scale_viterbi(weather_seq)
    plot_probabilities(weather_seq, title)


if __name__ == '__main__':
    all_for_task(sequence1, 'sequnce 1')
    all_for_task(sequence2, 'sequnce 2')
    all_for_task(sequence3, 'sequnce 3')
