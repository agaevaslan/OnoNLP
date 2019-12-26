import sys
import unittest

from stanford_parse import extract_normalized_keyphrases


def read_test_data():
    tests = []
    with open('data/keyphrases.tsv') as f:
        for l in f.readlines():
            if l.split('\t')[0] == '1':
                tests.append((l.split('\t')[1], l.split('\t')[2].strip()))
    return tests


class TestKeyphrases(unittest.TestCase):
    def test_np(self):
        for sent, kp in read_test_data():
            self.assertIn(kp.lower(), extract_normalized_keyphrases(sent))
