# coding: utf-8
import numpy as np
from itertools import chain

RESULTS = (
  np.array([0, 1, 1, 0, 0, 1, 1, 0, 0]),
  np.array([1, 0, 1, 0, 1, 0, 1, 0, 0]),
  np.array([0, 0, 0, 1, 1, 0, 1, 1, 0]),
  np.array([0, 0, 1, 0, 1, 0, 1, 1, 0]),
  np.array([0, 1, 1, 1, 1, 0, 0, 0, 0]),
  np.array([1, 0, 1, 1, 1, 0, 0, 0, 0]),
  np.array([0, 0, 1, 1, 0, 0, 1, 1, 0]),
  np.array([0, 0, 1, 1, 1, 0, 0, 1, 0]),
)

def make_mask(array, labels=('yes', 'no'), rule='far'):
  stack = []
  result = []
  flag = False
  for n, item in enumerate(array):
    if item == labels[0]:
      stack.append(n)
      flag = True
    if flag and item == labels[1]:
      if rule == 'close':
        result.append(stack[-1])
        result.append(n)
        stack = []
        flag = False
      elif rule == 'far':
        result.append(stack[0])
        result.append(n)
        stack = []
        flag = False
      else:
        raise ValueError("Not supported rule ", rule)
  mask = np.zeros(len(array), dtype=int)
  mask[result] = 1
  return mask
  

def print_mask(array, mask):
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
  print('\n')

def run_tbl(array, labels, rules, count):
  for label in labels:
    for rule in rules:
      print("Label:{} Rule:{}\n".format(label, rule))
      mask = make_mask(array, labels=label, rule=rule)
      print_mask(array, mask)
      assert any(mask - RESULTS[count]) == False, "Label:{}, Rule:{}".format(label, rule)
      count += 1

def main():  
  y_n = np.array(['no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no'])
  on_off = np.array(['on', 'on', 'off', 'on', 'off', 'off', 'off', 'on', 'on'])
  
  labels_y_n = (('no', 'yes'), ('yes', 'no'))
  labels_on_off = (('on', 'off'), ('off', 'on'))
  rules = ('close', 'far')
  
  run_tbl(y_n, labels_y_n, rules, count=0)
  run_tbl(on_off, labels_on_off, rules, count=4)

if __name__ == "__main__":
  main()

