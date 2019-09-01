from collections import defaultdict
import itertools
import re


def normalize_string(s):
    assert type(s) is str
    return "".join([l for l in s if l.isspace() or l.isalpha()]).lower()


def tokenize_string(s, delim=None):
    assert type(s) is str
    if delim:
        reg_exp = "|".join(delim)
        return [x.lower() for x in re.split(reg_exp, s) if x != '']
    return normalize_string(s).split()


def make_itemsets(receipts):
    return [set(items) for items in receipts]


def update_pair_counts(pair_counts, itemset):
    """
    Updates a dictionary of pair counts for
    all pairs of items in a given itemset.
    """
    assert type(pair_counts) is defaultdict
    possible_pairs = list(itertools.combinations(itemset, 2))
    for (a, b) in possible_pairs:
        pair_counts[(a, b)] += 1
        pair_counts[(b, a)] += 1


def update_item_counts(item_counts, itemset):
    for i in itemset:
        item_counts[i] += 1


def filter_rules_by_conf(pair_counts, item_counts, threshold, count_min=1):
    rules = {}  # (item_a, item_b) -> conf (item_a => item_b)
    for (a, b) in pair_counts:
        count_ab = pair_counts[(a, b)]
        count_a = item_counts[a]
        if count_a >= count_min:
            conf = count_ab / count_a
            if conf >= threshold:
                rules[(a, b)] = conf
    return rules


def gen_rule_str(a, b, val=None, val_fmt='{:.3f}', sep=" = "):
    text = "{} => {}".format(a, b)
    if val:
        text = "conf(" + text + ")"
        text += sep + val_fmt.format(val)
    return text


def print_rules(rules):
    if type(rules) is dict or type(rules) is defaultdict:
        from operator import itemgetter
        ordered_rules = sorted(rules.items(), key=itemgetter(1), reverse=True)
    else:  # Assume rules is iterable
        ordered_rules = [((a, b), None) for a, b in rules]
    for (a, b), conf_ab in ordered_rules:
        print(gen_rule_str(a, b, conf_ab))


def find_assoc_rules(receipts, threshold, count_min=1):
    pair_counts = defaultdict(int)
    item_counts = defaultdict(int)
    for itemset in receipts:
        update_pair_counts(pair_counts, itemset)
        update_item_counts(item_counts, itemset)
    return filter_rules_by_conf(pair_counts, item_counts, threshold, count_min)


def get_baskets(g):
    baskets = g.splitlines()
    baskets_norm = [tokenize_string(basket, ',') for basket in baskets]
    return baskets_norm


if __name__ == "__main__":
    # Example of running a pairwise association rules mining analysis
    # Confidence threshold
    THRESHOLD = 0.3

    # Only consider rules for items appearing at least `MIN_COUNT` times.
    MIN_COUNT = 1

    # sample input, replace with any other input
    sample_input = "citrus fruit,milk\nalmond,milk\npeanut,citrus fruit,brocolli,apple"
    baskets = get_baskets(sample_input)
    itemsets = make_itemsets(baskets)
    basket_rules = find_assoc_rules(itemsets, THRESHOLD, MIN_COUNT)
    print_rules(basket_rules)
