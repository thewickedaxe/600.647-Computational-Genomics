#!/usr/bin/pythonc

import itertools
import fileinput

nucleotides = ['A', 'C', 'G', 'T']


def hamming_distance(str1, str2):
    assert len(str1) == len(str2)
    count = 0
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            count += 1
    return count


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


def make_prod(string_with_cart_prod, cur_position, ntides):
    for pos_list in cur_position:
        ntides_deep_copy = ntides[:]
        for pos in pos_list:
            ntides_deep_copy[pos] = list(set(nucleotides) - {ntides_deep_copy[pos]})
        string_with_cart_prod.append(ntides_deep_copy)


def make_product(input_string, max_dist):
    character_expansions = []
    ntides = list(input_string)
    combination_positions = build_products(input_string, max_dist)
    make_prod(character_expansions, combination_positions, ntides)
    return character_expansions


def make_string(cart_prod_list, strings):
    for prod in cart_prod_list:
        for element in itertools.product(*prod):
            strings.append(''.join(list(element)))


def make_viable_string(input_string, max_distance):
    strings = []
    prods = [[list(viable_str) for viable_str in prod] for prod in make_product(input_string, max_distance)]
    make_string(prods, strings)
    return strings


def process_data(input_string, max_dist):
    distances = [input_string]
    for distance in range(1, max_dist + 1):
        distances.extend(make_viable_string(input_string, distance))
    return sorted(distances)


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


def print_result(distances):
    for distance in distances:
        print distance


def main():
    input_string, max_distance = read_input_data()
    distances = process_data(input_string, max_distance)
    print_result(distances)


if __name__ == "__main__":
    main()
