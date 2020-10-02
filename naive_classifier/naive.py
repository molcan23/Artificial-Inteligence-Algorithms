import numpy as np
import collections

ALL = 0
EXAMPLES = None
col_names = {'cas': 0, 'chcel': 1, 'ucil': 2, 'urobil': 3}
epsilon = 0.001


def alpha_trans(x, y):
    alpha = 1 / (x + y)
    return x*alpha, y*alpha


def alpha_trans_3(x, y, z):
    alpha = 1 / (x + y +z)
    return x*alpha, y*alpha, z*alpha


def get_p(column, value):
    column = col_names[column]
    column = EXAMPLES[:, column]
    x = collections.Counter(column)
    cases = x[value]
    return cases/ALL if cases/ALL > 0 else epsilon


def get_oc(column, value):
    column = col_names[column]
    column = EXAMPLES[:, column]
    x = collections.Counter(column)
    cases = x[value]
    return cases


def get_oc_resp(column, value, condition_col, condition_val):
    column = col_names[column]
    condition_col = col_names[condition_col]
    condition_all = 0
    good = 0
    for x in EXAMPLES:
        if x[condition_col] == condition_val:
            condition_all += 1
            if x[column] == value:
                good += 1

    return good/condition_all if good/condition_all > 0 else epsilon


def get_oc_resp2(column, value, condition_col1, condition_val1, condition_col2, condition_val2):
    column = col_names[column]
    condition_col1 = col_names[condition_col1]
    condition_col2 = col_names[condition_col2]
    condition_all = 0
    good = 0
    for x in EXAMPLES:
        if x[condition_col1] == condition_val1 and x[condition_col2] == condition_val2:
            condition_all += 1
            if x[column] == value:
                good += 1

    return good/condition_all if good/condition_all > 0 else epsilon


def first():
    # urobí či neurobí skúšku, ak sa študent má čas učiť a chce sa mu učiť a pritom sa zvládne akurát naučiť na skúšku

    urobil = get_p('cas', 1) * get_p('chcel', 1) * get_oc_resp2('ucil', 1, 'cas', 1, 'chcel', 1) * \
             get_oc_resp('urobil', 1, 'ucil', 1)

    neurobil = get_p('cas', 1) * get_p('chcel', 1) * get_oc_resp2('ucil', 1, 'cas', 1, 'chcel', 1) * \
               get_oc_resp('urobil', 0, 'ucil', 1)

    urobil, neurobil = alpha_trans(urobil, neurobil)
    print('First example')
    print(urobil, neurobil)
    if urobil == neurobil:
        print('Equally probable')
        return
    print('Passed' if urobil > neurobil else 'Failed')


def second():
    # urobí či neurobí skúšku, ak sa študent nemá čas učiť ale pritom sa chce učiť a zvládne sa naučiť len málo?
    urobil = get_p('cas', 0) * get_p('chcel', 1) * get_oc_resp2('ucil', 0, 'cas', 0, 'chcel', 1) * \
             get_oc_resp('urobil', 1, 'ucil', 0)

    neurobil = get_p('cas', 0) * get_p('chcel', 1) * get_oc_resp2('ucil', 0, 'cas', 0, 'chcel', 1) * \
               get_oc_resp('urobil', 0, 'ucil', 0)

    urobil,  neurobil = alpha_trans(urobil, neurobil)

    print('Second example')
    print(urobil, neurobil)
    if urobil == neurobil:
        print('Equally probable')
        return
    print('Passed' if urobil > neurobil else 'Failed')


def third():
    # mal či nemal študent čas sa učiť, ak skúšku urobil ale naučil sa málo a učiť sa mu nechcelo
    mal = get_p('cas', 1) * get_p('chcel', 0) * get_oc_resp2('ucil', 0, 'cas', 1, 'chcel', 0) * \
          get_oc_resp('urobil', 1, 'ucil', 0)

    nemal = get_p('cas', 0) * get_p('chcel', 0) * get_oc_resp2('ucil', 0, 'cas', 0, 'chcel', 0) * \
            get_oc_resp('urobil', 1, 'ucil', 0)

    mal,  nemal = alpha_trans(mal, nemal)
    print('Third example')
    print(mal, nemal)
    if mal == nemal:
        print('Equally probable')
        return
    print('Had time' if mal > nemal else 'Didn`t have time')


def forth():
    # chcelo sa študentovi učiť, ak neurobil skúšku a pritom sa učil vela a mal na učenie čas?
    chcel = get_p('cas', 1) * get_p('chcel', 1) * get_oc_resp2('ucil', 2, 'cas', 1, 'chcel', 1) * \
            get_oc_resp('urobil', 0, 'ucil', 2)

    nechcel = get_p('cas', 1) * get_p('chcel', 0) * get_oc_resp2('ucil', 2, 'cas', 1, 'chcel', 0) * \
              get_oc_resp('urobil', 0, 'ucil', 2)

    chcel,  nechcel = alpha_trans(chcel, nechcel)
    print('Forth example')
    print(chcel, nechcel)
    if chcel == nechcel:
        print('Equally probable')
        return
    print('Wanted' if chcel > nechcel else 'Didn`t want')


def fifth():
    # kolko sa študent učil, ak skúšku urobil, učiť sa mu nechcelo a mal na učenie čas?
    malo = get_p('cas', 1) * get_p('chcel', 0) * get_oc_resp2('ucil', 0, 'cas', 1, 'chcel', 0) * \
           get_oc_resp('urobil', 1, 'ucil', 0)

    akurat = get_p('cas', 1) * get_p('chcel', 0) * get_oc_resp2('ucil', 1, 'cas', 1, 'chcel', 0) * \
             get_oc_resp('urobil', 1, 'ucil', 1)

    vela = get_p('cas', 1) * get_p('chcel', 0) * get_oc_resp2('ucil', 2, 'cas', 1, 'chcel', 0) * \
           get_oc_resp('urobil', 1, 'ucil', 2)

    malo, akurat, vela = alpha_trans_3(malo, akurat, vela)

    print('Fifth example')
    print(malo, akurat, vela)
    if malo == akurat == vela:
        print('Equally probable')
        return
    if max(malo, akurat, vela) == malo:
        print('Not much')
    if max(malo, akurat, vela) == akurat:
        print('Enough')
    if max(malo, akurat, vela) == vela:
        print('A lot')


if __name__ == '__main__':
    EXAMPLES = np.loadtxt("naiveClassifierData.txt")
    ALL = EXAMPLES.shape[0]

    first()
    print()
    second()
    print()
    third()
    print()
    forth()
    print()
    fifth()



