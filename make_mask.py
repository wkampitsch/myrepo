# coding: utf-8
import numpy as np


def dist_ind(ind, rule):
    if rule == 'close':
        return [ind[1], ind[2]]
    elif rule == 'far_lb1':
        return [ind[0], ind[2]]
    elif rule == 'far_lb2':
        return [ind[1], ind[3]]
    elif rule == 'v_far':
        return [ind[0], ind[3]]
    else:
        print("Rule [{}] is not supported!".format(rule))
        raise ValueError


def make_mask(array, labels, rule):
    '''
    Generates a rule corresponding np.array mask
    Supported rules: 'close', 'far_lb1', 'far_lb2', 'v_far'
    Rules represent the distance between the labels - lb1 & lb2
    '''
    indices = []
    stack = [0]
    last = array[0]
    for i, item in enumerate(array[1:], 1):
        if item == last:
            stack.append(i)
        else:
            if stack:
                indices.append(stack[0])   # min index
                indices.append(stack[-1])  # max or repeat index
                stack = []
                stack.append(i)
        last = item
    if stack:
        indices.append(stack[0])
        indices.append(stack[-1])
    # eliminate first pair if not the starting label
    if labels[0] != array[0]:
        indices = indices[2:]
    # eliminate the last pair to comply with lb1, lb2 pairs
    if len(indices) / 2 % 2:
        indices = indices[:-2]
    # create group of 4 indices of the lb1 and lb2 pairs
    indices = [indices[i:i + 4] for i in range(0, len(indices), 4)]

    result = []
    for ind in indices:
        result.extend(dist_ind(ind, rule))

    mask = np.zeros(len(array), dtype=int)
    mask[result] = 1
    return mask


def print_tbl(array, mask):
    print('{:>5} - {:^4} - {:<6}'.format('label', 'mask', 'result'))
    print('-' * 21)
    rows = []
    for i, z in enumerate(zip(array, mask)):
        c, m = z
        if mask[i]:
            t = array[i]
        else:
            t = ''
        rows.append('{:>5} - {:^4} - {:<6}'.format(c, m, t))
    print('\n'.join(rows))


def run_tests(array, tests, verbose=True):
    for test in tests:
        label, rule, result = test
        mask = make_mask(array, labels=label, rule=rule)
        print("\nLabel: {} - Rule: {}".format(label, rule))
        if verbose:
            print_tbl(array, mask)
        else:
            print("Array: {}".format(array))
        if not any(mask - result):
            print("Passed Test :-)")
        else:
            print("TEST FAILED!!!")


def main():
    Y_N = np.array(['no', 'no', 'yes', 'yes', 'no', 'no',
                    'yes', 'no', 'no'])
    Y_N_TESTS = (
        (('no', 'yes'), 'close', np.array([0, 1, 1, 0, 0, 1, 1, 0, 0])),
        (('no', 'yes'), 'far_lb1', np.array([1, 0, 1, 0, 1, 0, 1, 0, 0])),
        (('no', 'yes'), 'far_lb2', np.array([0, 1, 0, 1, 0, 1, 1, 0, 0])),
        (('no', 'yes'), 'v_far', np.array([1, 0, 0, 1, 1, 0, 1, 0, 0])),
        (('yes', 'no'), 'close', np.array([0, 0, 0, 1, 1, 0, 1, 1, 0])),
        (('yes', 'no'), 'far_lb1', np.array([0, 0, 1, 0, 1, 0, 1, 1, 0])),
        (('yes', 'no'), 'far_lb2', np.array([0, 0, 0, 1, 0, 1, 1, 0, 1])),
        (('yes', 'no'), 'v_far', np.array([0, 0, 1, 0, 0, 1, 1, 0, 1]))
    )

    ON_OFF = np.array(['on', 'on', 'off', 'on', 'off',
                       'off', 'off', 'on', 'on'])
    ON_OFF_TESTS = (
        (('on', 'off'), 'close', np.array([0, 1, 1, 1, 1, 0, 0, 0, 0])),
        (('on', 'off'), 'far_lb1', np.array([1, 0, 1, 1, 1, 0, 0, 0, 0])),
        (('on', 'off'), 'far_lb2', np.array([0, 1, 1, 1, 0, 0, 1, 0, 0])),
        (('on', 'off'), 'v_far', np.array([1, 0, 1, 1, 0, 0, 1, 0, 0])),
        (('off', 'on'), 'close', np.array([0, 0, 1, 1, 0, 0, 1, 1, 0])),
        (('off', 'on'), 'far_lb1', np.array([0, 0, 1, 1, 1, 0, 0, 1, 0])),
        (('off', 'on'), 'far_lb2', np.array([0, 0, 1, 1, 0, 0, 1, 0, 1])),
        (('off', 'on'), 'v_far', np.array([0, 0, 1, 1, 1, 0, 0, 0, 1]))
    )

    ON = np.array(['on'] * 9)
    ON_TESTS = (
        (('on', 'off'), 'close', np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])),
        (('on', 'off'), 'far_lb1', np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])),
        (('on', 'off'), 'far_lb2', np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])),
        (('on', 'off'), 'v_far', np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])),
    )

    run_tests(Y_N, Y_N_TESTS, verbose=True)
    run_tests(ON_OFF, ON_OFF_TESTS, verbose=False)
    run_tests(ON, ON_TESTS, verbose=False)

if __name__ == "__main__":
    main()
