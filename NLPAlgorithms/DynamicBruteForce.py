def dynamic(text, width):
    words = text.split()
    count = len(words)
    slack = [[0] * count for i in range(count)]
    for i in range(count):
        slack[i][i] = width - len(words[i])
        for j in range(i + 1, count):
            slack[i][j] = slack[i][j - 1] - len(words[j]) - 1

    minima = [0] + [10 ** 20] * count
    breaks = [0] * count
    for j in range(count):
        i = j
        while i >= 0:
            if slack[i][j] < 0:
                cost = 10 ** 10
            else:
                cost = minima[i] + slack[i][j] ** 2
            if minima[j + 1] > cost:
                minima[j + 1] = cost
                breaks[j] = i
            i -= 1

    lines = []
    j = count
    while j > 0:
        i = breaks[j - 1]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()
    return lines
