import matplotlib.pyplot as plt
import numpy as np


def load_time_series():
    time_series = []
    with open("data.txt", "r") as input_file:
        lines = input_file.readlines()
        for line in lines:
            time_series.append(float(line))
    return np.array(time_series)


def mean_square_error(series1, series2):
    return np.mean(np.sum((series1 - series2) ** 2))


def linear_regression(y):
    x = [i for i in range(len(y))]
    denominator = (len(x) * np.sum(np.multiply(x, x)) - np.sum(x) ** 2)
    a = (len(x) * np.sum(np.multiply(x, y)) - np.sum(x) * np.sum(y)) / denominator
    b = (np.sum(np.multiply(x, x)) * np.sum(y) - np.sum(x) * np.sum(np.multiply(x, y))) / denominator
    return a, b


def LR_(ts):
    a, b = linear_regression(ts)
    lts = np.array([a * i + b for i in range(len(ts))])

    plt.plot(ts)
    plt.plot(ts - lts)
    plt.title("Linear regression")
    plt.show()
    return a, b, ts - lts


def auto_correlation(ts, h):
    ts_mean = np.mean(ts)
    c_h = np.mean(np.sum([(ts[i] - ts_mean) * (ts[i + h] - ts_mean)
                          for i in range(len(ts) - h - 1)])) / (np.var(ts)**2)
    return c_h


def auto_correlation_function(ts):
    best_h = float('inf')
    best_r = float('-inf')
    r = []
    c_0 = auto_correlation(ts, 0)
    for h in range(len(ts)):
        c_h = auto_correlation(ts, h)
        r_h = c_h / c_0
        r.append(r_h)
        # pocitam, ze teoreticky by mohola byt aj zaporna korelacia (nie vsak v tychto datach)
        if abs(r_h) > abs(best_r):
            best_r = r_h
            best_h = h
    plt.plot(r)
    plt.title('autocorrelation function')
    plt.show()
    return best_h, best_r, r


def fourier_transformation(ts):
    fts = np.fft.fft(ts)
    # nasobim komplexne zdruzenym, ale napriek tomu dava ComplexWarning
    # v tom je mozno chyba, preco 3 peaky namiesto 5?
    power_spectrum = [i * np.conj(i) for i in fts]
    plt.plot(power_spectrum)
    plt.title('power spectrum')
    plt.show()


def AR(ts, degree):
    X = []
    for i in range(len(ts) - degree):
        X.append([ts[i + j] for j in range(degree)])
    Y = [i for i in ts[degree:]]
    X, Y = np.array(X), np.array(Y)
    return np.linalg.lstsq(X, Y)[0]


def predict(ts, coef, a, b, rad):
    ts = [i for i in ts]
    for _ in range(100):
        ts.append(np.sum([ts[i - rad] * coef[i] for i in range(rad)]))
    trend = np.array([a * i + b for i in range(len(ts))])
    return ts + trend


if __name__ == '__main__':
    ts = load_time_series()
    a, b, ts = LR_(ts)
    _, _, r = auto_correlation_function(ts)
    fourier_transformation(r)
    # mame 3 peaky, takze radu 3, ale najlepsie je to pre radu 5
    degree = 5
    coef = AR(ts, degree)
    predicted = predict(ts, coef, a, b, degree)
    plt.plot(predicted)
    plt.title('original + predicted time series')
    plt.show()

