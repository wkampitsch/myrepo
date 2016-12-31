import numpy as np
from itertools import groupby, cycle
from make_mask import print_tbl

token = cycle([0, 1])


def dist_ind(l1, l2, rule):
    if rule == 'close':
        return [l1[1], l2[0]]
    elif rule == 'far_lb1':
        return [l1[0], l2[0]]
    elif rule == 'far_lb2':
        return [l1[1], l2[1]]
    elif rule == 'v_far':
        return [l1[0], l2[1]]
    else:
        print("Rule [{}] is not supported!".format(rule))
        raise ValueError


def switch(array):
    t = next(token)
    result = [t]
    last = array[0]
    for n in array[1:]:
        if n == last + 1:
            result.append(t)
        else:
            t = next(token)
            result.append(t)
        last = n
    return result


def feed_label(indices, mask):
    for group in groupby(enumerate(indices), lambda x: mask[x[0]]):
        yield [x[1] for x in list(group[1])]


def m_mask(a_i):
    result = []
    for lb_i in feed_label(a_i, switch(a_i)):
        if len(lb_i) == 1:
            result.append(lb_i * 2)
        elif len(lb_i) > 2:
            first, *_, end = lb_i
            result.append(first + end)
        else:
            result.append(lb_i)
    return result


def main():

    y_n = np.array(['no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no'])

    labels = ('no', 'yes')
    rule = 'close'

    lb1 = np.where(y_n == labels[0])[0]
    lb2 = np.where(y_n == labels[1])[0]

    if labels[0] != y_n[0]:
        pairs = zip(m_mask(lb1)[1:], m_mask(lb2))
    else:
        pairs = zip(m_mask(lb1), m_mask(lb2))

    result = []
    for lb1, lb2 in list(pairs):
        result.extend(dist_ind(lb1, lb2, rule))

    mask = np.zeros(len(y_n), dtype=int)
    mask[result] = 1

    print_tbl(y_n, mask)

if __name__ == '__main__':
    main()
