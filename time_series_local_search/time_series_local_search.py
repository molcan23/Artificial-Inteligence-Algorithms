import matplotlib.pyplot as plt
import numpy as np
import random


def load_time_series():
    time_series = []
    with open("data.txt", "r") as input_file:
        lines = input_file.readlines()
        for line in lines:
            time_series.append(float(line))
    return np.array(time_series)


def mean_square_error(series1, series2):
    return np.mean(np.sum((series1 - series2) ** 2))


def generate_series(mi, t_0):
    series = [t_0]
    for _ in range(500):
        series.append(mi * series[-1] * (1 - series[-1]))
    return np.array(series[1:])


def random_neighbour(x, interval, fraction):
    amplitude = (max(interval) - min(interval)) * (1 - fraction)
    a, b = interval
    new_i = max(a, x - amplitude), min(b, x + amplitude)
    x = random.uniform(new_i[0], new_i[1])
    return x


def annealing(original_series, maxsteps=100000):

    mi = random.uniform(0, 4)
    t_0 = random.random()
    series = generate_series(mi, t_0)
    cost = mean_square_error(original_series, series)
    mis, t_0s, costs = [mi], [t_0],  [cost]
    mix= []

    max_mi = 0
    min_mi = float('inf')
    for step in range(1, maxsteps):
        fraction = step / float(maxsteps)
        T = max(0.01, min(1, 1 - fraction))
        new_mi = random_neighbour(mi, (0, 4), fraction)
        new_t_0 = random_neighbour(t_0, (0, 1), fraction)
        series = generate_series(mi, t_0)
        new_cost = mean_square_error(original_series, series)

        p = 1 if new_cost < cost else np.exp(- (new_cost - cost) / T)

        mix.append(new_mi)

        max_mi = new_mi if new_mi > max_mi else max_mi
        min_mi = new_mi if new_mi < min_mi else min_mi
        if p >= random.random():
            mi, t_0, cost = new_mi, new_t_0, new_cost
            mis.append(mi)
            t_0s.append(t_0)
            costs.append(new_cost)

    plt.plot(mix)
    plt.show()

    return mi, t_0, cost, mis, t_0s, costs


if __name__ == '__main__':
    ts = load_time_series()

    series = []
    errs = []
    best_err = float('inf')
    best_mi = best_t_0 = None

    mi_up, mi_down = 4, 0
    t0_up, t0_down = 1, 0
    koef = [.2, .1, .05, .01, 0.001]
    for i in range(4):
        for _ in range(2000):
            mi = np.round(random.uniform(mi_down, mi_up), 4)  # random.random() * 4
            t_0 = np.round(random.uniform(t0_down, t0_up), 4)
            series = generate_series(mi, t_0)
            err = mean_square_error(series, ts)
            errs.append(err)
            if err < best_err:
                best_err = err
                best_mi = np.round(mi, 3)
                best_t_0 = np.round(t_0, 3)
        mi_up, mi_down = best_mi + koef[i], best_mi - koef[i]
        t0_up, t0_down = best_t_0 + koef[i], best_t_0 - koef[i]

    print(best_mi, best_t_0)

    my_series = generate_series(best_mi, best_t_0)

    plt.plot(ts[:100], label='original')
    plt.plot(my_series[:100], label='generated')
    plt.plot(np.array(ts - my_series)[:100], label='noise')
    plt.title('jedna cez druhu, mi = ' + str(best_mi) + ', t_0 = ' + str(best_t_0))
    plt.legend()
    plt.show()

    plt.plot(ts[:100], label='original')
    plt.plot(my_series[:100] - 0.3, label='generated shifted')
    plt.plot(np.array(ts - my_series)[:100], label='noise')
    plt.title('posun pre porovnanie, mi = ' + str(best_mi) + ', t_0 = ' + str(best_t_0))
    plt.show()

    # prvotne som nakodil to vyssie, tak som sa chcel pustit do niecoho, co som nevymyslel len ja z hlavy
    # a nasiel som annealing, ktory mi prisiel celkom podobny mojmu, ale nevedel som to spojazdnit
    # mam pocit, ze problem je pri vyberani suseda, ale nijakovsky to neslo

    # mi, t_0, cost, mis, t_0s, costs = annealing(ts)
    # print(cost, mi, t_0)
    #
    # plt.plot(costs)
    # plt.show()
    #
    # plt.plot(mis)
    # plt.show()
    #
    # plt.plot(t_0s)
    # plt.show()
