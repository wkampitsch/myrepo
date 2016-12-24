# coding: utf-8
import numpy as np

def	make_mask(array, labels=('yes', 'no'), rule='far'):
	stack = []
	result_label1 = []
	result_label2 = []
	flag = False
	for n, item in enumerate(array):
		if item == labels[0]:
			stack.append(n)
			flag = True
		if flag and item == labels[1]:
			if rule == 'close':
				result_label1.append(stack[-1])
				result_label2.append(n)
				stack = []
				flag = False
			elif rule == 'far':
				result_label1.append(stack[0])
				result_label2.append(n)
				stack = []
				flag = False
	mask = np.zeros(len(array), dtype=int)
	mask[result_label1] = 1
	mask[result_label2] = 1
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

def run_tbl(array, labels, rules):
	for label in labels:
		for rule in rules:
			print("Label:{} Rule:{}\n".format(label, rule))
			mask = make_mask(array, labels=label, rule=rule)
			print_mask(array, mask)

y_n = np.array(['no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no'])
on_off = np.array(['on', 'on', 'off', 'on', 'off', 'off', 'off', 'on', 'on'])

labels_y_n = (('no', 'yes'), ('yes', 'no'))
labels_on_off = (('on', 'off'), ('off', 'on'))
rules = ('close', 'far')

run_tbl(y_n, labels_y_n, rules)
run_tbl(on_off, labels_on_off, rules)

