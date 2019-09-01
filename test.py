from main import (normalize_string, tokenize_string,
                  make_itemsets, update_pair_counts,
                  update_item_counts, filter_rules_by_conf,
                  find_assoc_rules)
from collections import defaultdict
import math


def test_normalize_string():
    assert normalize_string("I'm Iron Man") == "im iron man"


def test_tokenize_string():
    assert tokenize_string("I'm Iron Man") == ["im", "iron", "man"]
    assert tokenize_string("Tony, Stark is cool", [","]) == ["tony", " stark is cool"]
    assert tokenize_string("Tony, Stark \nis cool", [",", "\n"]) == ["tony", " stark ", "is cool"]


def test_make_itemsets():
    assert make_itemsets(["adam", "fam"]) == [{'a', 'd', 'm'}, {'f', 'a', 'm'}]
    assert make_itemsets([["milk", "milk", "fish"], ["chicken", "egg"]]) == [{'milk', 'fish'}, {'chicken', 'egg'}]


def test_update_pair_counts():
    itemset_1 = set("error")
    itemset_2 = set("dolor")
    pair_counts = defaultdict(int)

    update_pair_counts(pair_counts, itemset_1)
    assert len(pair_counts) == 6
    update_pair_counts(pair_counts, itemset_2)
    assert len(pair_counts) == 16

    for a, b in pair_counts:
        assert (b, a) in pair_counts
        assert pair_counts[(a, b)] == pair_counts[(b, a)]


def test_update_item_counts():
    itemset_1 = "error"
    item_counts = defaultdict(int)
    update_item_counts(item_counts, itemset_1)
    assert len(item_counts) == 3
    assert item_counts == {'e': 1, 'r': 3, 'o': 1}


def test_filter_rules_by_conf():
    pair_counts = {('man', 'woman'): 5,
                   ('bird', 'bee'): 3,
                   ('red fish', 'blue fish'): 7}

    item_counts = {'man': 7,
                   'bird': 9,
                   'red fish': 11}

    rules = filter_rules_by_conf(pair_counts, item_counts, 0.5)
    assert ('man', 'woman') in rules
    assert ('bird', 'bee') not in rules
    assert ('red fish', 'blue fish') in rules

    for a, b, c in [('man', 'woman', 0.7142857142857143), ('red fish', 'blue fish', 0.6363636363636364)]:
        assert math.isclose(rules[(a, b)], c, rel_tol=1e-3)


def test_find_assoc_rules():
    receipts = [set('abbc'), set('ac'), set('a')]
    rules = find_assoc_rules(receipts, 0.6)
    assert ('a', 'b') not in rules
    assert ('b', 'a') in rules
    assert ('a', 'c') in rules
    assert ('c', 'a') in rules
    assert ('b', 'c') in rules
    assert ('c', 'b') not in rules
