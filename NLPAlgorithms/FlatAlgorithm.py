def shortest(text, width):
    words = text.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] + [10 ** 20] * count
    breaks = [0] * (count + 1)
    for i in range(count):
        j = i + 1
        while j <= count:
            w = offsets[j] - offsets[i] + j - i - 1
            if w > width:
                break
            cost = minima[i] + (width - w) ** 2
            if cost < minima[j]:
                minima[j] = cost
                breaks[j] = i
            j += 1

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()
    return lines
