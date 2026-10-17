import unittest
from wordfreq.cli import count


class CountTest(unittest.TestCase):
    def test_counts_case_insensitive(self):
        self.assertEqual(count("The cat and the hat")["the"], 2)

    def test_stop_words(self):
        self.assertNotIn("the", count("the end", stop={"the"}))

    def test_apostrophes(self):
        self.assertEqual(count("don't 'quote'")["quote"], 1)


if __name__ == "__main__":
    unittest.main()
