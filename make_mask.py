# coding: utf-8
import numpy as np
from itertools import tee, chain

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

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

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

def make_mask2(array, labels=('yes', 'no'), rule='close'):
  data = pairwise(chain(array, [-1]))
  result = []
  flag = True
  after_trigger = False
  for i, (c, n) in enumerate(data):
    #print(i, c, n)
    if c == labels[0] or after_trigger:
      if c != n and n != -1:
        result.append(i)
        result.append(i+1)
        flag = False
        after_trigger = True
      elif flag:
        result.append(i)
        flag = False
        after_trigger = True
      elif n == -1:
        result.append(i)

  result = zip(result[::2],result[1::2])
  print("result before pop: %s" % result)
  if len(result) % 2:
    result.pop()
  result = zip(result[::2],result[1::2])
  #print("result after pop: %s" % result)
  m_result = []
  for l1, l2 in result:
    m_result.extend(dist_ind(l1, l2, rule))
  #print(m_result)
  
  mask = np.zeros(len(array), dtype=int)
  mask[m_result] = 1
  return mask

def dist_ind(l1, l2, rule):
  if rule == 'close':
    return [l1[1], l2[0]]
  elif rule == 'far_label1':
    return [l1[0], l2[0]]
  elif rule == 'far_label2':
    return [l1[1], l2[1]]
  elif rule == 'very_far':
    return [l1[0], l2[1]]
  else:
    print("Rule [{}] is not supported!".format(rule))
    raise ValueError

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
      mask = make_mask2(array, labels=label, rule=rule)
      print_mask(array, mask)
      #assert any(mask - RESULTS[count]) == False, "Label:{}, Rule:{}".format(label, rule)
      count += 1

def main():  
  y_n = np.array(['no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no'])
  on_off = np.array(['on', 'on', 'off', 'on', 'off', 'off', 'off', 'on', 'on'])
  
  labels_y_n = (('no', 'yes'), ('yes', 'no'))
  labels_on_off = (('on', 'off'), ('off', 'on'))
  rules = ('close', 'far')
  rules2 = ('close', 'far_label1')
  
  #run_tbl(y_n, labels_y_n, rules2, count=0)
  #run_tbl(on_off, labels_on_off, rules2, count=4)
  print(make_mask2(on_off, labels=('off', 'on')))

if __name__ == "__main__":
  main()

