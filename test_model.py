import unittest
from model import to_tokens, build, prob, suggest_next, load, make_vocab

class TestModel(unittest.TestCase):
    def setUp(self):
        self.sents = ["the patient was seen", "the patient was advised"]
        self.vocab = make_vocab(self.sents)
        self.foll2 = build(self.sents, n=2)
        self.foll3 = build(self.sents, n=3)

    def test_tokenizer(self):
        self.assertEqual(to_tokens("The Patient, was seen!"),
                         ["the", "patient", "was", "seen"])

    def test_bigram_counts(self):
        self.assertEqual(self.foll2[("the",)]["patient"], 2)
        self.assertEqual(self.foll2[("was",)]["seen"], 1)

    def test_laplace_probability(self):
        p = prob(self.foll2, ("the",), "patient", len(self.vocab))
        self.assertAlmostEqual(p, 3 / 8)

    def test_unseen_word_is_not_zero(self):
        self.assertGreater(prob(self.foll2, ("the",), "banana", len(self.vocab)), 0)

    def test_probabilities_sum_to_one(self):
        total = sum(prob(self.foll2, ("the",), w, len(self.vocab)) for w in self.vocab)
        self.assertAlmostEqual(total, 1.0)

    def test_unseen_context_gives_no_suggestions(self):
        self.assertEqual(suggest_next("zebra", self.foll3, self.vocab), [])

    def test_top_suggestion(self):
        self.assertEqual(suggest_next("the patient", self.foll3, self.vocab)[0][0], "was")

class TestCorpus(unittest.TestCase):
    def test_corpus_loads(self):
        self.assertGreater(len(load()), 0)

if __name__ == "__main__":
    unittest.main()