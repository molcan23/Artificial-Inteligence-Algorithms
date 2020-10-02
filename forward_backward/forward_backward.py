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
    forward = []

    best_state_for_w0 = None
    for w1 in weather:
        state = {}
        for w2 in weather:
            state[w2] = .25 * TRANSITIONS[w1][w2] * OBSERVATIONS[w2][observation[0]]
            if best_state_for_w0 is None or \
                    max(state, key=state.get) > max(best_state_for_w0, key=best_state_for_w0.get):
                best_state_for_w0 = state
    forward.append(best_state_for_w0)

    for o in observation[1:]:
        prev_state = max(forward[-1], key=forward[-1].get)

        prev_probability = forward[-1][prev_state]
        state = {}
        for w in weather:
            state[w] = TRANSITIONS[prev_state][w] * prev_probability * OBSERVATIONS[w][o]
        forward.append(state)

    return forward


def forward_backward(observations):
    forward = []
    best_backward = []
    p_forward = 0

    for end_weather in weather:
        # forward
        forward = []
        last = {}
        for w in weather:
            last_sum = .25
            last[w] = OBSERVATIONS[w][observations[0]] * last_sum

        forward.append(last)
        previous = last

        for observation_i in observations[1:]:
            last = {}
            for w in weather:
                last_sum = sum(previous[k]*TRANSITIONS[k][w] for k in weather)
                last[w] = OBSERVATIONS[w][observation_i] * last_sum

            forward.append(last)
            previous = last

        p_forward = sum(last[k] * TRANSITIONS[k][end_weather] for k in weather)

        # backward
        max_p = 0
        best_backward = None

        backward = []
        b_curr = {}
        for w in weather:
            b_curr[w] = TRANSITIONS[w][end_weather]

        backward.insert(0, b_curr)
        b_prev = b_curr

        for o in reversed(observations[:-1]):
            b_curr = {}
            for w1 in weather:
                b_curr[w1] = sum(TRANSITIONS[w1][w2] * OBSERVATIONS[w2][o] * b_prev[w2] for w2 in weather)

            backward.insert(0, b_curr)
            b_prev = b_curr

        start = backward[0]
        p_ = start[max(start, key=start.get)]
        if p_ > max_p:
            max_p = p_
            best_backward = backward

    posterior = []
    for i in range(len(observations)):
        posterior.append({w: forward[i][w] * best_backward[i][w] / p_forward for w in weather})

    return forward, best_backward, posterior


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
        for day in wet_seq:
            prob_line.append(day[w])
        plt.plot(prob_line, label=w)

    plt.legend()
    plt.title(title)
    plt.show()


def all_for_task(sequence, title):
    forward, backward, pos = forward_backward(sequence)
    print('Forward for', title, ':', most_probable(forward))
    print('Backward for', title, ':', most_probable(backward))
    print('Posterior for', title, ':', most_probable(pos))
    forward = scale_viterbi(forward)
    backward = scale_viterbi(backward)
    pos = scale_viterbi(pos)
    plot_probabilities(forward, title)
    plot_probabilities(backward, title)
    plot_probabilities(pos, title)


if __name__ == '__main__':
    all_for_task(sequence1, 'sequnce 1')
    all_for_task(sequence2, 'sequnce 2')
    all_for_task(sequence3, 'sequnce 3')
