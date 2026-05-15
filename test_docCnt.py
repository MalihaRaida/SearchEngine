import unittest
from docCnt import DocCnt
from doc import Doc


class TestDocCnt(unittest.TestCase):
    """Test suite for the DocCnt class."""

    def setUp(self):
        """Set up test fixtures."""
        self.doc1 = Doc.from_string("Python Tutorial\nLearn Python programming", "http://example.com/1")
        self.doc2 = Doc.from_string("Java Guide\nLearn Java programming", "http://example.com/2")
        self.doc3 = Doc.from_string("C++ Basics\nLearn C++ programming", "http://example.com/3")

    # ------------------------------------------------------------------
    # Constructor Tests
    # ------------------------------------------------------------------

    def test_init_valid(self):
        """Test creating a DocCnt with valid arguments."""
        dc = DocCnt(self.doc1, 5)
        self.assertEqual(dc.doc, self.doc1)
        self.assertEqual(dc.cnt, 5)

    def test_init_zero_count(self):
        """Test creating a DocCnt with zero count."""
        dc = DocCnt(self.doc1, 0)
        self.assertEqual(dc.cnt, 0)

    def test_init_negative_count(self):
        """Test creating a DocCnt with negative count."""
        dc = DocCnt(self.doc1, -1)
        self.assertEqual(dc.cnt, -1)

    def test_init_none_doc_raises_ValueError(self):
        """Test that None doc raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DocCnt(None, 5)
        self.assertIn("Doc cannot be None", str(context.exception))

    def test_init_invalid_doc_type_raises_TypeError(self):
        """Test that invalid doc type raises TypeError."""
        with self.assertRaises(TypeError) as context:
            DocCnt("not a doc", 5)
        self.assertIn("doc must be a Doc instance", str(context.exception))

    def test_init_invalid_cnt_type_raises_TypeError(self):
        """Test that invalid count type raises TypeError."""
        with self.assertRaises(TypeError) as context:
            DocCnt(self.doc1, "5")
        self.assertIn("cnt must be an integer", str(context.exception))

    def test_init_float_cnt_raises_TypeError(self):
        """Test that float count raises TypeError."""
        with self.assertRaises(TypeError):
            DocCnt(self.doc1, 5.5)

    # ------------------------------------------------------------------
    # Property Tests
    # ------------------------------------------------------------------

    def test_doc_property(self):
        """Test doc property accessor."""
        dc = DocCnt(self.doc1, 5)
        self.assertIs(dc.doc, self.doc1)

    def test_cnt_property(self):
        """Test cnt property accessor."""
        dc = DocCnt(self.doc1, 10)
        self.assertEqual(dc.cnt, 10)

    # ------------------------------------------------------------------
    # Comparison Tests (__eq__)
    # ------------------------------------------------------------------

    def test_eq_same_count(self):
        """Test equality with same count."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 5)
        self.assertTrue(dc1 == dc2)

    def test_eq_different_count(self):
        """Test inequality with different counts."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 10)
        self.assertFalse(dc1 == dc2)

    def test_eq_same_object(self):
        """Test equality with same object."""
        dc1 = DocCnt(self.doc1, 5)
        self.assertTrue(dc1 == dc1)

    def test_eq_none_raises_TypeError(self):
        """Test that comparing with None raises TypeError."""
        dc1 = DocCnt(self.doc1, 5)
        with self.assertRaises(TypeError) as context:
            dc1 == None
        self.assertIn("Cannot compare with None", str(context.exception))

    def test_eq_invalid_type_raises_TypeError(self):
        """Test that comparing with non-DocCnt raises TypeError."""
        dc1 = DocCnt(self.doc1, 5)
        with self.assertRaises(TypeError) as context:
            dc1 == 5
        self.assertIn("Can only compare DocCnt with DocCnt", str(context.exception))

    def test_eq_string_raises_TypeError(self):
        """Test that comparing with string raises TypeError."""
        dc1 = DocCnt(self.doc1, 5)
        with self.assertRaises(TypeError):
            dc1 == "DocCnt"

    # ------------------------------------------------------------------
    # Comparison Tests (__lt__)
    # ------------------------------------------------------------------

    def test_lt_less_than(self):
        """Test less than comparison."""
        dc1 = DocCnt(self.doc1, 3)
        dc2 = DocCnt(self.doc2, 5)
        self.assertTrue(dc1 < dc2)

    def test_lt_greater_than(self):
        """Test that greater count is not less than."""
        dc1 = DocCnt(self.doc1, 10)
        dc2 = DocCnt(self.doc2, 5)
        self.assertFalse(dc1 < dc2)

    def test_lt_equal(self):
        """Test that equal counts are not less than."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 5)
        self.assertFalse(dc1 < dc2)

    def test_lt_none_raises_TypeError(self):
        """Test that comparing with None raises TypeError."""
        dc1 = DocCnt(self.doc1, 5)
        with self.assertRaises(TypeError) as context:
            dc1 < None
        self.assertIn("Cannot compare with None", str(context.exception))

    def test_lt_invalid_type_raises_TypeError(self):
        """Test that comparing with non-DocCnt raises TypeError."""
        dc1 = DocCnt(self.doc1, 5)
        with self.assertRaises(TypeError) as context:
            dc1 < 10
        self.assertIn("Can only compare DocCnt with DocCnt", str(context.exception))

    # ------------------------------------------------------------------
    # Other Comparison Tests (provided by @total_ordering)
    # ------------------------------------------------------------------

    def test_gt_greater_than(self):
        """Test greater than comparison (provided by total_ordering)."""
        dc1 = DocCnt(self.doc1, 10)
        dc2 = DocCnt(self.doc2, 5)
        self.assertTrue(dc1 > dc2)

    def test_le_less_or_equal(self):
        """Test less than or equal comparison."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 5)
        dc3 = DocCnt(self.doc3, 10)
        self.assertTrue(dc1 <= dc2)
        self.assertTrue(dc1 <= dc3)
        self.assertFalse(dc3 <= dc1)

    def test_ge_greater_or_equal(self):
        """Test greater than or equal comparison."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 5)
        dc3 = DocCnt(self.doc3, 3)
        self.assertTrue(dc1 >= dc2)
        self.assertTrue(dc1 >= dc3)
        self.assertFalse(dc3 >= dc1)

    def test_ne_not_equal(self):
        """Test not equal comparison."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 10)
        self.assertTrue(dc1 != dc2)

    # ------------------------------------------------------------------
    # Sorting Tests
    # ------------------------------------------------------------------

    def test_sorting(self):
        """Test that DocCnt objects can be sorted by count."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 10)
        dc3 = DocCnt(self.doc3, 3)
        
        docCnts = [dc2, dc1, dc3]
        sorted_docCnts = sorted(docCnts)
        
        self.assertEqual(sorted_docCnts[0].cnt, 3)
        self.assertEqual(sorted_docCnts[1].cnt, 5)
        self.assertEqual(sorted_docCnts[2].cnt, 10)

    def test_sorting_descending(self):
        """Test sorting in descending order."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 10)
        dc3 = DocCnt(self.doc3, 3)
        
        docCnts = [dc2, dc1, dc3]
        sorted_docCnts = sorted(docCnts, reverse=True)
        
        self.assertEqual(sorted_docCnts[0].cnt, 10)
        self.assertEqual(sorted_docCnts[1].cnt, 5)
        self.assertEqual(sorted_docCnts[2].cnt, 3)

    def test_min_max(self):
        """Test that min and max work with DocCnt objects."""
        dc1 = DocCnt(self.doc1, 5)
        dc2 = DocCnt(self.doc2, 10)
        dc3 = DocCnt(self.doc3, 3)
        
        docCnts = [dc2, dc1, dc3]
        
        self.assertEqual(min(docCnts).cnt, 3)
        self.assertEqual(max(docCnts).cnt, 10)

    # ------------------------------------------------------------------
    # String Representation Tests
    # ------------------------------------------------------------------

    def test_repr(self):
        """Test __repr__ method."""
        dc = DocCnt(self.doc1, 5)
        repr_str = repr(dc)
        self.assertIn("DocCnt", repr_str)
        self.assertIn("Python Tutorial", repr_str)
        self.assertIn("5", repr_str)

    def test_str(self):
        """Test __str__ method."""
        dc = DocCnt(self.doc1, 5)
        str_repr = str(dc)
        self.assertIn("DocCnt", str_repr)
        self.assertIn("Python Tutorial", str_repr)
        self.assertIn("5", str_repr)

    # ------------------------------------------------------------------
    # Edge Cases
    # ------------------------------------------------------------------

    def test_large_count(self):
        """Test with large count value."""
        dc = DocCnt(self.doc1, 1000000)
        self.assertEqual(dc.cnt, 1000000)

    def test_comparison_with_negative_counts(self):
        """Test comparison with negative counts."""
        dc1 = DocCnt(self.doc1, -5)
        dc2 = DocCnt(self.doc2, -10)
        dc3 = DocCnt(self.doc3, 0)
        
        self.assertTrue(dc2 < dc1)  # -10 < -5
        self.assertTrue(dc1 < dc3)  # -5 < 0
        self.assertTrue(dc2 < dc3)  # -10 < 0


if __name__ == "__main__":
    unittest.main()
