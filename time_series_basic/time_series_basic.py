import numpy as np
import matplotlib.pyplot as plt


def load_time_series():
    time_series = []
    with open("data.txt", "r") as input_file:
        lines = input_file.readlines()
        for line in lines[5:-2]:
            line1 = line.split(' ')
            # print(line1)
            time_series.append(float(line1[2][:-1]))
    return np.array(time_series)


def moving_average(time_series, window):
    smoothed_time_series = []
    for i in range(window, len(time_series)):
        smoothed_time_series.append(np.mean(time_series[i - window + 1:i + 1]))
    return np.array(smoothed_time_series)


def centered_moving_average(time_series, window):
    smoothed_time_series = []
    half = int(window / 2)
    for i in range(window - half, len(time_series) - half):
        smoothed_time_series.append(np.mean(time_series[i - half + 1:i + half + 1]))
    return np.array(smoothed_time_series)


def double_moving_average(time_series, window1, window2):
    smoothed_time_series_once = moving_average(time_series, window1)
    smoothed_time_series_twice = moving_average(smoothed_time_series_once, window2)
    return np.array(smoothed_time_series_twice)


def linear_regression(y):
    x = [i for i in range(len(y))]
    denominator = (len(x) * np.sum(np.multiply(x, x)) - np.sum(x) ** 2)
    a = (len(x) * np.sum(np.multiply(x, y)) - np.sum(x) * np.sum(y)) / denominator
    b = (np.sum(np.multiply(x, x)) * np.sum(y) - np.sum(x) * np.sum(np.multiply(x, y))) / denominator
    return a, b


def single_exponential_smoothing(time_series, alpha):
    smoothed = [time_series[0]]
    for i in range(1, len(time_series) - 1):
        smoothed.append(alpha * time_series[i] + (1 - alpha) * smoothed[-1])
    return smoothed


def forecast_single(time_series, smoothed, alpha):
    ts = [i for i in time_series]
    # bootstraping
    boot = ts[-1]

    for _ in range(50):
        # new je to iste
        new = alpha * boot + (1 - alpha) * smoothed[-1]
        smoothed.append(new)
        ts.append(new)

    return ts[len(time_series):]


def double_exponential_smoothing(time_series, alpha, gama):
    smoothed = [time_series[0]]
    b = [(time_series[0] - time_series[-1]) / (len(time_series) - 1)]

    for i in range(2, len(time_series)):
        smoothed.append(alpha * time_series[i] + (1 - alpha) * (smoothed[-1] + b[-1]))
        b.append(gama * (smoothed[-1] - smoothed[-2]) + (1 - gama) * b[-1])

    return smoothed, b


def triple_exponential_smoothing(time_series, alpha, gama, beta):
    smoothed = [time_series[0]]
    b = [(time_series[1] - time_series[-1]) / (len(time_series) - 1)]
    # seasonality
    I = []
    L = None  # malo by sa vypocitat L
    for i in range(1, len(time_series)):
        smoothed.append(alpha * time_series[i] / I[i - L] + (1 - alpha) * (smoothed[-1] + b[-1]))
        b.append(gama * (smoothed[-1] - smoothed[-2]) + (1 - gama) * b[-1])
        I.append(beta * time_series[i] / smoothed[-1] + (1 - beta) * I[- L + 1])
    return smoothed, b, I


def double_exponential_forecast(time_series, smoothed, b):
    ts = [i for i in time_series]
    for i in range(50):
        ts.append(smoothed[-1] + i * b[-1])
    return ts[500:]


def triple_exponential_forecast(time_series, smoothed, b, I, beta, L):
    ts = [i for i in time_series]
    for m in range(50):
        ts.append(beta * (time_series[-1] / smoothed[-1] + (1 - beta) * I[-L + m]))
    return ts[500:]


def mean_square_error(series1, series2):
    return np.mean(np.sum((series1 - series2) ** 2))


def MA_(ts, window_width=15):
    # skusene sirky okna: 50, 30, 25, 20, 15, 10
    plt.plot(ts)
    sts = moving_average(ts, window_width)
    plt.xlabel("window width = " + str(window_width))
    plt.plot(np.array([i for i in range(window_width, len(ts))]), ts[window_width:] - sts)
    plt.title("Moving average")
    plt.show()


def CMA_(ts, window_width=15):
    # skusene sirky okna: 50, 30, 25, 20, 15, 10
    plt.plot(ts)
    cts = centered_moving_average(ts, window_width)
    plt.xlabel("window width = " + str(window_width))
    plt.plot(np.array([i for i in range(int(window_width / 2), len(ts) - int((window_width + 1) / 2))]),
             ts[int(window_width / 2):-int((window_width + 1) / 2)] - cts)
    plt.title("Centered moving average")
    plt.show()


def DMA_(ts, window_width=15):
    # skusene sirky okna: 50, 30, 25, 20, 15, 10
    plt.plot(ts)
    best_MSE = float('inf')
    best_j = 0
    best_series = None

    for j in range(5, 25):
        cts = double_moving_average(ts, window_width, j)
        mse = mean_square_error(ts[window_width + j:], cts)
        if mse < best_MSE:
            best_j = j
            best_MSE = mse
            best_series = cts

    plt.xlabel("window1 = " + str(window_width) + ", window2 = " + str(best_j))
    plt.title("Double moving average")
    plt.plot(np.array(range(window_width + best_j, len(ts))), ts[window_width + best_j:] - best_series)
    plt.show()


def LR_(ts):
    plt.plot(ts)
    best_MSE = float('inf')
    best_j = 0
    best_k = 0
    best_series = None

    a, b = linear_regression(ts)
    for j in range(1, 11):
        for k in range(1, 11):
            lts = (k / 100) * np.array([(j / 100) * (i ** 2) + a * i + b for i in range(len(ts))])
            mse = mean_square_error(ts, lts)
            if mse < best_MSE:
                best_j = j
                best_k = k
                best_MSE = mse
                best_series = lts

    plt.plot(ts - best_series)
    plt.xlabel(
        "a = " + str(round(a, 3)) + ", b = " + str(round(b, 3)) + ", j = " + str(best_j) + ", k = " + str(best_k))
    plt.title("Linear regression")
    plt.show()


def SES_(ts):
    plt.plot(ts)
    best_MSE = float('inf')
    best_i = 0
    best_series = None

    for i in range(1, 11):
        ses = single_exponential_smoothing(ts, i / 10)
        mse = mean_square_error(ts[1:], ses)
        if mse < best_MSE:
            best_i = i / 10
            best_MSE = mse
            best_series = ses

    plt.xlabel("alpha = " + str(best_i))
    forecast = forecast_single(ts, best_series, best_i)
    plt.plot(np.array(range(501, 551)), forecast)
    plt.title("Single exponential smoothing")
    plt.show()


def DES_(ts):
    plt.plot(ts)
    best_MSE = float('inf')
    best_i = 0
    best_j = 0
    best_series = None
    best_b = None

    for i in range(1, 20):
        for j in range(1, 11):
            des, b = double_exponential_smoothing(ts, i / 10, j / 100)
            mse = mean_square_error(ts[1:], des)
            if mse < best_MSE:
                best_i = i
                best_j = j
                best_MSE = mse
                best_series = des
                best_b = b

    forecast = double_exponential_forecast(ts, best_series, best_b)
    plt.xlabel("alpha = " + str(best_i) + ", gama = " + str(best_j))
    plt.plot(np.array(range(501, 551)), forecast)
    plt.title("Double exponential smoothing")
    plt.show()


if __name__ == '__main__':
    ts = load_time_series()
    MA_(ts)
    CMA_(ts)
    DMA_(ts)

    LR_(ts)
    SES_(ts)
    DES_(ts)
