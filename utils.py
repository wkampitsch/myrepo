from itertools import groupby


def chunker(items, chunk_size):
    '''Group items in chunks of chunk_size'''
    for _key, group in groupby(enumerate(items), lambda x: x[0] // chunk_size):
        yield [g[1] for g in group]  # can be implemented as a generator, too


def chunker2(items, chunk_size):
    '''Group items in chunks of chunk_size'''
    return (items[i:i + chunk_size] for i in range(0, len(items), chunk_size))
