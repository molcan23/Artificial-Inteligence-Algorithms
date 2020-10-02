import numpy as np

SAMPLES_ITERATION = 1000000


def p_a_b_e(b, e):
    if b and e:
        return .95
    elif b and not e:
        return .94
    elif not b and e:
        return .29
    else:
        return .001


def p_j_a(a):
    return .9 if a else .05


def p_m_a(a):
    return .7 if a else .01


def p_b(number):
    return True if number < .001 else False


def p_e(number):
    return True if number < .002 else False


def universal_p(number, threshold):
    return True if number < threshold else False


def p_a():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(3)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        all_cases += 1
        if A:
            positive += 1

    return positive / all_cases


def p_b_and_e():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(2)
        B = p_b(samples[0])
        E = p_e(samples[1])
        all_cases += 1
        if B and E:
            positive += 1

    return positive / all_cases


def p_m_and_j():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(5)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)

        p_ja = p_j_a(A)
        p_ma = p_m_a(A)
        J = universal_p(samples[3], p_ja)
        M = universal_p(samples[4], p_ma)
        all_cases += 1
        if J and M:
            positive += 1

    return positive / all_cases


def p_not_m_and_not_j():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(5)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)

        p_ja = p_j_a(A)
        p_ma = p_m_a(A)
        J = universal_p(samples[3], p_ja)
        M = universal_p(samples[4], p_ma)
        all_cases += 1
        if not J and not M:
            positive += 1

    return positive / all_cases


def p_abe():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(3)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        all_cases += 1
        if A and B and E:
            positive += 1

    return positive / all_cases


def p_j_not_a():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(4)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        if A:
            continue
        J = universal_p(samples[3], .05)
        all_cases += 1
        if J:
            positive += 1

    return positive / all_cases


def p_j_a_not_b():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(4)
        B = p_b(samples[0])
        if B:
            continue

        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        if not A:
            continue
        J = universal_p(samples[3], .05)
        all_cases += 1
        if J:
            positive += 1

    return positive / all_cases


def p_b_a():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(3)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        if not A:
            continue
        all_cases += 1
        if B:
            positive += 1

    return positive / all_cases


def p_b_j_not_m():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(5)
        B = p_b(samples[0])
        E = p_e(samples[1])
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)

        p_ja = p_j_a(A)
        p_ma = p_m_a(A)

        J = universal_p(samples[3], p_ja)
        M = universal_p(samples[4], p_ma)

        if not (J or not M):
            continue

        all_cases += 1
        if B:
            positive += 1

    return positive / all_cases


def p_j_b_or_e():
    all_cases = 0
    positive = 0

    for _ in range(SAMPLES_ITERATION):
        samples = np.random.random_sample(4)
        B = p_b(samples[0])
        E = p_e(samples[1])
        if not B and not E:
            continue
        p_a_be = p_a_b_e(B, E)
        A = universal_p(samples[2], p_a_be)
        J = universal_p(samples[3], A)
        all_cases += 1
        if J:
            positive += 1

    return positive / all_cases


if __name__ == '__main__':
    print('P(a)', p_a())
    print('P(b, e)', p_b_and_e())
    print('P(m, j)', p_m_and_j())
    print('P(not m, not j)', p_not_m_and_not_j())
    print('P(a, b, e)', p_abe())

    print()

    print('P(j| not a)', p_j_not_a())
    print('P(j| a, not b)', p_j_a_not_b())
    print('P(b| a)', p_b_a())
    print('P(b | j, not m)', p_b_j_not_m())
    print('P(j | b or e)', p_j_b_or_e())

    # print(test())

# P(j | not a) = 0.05020531292942927
# P(j | a, not b) = 0.05239153260584243
# P(b | a) = 0.3707575170989805
# P(b | j, not m) = 0.0009734194786721736
# P(j | b or e) = 0.47989707301383083
