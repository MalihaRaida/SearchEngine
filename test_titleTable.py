"""Unit tests for TitleTable."""

import unittest
from doc import Doc
from titleTable import TitleTable, DuplicateException, NotPossibleException


class TestTitleTable(unittest.TestCase):
    
    def setUp(self):
        """Create a fresh TitleTable for each test."""
        self.table = TitleTable()
        
    def test_init_empty(self):
        """Test that a new table starts empty."""
        self.assertEqual(len(self.table), 0)
        
    def test_addDoc_single(self):
        """Test adding a single document."""
        doc = Doc("Test Title", "This is the body")
        self.table.addDoc(doc)
        self.assertEqual(len(self.table), 1)
        self.assertIn("Test Title", self.table)
        
    def test_addDoc_multiple(self):
        """Test adding multiple documents with different titles."""
        doc1 = Doc("Title 1", "Body 1")
        doc2 = Doc("Title 2", "Body 2")
        doc3 = Doc("Title 3", "Body 3")
        
        self.table.addDoc(doc1)
        self.table.addDoc(doc2)
        self.table.addDoc(doc3)
        
        self.assertEqual(len(self.table), 3)
        self.assertIn("Title 1", self.table)
        self.assertIn("Title 2", self.table)
        self.assertIn("Title 3", self.table)
        
    def test_addDoc_duplicate_raises_exception(self):
        """Test that adding a duplicate title raises DuplicateException."""
        doc1 = Doc("Same Title", "Body 1")
        doc2 = Doc("Same Title", "Body 2")
        
        self.table.addDoc(doc1)
        
        with self.assertRaises(DuplicateException) as cm:
            self.table.addDoc(doc2)
        
        self.assertIn("Same Title", str(cm.exception))
        self.assertEqual(len(self.table), 1)  # Only first doc should be added
        
    def test_addDoc_none_raises_ValueError(self):
        """Test that adding None raises ValueError."""
        with self.assertRaises(ValueError):
            self.table.addDoc(None)
            
    def test_lookup_existing(self):
        """Test looking up an existing document."""
        doc = Doc("My Document", "Some content here")
        self.table.addDoc(doc)
        
        result = self.table.lookup("My Document")
        self.assertEqual(result.title(), "My Document")
        self.assertEqual(result.body(), "Some content here")
        
    def test_lookup_nonexistent_raises_exception(self):
        """Test that looking up a nonexistent title raises NotPossibleException."""
        doc = Doc("Exists", "Body")
        self.table.addDoc(doc)
        
        with self.assertRaises(NotPossibleException) as cm:
            self.table.lookup("Does Not Exist")
        
        self.assertIn("Does Not Exist", str(cm.exception))
        
    def test_lookup_none_raises_exception(self):
        """Test that looking up None raises NotPossibleException."""
        with self.assertRaises(NotPossibleException):
            self.table.lookup(None)
            
    def test_lookup_empty_string_raises_exception(self):
        """Test that looking up empty string raises NotPossibleException."""
        with self.assertRaises(NotPossibleException):
            self.table.lookup("")
            
    def test_case_sensitive_titles(self):
        """Test that titles are case-sensitive."""
        doc1 = Doc("Title", "Body 1")
        doc2 = Doc("title", "Body 2")
        doc3 = Doc("TITLE", "Body 3")
        
        self.table.addDoc(doc1)
        self.table.addDoc(doc2)
        self.table.addDoc(doc3)
        
        self.assertEqual(len(self.table), 3)
        self.assertEqual(self.table.lookup("Title").body(), "Body 1")
        self.assertEqual(self.table.lookup("title").body(), "Body 2")
        self.assertEqual(self.table.lookup("TITLE").body(), "Body 3")


if __name__ == "__main__":
    unittest.main()
