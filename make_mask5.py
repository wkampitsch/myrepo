import numpy as np

def make_mask(array, labels=('l1','l2'), rule='close', debug=False):
	'''
	create mask
	'''
	debug_info = []
	
	p_label, s_label = labels
	
	p_label_i = np.where(array == p_label)[0]
	s_label_i = np.where(array == s_label)[0]
	debug_info.append('array:{}\n{}:{} - {}:{}\n'.format(array, p_label, p_label_i, s_label, s_label_i))

	# strip the front
	mask = (s_label_i > p_label_i[0])
	s_label_i = s_label_i[mask]
	debug_info.append('\tafter stripping the front:\n \t{}:{} - {}:{}\n'.format(p_label, p_label_i, s_label, s_label_i))
	
	# del repetitive p_labels
	if rule == 'far':
		repetion = np.intersect1d(p_label_i, p_label_i + 1)
	elif rule == 'close':
		repetion = np.intersect1d(p_label_i, p_label_i - 1)
	else:
		raise Exception('rule not implemented!')
		
	# del repetitive s_labels
	repetion_s = np.intersect1d(s_label_i, s_label_i + 1)
	
	# masking with repetion on p_label
	mask = np.in1d(p_label_i, repetion, invert=True)
	debug_info.append('*{}* label: invert mask (rule={})\n{} in {}:{}\n'.format(p_label, rule, repetion, p_label, p_label_i))
	
	p_label_i = p_label_i[mask]
	debug_info.append('\tafter masking ({}):\n\t{}:{} - {}:{}\n'.format(mask, p_label, p_label_i, s_label, s_label_i))
	
	# masking with repetion on s_label
	mask = np.in1d(s_label_i, repetion_s, invert=True)
	debug_info.append('*{}* label: invert mask (rule={})\n{} in {}:{}\n'.format(s_label, rule, repetion_s, s_label, s_label_i))
	
	s_label_i = s_label_i[mask]
	debug_info.append('\tafter masking ({}):\n\t{}:{} - {}:{}\n'.format(mask, p_label, p_label_i, s_label, s_label_i))
	
	# strip the back
	if len(p_label_i) > len(s_label_i):
		p_label_i = p_label_i[:-1]
	elif len(p_label_i) < len(s_label_i):
		s_label_i = s_label_i[:-1]
		
	debug_info.append('\tafter stripping the back:\n\t{}:{} - {}:{}\n'.format(p_label, p_label_i, s_label, s_label_i))

	if debug:
		print('\n'.join(debug_info))

	mask = np.zeros(len(array), dtype=int)
	mask[p_label_i] = 1
	mask[s_label_i] = 1
	
	return  mask

def feed_chunk(array):
	max_i = len(array)-1
	result = []
	chunk = []
	for i, item in enumerate(list(array)):
		
		if not chunk:
			chunk.append(item)
		elif item in chunk:
			chunk.append(item)
		else:
			result.append(chunk)
			chunk = []
			chunk.append(item)
		#print('i:{}\nitem:{}\nchunk:{}\nresult:{}\n'.format(i, item, chunk, result))
	result.append(chunk)
	
	return result

def make_mask2(array, labels=('yes', 'no'), rule='close', debug=False):
	
	p_label, s_label = labels
	counter = -1
	front = 0
	mask = np.zeros(len(array), dtype=int)
	mx = len(feed_chunk(array))
	
	for n, chunk in enumerate(feed_chunk(array)):
		counter += len(chunk)
#		print(chunk, len(chunk), counter, mx, n)
		if p_label in chunk and not front:
			front = 1
			mx = mx - n
			if rule == 'far':
				mask[counter-len(chunk)+1] = 1
			elif rule == 'close':
				mask[counter] = 1
		elif p_label in chunk and front:	
			if rule == 'far':
				mask[counter-len(chunk)+1] = 1
			elif rule == 'close':
				mask[counter] = 1
		elif s_label in chunk and front:
			mask[counter-len(chunk)+1] = 1
		
	if mx % 2 == 1:
		mask[np.where(mask == 1)[0][-1:]] = 0
		
	return mask
	
def print_mask(array, mask):
	print('{:>4} - {:^4} - {:<6}'.format('y_n', 'mask', 'result'))
	print('-'*21)
	rows = []
	for i, z in enumerate(zip(array, mask)):
		c, m = z
		if mask[i]:
			t = array[i]
		else:
			t = ''	
		rows.append('{:>4} - {:^4} - {:<6}'.format(c, m, t))
	print('\n'.join(rows))
	print('\n')

y_n = np.array(['no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no'])
on_off = np.array(['on', 'on', 'off', 'on', 'off', 'off', 'off', 'on', 'on'])

#mask = (make_mask(y_n, labels=('no', 'yes'), rule='far', debug=False) == 1)
#print_mask(y_n, mask)

#mask = (make_mask(on_off, labels=('on', 'off'), rule='close', debug=False ) == 1)
#print_mask(on_off, mask)

labels = (('no', 'yes'), ('yes', 'no'))
labels2 = (('on', 'off'), ('off', 'on'))
rules = ('close', 'far')

a = [np.random.choice(['yes', 'no']) for i in range(10)]
a = np.array(a)
a = on_off

for l in labels2:
	for r in rules:
		pass
		print(l, r)
		mask = (make_mask2(a, labels=l, rule=r) == 1)
		print_mask(a, mask)

#print_mask(y_n, mask_mask2(y_n, labels=('yes', 'no')))

#print(feed_chunk(y_n))



