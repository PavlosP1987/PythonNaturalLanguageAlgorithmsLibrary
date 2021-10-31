import multiprocessing as mp
pool = mp.Pool(mp.cpu_count())

results = []


def howmany_within_range2(i, row, minimum, maximum):
    
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return (i, count)



def collect_result(result):
    global results
    results.append(result)



for i, row in enumerate(data):
    pool.apply_async(howmany_within_range2, args=(i, row, 4, 8), callback=collect_result)

 
pool.close()
pool.join()  


results.sort(key=lambda x: x[0])
results_final = [r for i, r in results]

print(results_final[:10])
#> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]
