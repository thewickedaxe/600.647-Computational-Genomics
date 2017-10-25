#!/usr/bin/python

import itertools
import fileinput

nucleotides_and_friends = ['A', 'C', 'G', 'T', 'X']
nucleotides = ['A', 'C', 'G', 'T']


def filter(input, combo, index, data, key, strs):
    if index == combo:
        strs.extend(data)
        return
    elif key >= len(input):
        return
    else:
        data[index] = key
        key += 1
        filter(input, combo, index + 1, data, key, strs)
        filter(input, combo, index, data, key, strs)


def build_products(input_string, max_dist):
    strs = []
    data = list('*' * max_dist)
    filter(list(input_string), max_dist, 0, data, 0, strs)
    return [strs[i:i + max_dist] for i in range(0, len(strs), max_dist)]


def generate_substitution_candidates(input_string, target_distance):
    prods = []
    permutations = build_products(input_string, target_distance)
    chars = list(input_string)
    make_substitution_candidate(chars, prods, permutations)
    return prods


def make_substitution_candidate(char_list, prods, perms):
    for perm_list in perms:
        char_deep_copy = char_list[:]
        for pos in perm_list:
            char_deep_copy[pos] = list(set(nucleotides_and_friends) - {char_deep_copy[pos]})
        prods.append(char_deep_copy)


def get_sub_prods(input_string, target_distance):
    strings  = []
    if target_distance == 0:
        return [input_string]
    candidates = [[list(e) for e in candidate] for candidate in
                  generate_substitution_candidates(input_string, target_distance)]
    for candidate in candidates:
        for element in itertools.product(*candidate):
            strings.append(''.join(list(element)))
    return strings


def make_deleted_prod(chars, candidates, perms):
    for perm in perms:
        chars_deep = chars[:]
        for symbol in perm:
            chars_deep[symbol] = list(set(nucleotides_and_friends) - {chars_deep[symbol]})
        candidates.append(chars_deep)


def make_deleted_prods(input_string, target_distance):
    strs = []
    combination_positions = build_products(input_string, target_distance)
    char_list = list(input_string)
    make_deleted_prod(char_list, strs, combination_positions)
    return strs


def make_deleted_candidate(candiates, strings):
    for candidate in candiates:
        for symbol in itertools.product(*candidate):
            strings.append(''.join(list(symbol)))


def make_deleted_candidates(input_string, target_distance):
    strings = []
    if target_distance == 0:
        return [input_string]
    candidates = [[list(e) for e in expansion] for expansion in make_deleted_prods(input_string, target_distance)]
    make_deleted_candidate(candidates, strings)
    return [input_string.replace('X', '') for input_string in strings]


def make_insertion_prods(input_string, target_distance):
    candidates = []
    permutations = []
    permutations += build_products(input_string + ('_' * target_distance), target_distance)
    chars = list(input_string)
    for perm in permutations:
        chars_deep = chars[:]
        for pos in perm:
            chars_deep.insert(pos, nucleotides)
        candidates.append(chars_deep)
    return candidates


def extrapolate_insertion(target_string):
    if target_string.count('_') == 0:
        return target_string
    sym_list = [nucleotides if c == '_' else [c] for c in target_string]
    return [''.join(list(e)) for e in itertools.product(*sym_list)]


def make_prods(str_with_prods, strs):
    for candidate_prod in str_with_prods:
        for symbol in itertools.product(*candidate_prod):
            strs.append(''.join(list(symbol)))


def build_inserted_prods(input_string, target_dist):
    str_with_prods = [[list(e) for e in candidate_prod] for candidate_prod in
                      make_insertion_prods(input_string, target_dist)]
    strs = []
    make_prods(str_with_prods, strs)
    strs = [extrapolate_insertion(input_string) for input_string in strs]
    final_set = []
    for input_string in strs:
        if isinstance(input_string, list):
            final_set.extend(input_string)
        else:
            final_set.append(input_string)

    return final_set


def handle_del(input_string, prod_strings, target_distance):
    for i in range(0, target_distance):
        for perm in get_sub_prods(input_string, i):
            prod_strings += make_deleted_candidates(perm, (target_distance - i))
    return prod_strings


def handle_regular_case(input_string, prod_strings, target_distance):
    for i in range(0, target_distance):
        for perm in make_deleted_candidates(input_string, i):
            prod_strings += build_inserted_prods(perm, (target_distance - i))

    return prod_strings


def handle_sub_ins(input_string, prod_strings, target_distance):
    for i in range(0, target_distance):
        for perm in get_sub_prods(input_string, i):
            prod_strings += build_inserted_prods(perm, (target_distance - i))

    return prod_strings


def make_edit_candidates(input_string, target_distance):
    prod_strings = get_sub_prods(input_string, target_distance)
    prod_strings = handle_sub_ins(input_string, prod_strings, target_distance)  # deletion and insertion
    prod_strings = handle_regular_case(input_string, prod_strings, target_distance)
    prod_strings = handle_del(input_string, prod_strings, target_distance)
    return list(set(prod_strings))


def process_data(input_string, target_dist):
    str_list = [input_string]
    for target_dist in range(1, target_dist + 1):
        str_list.extend(make_edit_candidates(input_string, target_dist))
    return list(set(str_list))


def read_input_data():
    retline = ""
    max_distance = 0
    for line in fileinput.input():
        if retline == "":
            retline += line
        else:
            max_distance = int(line)
    retline = retline.strip()
    return retline, max_distance


def print_results(results):
    for result in results:
        print result


def main():
    input_string, max_dist = read_input_data()
    strs = process_data(input_string, max_dist)
    print_results(sorted(strs))


if __name__ == "__main__":
    main()
