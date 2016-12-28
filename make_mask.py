# coding: utf-8
import numpy as np


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


def make_mask(array, labels, rule):
    '''
    Generates a rule corresponding np.array mask
    Supported rules: 'close', 'far_lb1', 'far_lb2', 'v_far'
    Rules represent the distance between the labels - lb1 & lb2
    '''
    first = True
    stack = []
    result = []

    for i, item in enumerate(array):
        if first:
            stack.append(i)
            last = item
            first = False
            continue
        if item == last:
            stack.append(i)
        else:
            if stack:
                result.append(stack[0])
                result.append(stack[-1])
                stack = []
                stack.append(i)
        last = item
    if stack:
        result.append(stack[0])
        result.append(stack[-1])
    # create tuple pairs of indices of the same label
    result = list(zip(result[::2], result[1::2]))
    # eliminate first pair if not the starting label
    if labels[0] != array[0]:
        result = result[1:]
    # eliminate the last pair if not a even number
    if len(result) % 2:
        result.pop()
    # create tuple pairs of pair of indices of Lb1 & Lb2
    result = zip(result[::2], result[1::2])

    m_result = []
    for l1, l2 in result:
        m_result.extend(dist_ind(l1, l2, rule))

    mask = np.zeros(len(array), dtype=int)
    mask[m_result] = 1
    return mask


def print_tbl(array, mask):
    print('{:>5} - {:^4} - {:<6}'.format('label', 'mask', 'result'))
    print('-'*21)
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

    ON = np.array(['on']*9)
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

