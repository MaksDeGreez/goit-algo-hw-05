import random
import timeit

# Boyer-Moore

def build_shift_table(pattern):
  table = {}
  length = len(pattern)
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  table.setdefault(pattern[-1], length)
  return table

def boyer_moore_search(text, pattern):
  shift_table = build_shift_table(pattern)
  i = 0

  while i <= len(text) - len(pattern):
    j = len(pattern) - 1

    while j >= 0 and text[i + j] == pattern[j]:
      j -= 1

    if j < 0:
      return i

    i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

  return -1

# Knuth-Morris-Pratt

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

# Rabin-Karp

def rabin_karp_search(text, pattern):
    d = 256  # Number of characters in the input alphabet
    q = 101  # A prime number
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0  # Hash value for pattern
    t = 0  # Hash value for text

    for i in range(m):
        p = (d*p + ord(pattern[i])) % q
        t = (d*t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t:
            if text[s:s+m] == pattern:
                return s
        if s < n - m:
            t = (t - ord(text[s]) * h) * d + ord(text[s + m])
            t %= q
            if t < 0:
                t += q
    return -1

# Utils

def measure_time(func, text, pattern):
    times = timeit.repeat(lambda: func(text, pattern), repeat=3, number=1)
    return min(times)

def main():
    with open('text_1.txt', 'r', encoding='utf-8') as file:
        text1 = file.read()
    with open('text_2.txt', 'r', encoding='utf-8') as file:
        text2 = file.read()

    # Selecting substrings for search
    left = random.randint(0, len(text1) - 21)
    right = left + 20
    existing_substring1 = text1[left:right]
    non_existing_substring1 = 'NonExistingSubstring1'

    left = random.randint(0, len(text2) - 21)
    right = left + 20
    existing_substring2 = text2[left:right]
    non_existing_substring2 = 'NonExistingSubstring2'

    algorithms = [boyer_moore_search, kmp_search, rabin_karp_search]
    results = {}
    texts = [
        ('Text 1', text1, existing_substring1, non_existing_substring1),
        ('Text 2', text2, existing_substring2, non_existing_substring2)
    ]

    for text_name, text, existing_substring, non_existing_substring in texts:
        print(f'\n{text_name}:')
        results[text_name] = {}
        for substring_type, substring in [('Existing Substring', existing_substring), ('Non-existing Substring', non_existing_substring)]:
            print(f'\nSearching {substring_type}: "{substring[:30]}..."')
            results[text_name][substring_type] = {}
            for algorithm in algorithms:
                time_taken = measure_time(algorithm, text, substring)
                print(f'{algorithm.__name__}: {time_taken:.6f} seconds')
                results[text_name][substring_type][algorithm.__name__] = time_taken

if __name__ == "__main__":
    main()
