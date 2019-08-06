from collections import defaultdict
from itertools import chain, combinations

def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def join_set(itemsets, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemsets for j in itemsets if len(i.union(j)) == length])

def get_unique_items(records):
    '''
    get all unique items (unique 1-itemsets)
    '''
    items = set()
    for transaction in records:
        for item in transaction:
            items.add(frozenset([item]))
    return items

class Apriori(object):
    def __init__(self, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_set = dict()
        self.large_set = dict()
        self.num_records = 0

    def _get_frequent_itemset(self, itemsets, records):
        """calculates the support for items in the itemSet and returns a subset
        of the itemSet each of whose elements satisfies the minimum support"""
        frequent_set_pass = dict()
        candidate_set = defaultdict(int)
        num_records = len(records)

        # count for every candidate set
        for item in itemsets:
            for transaction in records:
                if item.issubset(transaction):
                    candidate_set[item] += 1

        # thresholding
        for item, count in candidate_set.items():
            support = float(count) / num_records
            if support >= self.min_support:
                frequent_set_pass[item] = count
        return frequent_set_pass

    def get_support(self, item):
        return float(self.frequent_set[item]) / self.num_records

    def fit(self, records):
        """
        run the apriori algorithm. data_iter is a record iterator
        Return both:
        - items (tuple, support)
        - rules ((pretuple, posttuple), confidence)
        """
        items = get_unique_items(records)
        self.num_records = len(records)
    
        # k = 1
        frequent_set_pass = self._get_frequent_itemset(items, records)
        self.frequent_set.update(frequent_set_pass)
        previous_set = frequent_set_pass.keys()

        k = 2
        while(previous_set != set([])):
            self.large_set[k-1] = previous_set
            current_set = join_set(previous_set, k)
            frequent_set_pass = self._get_frequent_itemset(current_set, records)
            self.frequent_set.update(frequent_set_pass)
            previous_set = frequent_set_pass.keys()
            k = k + 1

    def gen_all_rules(self, sort_by=2):
        # generate rules
        rules = []
        for key, value in self.large_set.items():
            for item in value:
                _subsets = map(frozenset, [x for x in subsets(item)])
                for element in _subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = self.get_support(item) / self.get_support(element)
                        lift = confidence / self.get_support(remain)
                        if confidence >= self.min_confidence:
                            rules.append(((tuple(element), tuple(remain)),
                                            confidence, lift))

        return sorted(rules, key=lambda x: x[sort_by], reverse=True)

    def inspect(self, rhs, sort_by=2):
        rules = []
        for key, _ in self.frequent_set.items():
            item = key
            if rhs.issubset(item) and len(item) >1:
                element = item.difference(rhs)
                confidence = self.get_support(item) / self.get_support(element)
                lift = confidence / self.get_support(rhs)

                if confidence >= self.min_confidence:
                    rules.append(((tuple(element), tuple(rhs)),
                                confidence, lift))
        return sorted(rules, key=lambda x: x[sort_by], reverse=True)

if __name__ == '__main__':
    # training data
    transactions = [
        frozenset(['A', 'C', 'D']),
        frozenset(['B', 'C', 'E']),
        frozenset(['A', 'B', 'C', 'E']),
        frozenset(['B', 'E']),
        ]

    # model
    model = Apriori(min_support=0.5, min_confidence=0.5)
    model.fit(transactions)
    rules = model.gen_all_rules()

    # see all rules
    print('[*] all rules')
    for rule in rules :
        print('{:10s} => {:10s}, conf:{:.5f}, lift:{:.5f}'.format(
                    str(rule[0][0]), str(rule[0][1]), rule[1], rule[2]))

    print('\n --- \n')

    # inspect a specific rule
    inspected_itemset = frozenset(['E'])
    print('[*] inspected itemset:', inspected_itemset)
    rules = model.inspect(inspected_itemset)
    for rule in rules:
        print('{:10s} => {:10s}, conf:{:.5f}, lift:{:.5f}'.format(
                    str(rule[0][0]), str(rule[0][1]), rule[1], rule[2]))