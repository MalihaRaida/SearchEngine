import unittest

from doc import Doc


class TestDoc(unittest.TestCase):
    def test_from_string_with_title_prefix(self):
        s = """
        Title: My Document
        
        This is the body. The body has words: apple apple banana.
        """
        d = Doc.from_string(s, url="http://example")
        self.assertEqual(d.title(), "My Document")
        self.assertIn("apple", d.tokens())
        self.assertEqual(d.word_counts().get("apple", 0), 2)

    def test_from_string_without_prefix(self):
        s = """
        My Title

        Body line one.
        Body line two apple.
        """
        d = Doc.from_string(s)
        self.assertEqual(d.title(), "My Title")
        self.assertIn("apple", d.tokens())

    def test_contains_all_keywords_and_match_count(self):
        s = "Title: T\n\napple banana apple cherry"
        d = Doc.from_string(s)
        self.assertTrue(d.contains_all_keywords(["apple"]))
        self.assertTrue(d.contains_all_keywords(["apple", "banana"]))
        self.assertFalse(d.contains_all_keywords(["apple", "durian"]))
        # match count: apple=2, banana=1
        self.assertEqual(d.match_count(["apple", "banana"]), 3)

    def test_empty_body_raises(self):
        with self.assertRaises(ValueError):
            Doc.from_string("   \n   \n")


if __name__ == "__main__":
    unittest.main()
