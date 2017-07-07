from random import randint

def uniform(a, b):
    x = a[:]
    y = b[:]

    length = len(a)
    i = 0

    while i < length:
        is_swap = randint(0, 1)
        if is_swap == 1:
            x[i], y[i] = y[i], x[i]
        i+=1
    
    return x, y

def onepoint(a, b):
    i = randint(0, len(a))
    x = b[:i] + a[i:]
    y = a[:i] + b[i:]

    return x, y
