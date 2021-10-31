  from collections import deque

def binary(text, width):
    words = text.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] * (count + 1)
    breaks = [0] * (count + 1)

    def c(i, j):
        w = offsets[j] - offsets[i] + j - i - 1
        if w > width:
            return 10 ** 10 * (w - width)
        return minima[i] + (width - w) ** 2

    def h(l, k):
        low, high = l + 1, count
        while low < high:
            mid = (low + high) // 2
            if c(l, mid) <= c(k, mid):
                high = mid
            else:
                low = mid + 1
        if c(l, high) <= c(k, high):
            return high
        return l + 2

    q = deque([(0, 1)])
    for j in range(1, count + 1):
        l = q[0][0]
        if c(j - 1, j) <= c(l, j):
            minima[j] = c(j - 1, j)
            breaks[j] = j - 1
            q.clear()
            q.append((j - 1, j + 1))
        else:
            minima[j] = c(l, j)
            breaks[j] = l
            while c(j - 1, q[-1][1]) <= c(q[-1][0], q[-1][1]):
                q.pop()
            q.append((j - 1, h(j - 1, q[-1][0])))
            if j + 1 == q[1][1]:
                q.popleft()
            else:
                q[0] = q[0][0], (q[0][1] + 1)

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()
    return lines
