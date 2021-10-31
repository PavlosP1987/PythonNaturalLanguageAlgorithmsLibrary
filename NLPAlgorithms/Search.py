from heapq import heappush, heappop


def generate_options(prefix_proba, prefix, suffix, lang_model, missed_model, optimism=0.5, cache=None):
    options = []
    for letter in lang_model.vocabulary_ + ['']:
        if letter:  # assume a missing letter
            next_letter = letter
            new_suffix = suffix
            new_prefix = prefix + next_letter
            proba_missing_state = - np.log(missed_model.predict_proba(prefix, letter))
        else:  # assume no missing letter
            next_letter = suffix[0]
            new_suffix = suffix[1:]
            new_prefix = prefix + next_letter
            proba_missing_state = - np.log((1 - missed_model.predict_proba(prefix, next_letter)))
        proba_next_letter = - np.log(lang_model.single_proba(prefix, next_letter))
        if cache:
            proba_suffix = cache[len(new_suffix)] * optimism
        else:
            proba_suffix = - np.log(lang_model.single_proba(new_prefix, new_suffix)) * optimism
        proba = prefix_proba + proba_next_letter + proba_missing_state + proba_suffix
        options.append((proba, new_prefix, new_suffix, letter, proba_suffix))
    return options
print(generate_options(0, ' ', 'brac ', lang_model, missed_model))

def noisy_channel(word, lang_model, missed_model, freedom=1.0, max_attempts=1000, optimism=0.1, verbose=True):
    query = word + ' '
    prefix = ' '
    prefix_proba = 0.0
    suffix = query
    full_origin_logprob = -lang_model.single_log_proba(prefix, query)
    no_missing_logprob = -missed_model.single_log_proba(prefix, query)
    best_logprob = full_origin_logprob + no_missing_logprob
    # add empty beginning to the heap
    heap = [(best_logprob * optimism, prefix, suffix, '', best_logprob * optimism)]
    # add the default option (no missing letters) to candidates
    candidates = [(best_logprob, prefix + query, '', None, 0.0)]
    if verbose:
        # todo: include distortion probability
        print('baseline score is', best_logprob)
    # prepare cache for suffixes (the slowest operation)
    cache = {}
    for i in range(len(query)+1):
        future_suffix = query[:i]
        cache[len(future_suffix)] = -lang_model.single_log_proba('', future_suffix) # rough approximation
        cache[len(future_suffix)] += -missed_model.single_log_proba('', future_suffix) # at least add missingness
    
    for i in range(max_attempts):
        if not heap:
            break
        next_best = heappop(heap)
        if verbose:
            print(next_best)
        if next_best[2] == '':  # it is a leaf
            # this is the best leaf as far, add it to candidates
            if next_best[0] <= best_logprob + freedom:
                candidates.append(next_best)
                # update the best likelihood
                if next_best[0] < best_logprob:
                    best_logprob = next_best[0]
        else: # it is not a leaf - generate more options
            prefix_proba = next_best[0] - next_best[4] # all proba estimate minus suffix
            prefix = next_best[1]
            suffix = next_best[2]
            new_options = generate_options(prefix_proba, prefix, suffix, lang_model, missed_model, optimism, cache)
            # add only the solution potentioally no worse than the best + freedom
            for new_option in new_options: 
                if new_option[0] < best_logprob + freedom:
                    heappush(heap, new_option)
    if verbose:
        print('heap size is', len(heap), 'after', i, 'iterations')
    result = {}
    for candidate in candidates:
        if candidate[0] <= best_logprob + freedom:
            result[candidate[1][1:-1]] = candidate[0]
    return result
	
	
result = noisy_channel('brc', lang_model, missed_model, freedom=2.0, optimism=0.5, verbose=True)
print(result)

with open('Fellowship_of_the_Ring.txt', encoding = 'utf-8') as f:
    text = f.read()
import re
text2 = re.sub(r'[^a-z ]+', '', text.lower().replace('\n', ' '))
print(text2[0:100])

all_letters = ''.join(list(sorted(list(set(text2)))))
print(repr(all_letters))

missing_set = [
] + [(all_letters, '-' * len(all_letters))] * 3 + [(all_letters, all_letters)] * 10 + [('aeiouy', '------')] * 30



for i in range(5):
    tmp = LanguageNgramModel(i, 1.0, 0.001)
    tmp.fit(text2[0:-5000])
    print(i, tmp.single_log_proba(' ', text2[-5000:]))





big_lang_m = LanguageNgramModel(4, 0.001, 0.01)
big_lang_m.fit(text2)
big_err_m = MissingLetterModel(0, 0.1)
big_err_m.fit(missing_set)


noisy_channel('sm', big_lang_m, big_err_m, max_attempts=10000, optimism=0.9, freedom=3.0, verbose=False)

noisy_channel('frd', big_lang_m, big_err_m, max_attempts=10000, optimism=0.9, freedom=3.0, verbose=False)
