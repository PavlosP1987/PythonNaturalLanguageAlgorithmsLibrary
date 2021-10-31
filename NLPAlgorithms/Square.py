def int_sqrt(x):
    if x < 0:
        raise ValueError('square root not defined for negative numbers')
    n = int(x)
    if n == 0:
        return 0
    a, b = divmod(n.bit_length(), 2)
    x = 2**(a+b)
    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y

def find_match(pattern):
    lowest = int(pattern.replace('?', '0'), 2)
    highest = int(pattern.replace('?', '1'), 2)
    mask = int(pattern.replace('0', '1').replace('?', '0'), 2)
    lowsqrt = int_sqrt(lowest)
    if lowsqrt*lowsqrt != lowest:
            lowsqrt += 1
    highsqrt = int_sqrt(highest)
    for n in range(lowsqrt, highsqrt+1):
        if (n*n & mask)==lowest:
            return n*n

print(find_match('1??1??1'))
print(find_match('1??0??1'))
print(find_match('1??????????????????????????????????????????????????????????????????????1??0??1'))
