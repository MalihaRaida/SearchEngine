"""Comprehensive tests for the Engine class."""

import unittest
import os
from doc import Doc
from engine import Engine, NotPossibleException


class TestEngine(unittest.TestCase):
    
    def setUp(self):
        """Create test documents file and initialize engine."""
        # Create test documents file
        self.test_docs_file = "test_docs.txt"
        with open(self.test_docs_file, 'w') as f:
            f.write("""Title: Python Programming
Python programming language basics tutorial guide

Python syntax variables functions loops


Title: Data Structures
Arrays lists trees graphs algorithms

Python data structures implementation


Title: Machine Learning
Python machine learning algorithms models

Neural networks deep learning tensorflow""")
        
        # Initialize engine
        self.engine = Engine()
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_docs_file):
            os.remove(self.test_docs_file)
    
    # =========================================================================
    # Test 1: __init__() - Constructor
    # =========================================================================
    
    def test_init_success(self):
        """Test successful engine initialization."""
        engine = Engine()
        stats = engine.get_stats()
        self.assertEqual(stats["documents"], 0)
        self.assertEqual(stats["urls_added"], 0)
        self.assertFalse(stats["active_query"])
    
    def test_init_with_missing_file(self):
        """Test initialization fails with missing uninteresting words file."""
        with self.assertRaises(NotPossibleException):
            Engine("nonexistent_file.txt")
    
    # =========================================================================
    # Test 2: findDoc() - Find Document by Title
    # =========================================================================
    
    def test_findDoc_success(self):
        """Test finding a document by title."""
        # Add documents first
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # Find document
        doc = self.engine.findDoc("Python Programming")
        self.assertEqual(doc.title(), "Python Programming")
        self.assertIn("python", doc.body().lower())
    
    def test_findDoc_not_found(self):
        """Test finding non-existent document raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.findDoc("Nonexistent Title")
    
    def test_findDoc_none_title(self):
        """Test finding document with None title raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.findDoc(None)
    
    # =========================================================================
    # Test 3: queryFirst() - Start New Query
    # =========================================================================
    
    def test_queryFirst_success(self):
        """Test starting a new query with valid keyword."""
        # Add documents
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # Start query
        query = self.engine.queryFirst("python")
        
        # Verify results
        self.assertGreater(query.size(), 0)
        self.assertIn("python", query.keys())
        
        # Check documents are ranked by occurrence
        if query.size() >= 2:
            doc1 = query.fetch(0)
            doc2 = query.fetch(1)
            count1 = doc1.match_count(["python"])
            count2 = doc2.match_count(["python"])
            self.assertGreaterEqual(count1, count2)
    
    def test_queryFirst_uninteresting_word(self):
        """Test query with uninteresting word raises exception."""
        # Add documents
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # Try uninteresting word
        with self.assertRaises(NotPossibleException):
            self.engine.queryFirst("the")
    
    def test_queryFirst_none_keyword(self):
        """Test query with None keyword raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.queryFirst(None)
    
    def test_queryFirst_empty_keyword(self):
        """Test query with empty keyword raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.queryFirst("")
    
    def test_queryFirst_no_matches(self):
        """Test query with keyword not in any document."""
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        query = self.engine.queryFirst("quantum")
        self.assertEqual(query.size(), 0)
    
    # =========================================================================
    # Test 4: queryMore() - Refine Query
    # =========================================================================
    
    def test_queryMore_success(self):
        """Test refining a query with additional keyword."""
        # Add documents
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # Start initial query
        query1 = self.engine.queryFirst("python")
        initial_size = query1.size()
        
        # Refine query
        query2 = self.engine.queryMore("machine")
        
        # Refined query should have fewer or equal matches
        self.assertLessEqual(query2.size(), initial_size)
        
        # Check keywords
        self.assertIn("python", query2.keys())
        self.assertIn("machine", query2.keys())
        
        # All results should contain both keywords
        for i in range(query2.size()):
            doc = query2.fetch(i)
            self.assertTrue(doc.contains_all_keywords(["python", "machine"]))
    
    def test_queryMore_no_active_query(self):
        """Test refining query when no query is active raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.queryMore("keyword")
    
    def test_queryMore_uninteresting_word(self):
        """Test refining with uninteresting word raises exception."""
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        self.engine.queryFirst("python")
        
        with self.assertRaises(NotPossibleException):
            self.engine.queryMore("the")
    
    def test_queryMore_duplicate_keyword(self):
        """Test adding same keyword twice raises exception."""
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        self.engine.queryFirst("python")
        
        with self.assertRaises(NotPossibleException):
            self.engine.queryMore("python")
    
    def test_queryMore_filters_results(self):
        """Test that queryMore filters to documents with ALL keywords."""
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # Query for 'python' - should match multiple docs
        query1 = self.engine.queryFirst("python")
        
        # Refine with 'learning' - should filter to only ML doc
        query2 = self.engine.queryMore("learning")
        
        # Verify filtering worked
        for i in range(query2.size()):
            doc = query2.fetch(i)
            self.assertIn("learning", doc.body().lower())
            self.assertIn("python", doc.body().lower())
    
    # =========================================================================
    # Test 5: addDocs() - Add Documents from URL
    # =========================================================================
    
    def test_addDocs_success(self):
        """Test adding documents from valid URL."""
        url = f"file://{self.test_docs_file}"
        query = self.engine.addDocs(url)
        
        # Check documents were added
        stats = self.engine.get_stats()
        self.assertGreater(stats["documents"], 0)
        
        # URL should be tracked
        self.assertIn(url, self.engine._urls)
    
    def test_addDocs_duplicate_url(self):
        """Test adding same URL twice raises exception."""
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        with self.assertRaises(NotPossibleException):
            self.engine.addDocs(url)
    
    def test_addDocs_invalid_url(self):
        """Test adding from invalid URL raises exception."""
        from comm import NotPossibleException as CommNotPossible
        with self.assertRaises((NotPossibleException, CommNotPossible)):
            self.engine.addDocs("file://nonexistent_file.txt")
    
    def test_addDocs_none_url(self):
        """Test adding from None URL raises exception."""
        with self.assertRaises(NotPossibleException):
            self.engine.addDocs(None)
    
    def test_addDocs_updates_active_query(self):
        """Test that adding docs updates an active query."""
        # Create additional documents file
        extra_docs_file = "extra_docs.txt"
        with open(extra_docs_file, 'w') as f:
            f.write("""Title: Python Testing
Python testing frameworks pytest unittest

Advanced python testing strategies""")
        
        try:
            # Add initial documents and start query
            url1 = f"file://{self.test_docs_file}"
            self.engine.addDocs(url1)
            query1 = self.engine.queryFirst("python")
            initial_matches = query1.size()
            
            # Add more documents
            url2 = f"file://{extra_docs_file}"
            query2 = self.engine.addDocs(url2)
            
            # Query should have more matches now
            self.assertGreaterEqual(query2.size(), initial_matches)
            
        finally:
            if os.path.exists(extra_docs_file):
                os.remove(extra_docs_file)
    
    def test_addDocs_skips_duplicate_titles(self):
        """Test that documents with duplicate titles are skipped."""
        # Create file with duplicate title
        dup_docs_file = "dup_docs.txt"
        with open(dup_docs_file, 'w') as f:
            f.write("""Title: Python Programming
This is a different Python Programming document""")
        
        try:
            # Add original documents
            url1 = f"file://{self.test_docs_file}"
            self.engine.addDocs(url1)
            initial_count = self.engine.get_stats()["documents"]
            
            # Try to add duplicate
            url2 = f"file://{dup_docs_file}"
            self.engine.addDocs(url2)
            
            # Count should not increase
            final_count = self.engine.get_stats()["documents"]
            self.assertEqual(initial_count, final_count)
            
        finally:
            if os.path.exists(dup_docs_file):
                os.remove(dup_docs_file)
    
    # =========================================================================
    # Integration Tests
    # =========================================================================
    
    def test_full_workflow(self):
        """Test complete workflow: add docs, query, refine, find."""
        # 1. Add documents
        url = f"file://{self.test_docs_file}"
        self.engine.addDocs(url)
        
        # 2. Start query
        query1 = self.engine.queryFirst("python")
        self.assertGreater(query1.size(), 0)
        
        # 3. Refine query
        query2 = self.engine.queryMore("learning")
        
        # 4. Find specific document
        doc = self.engine.findDoc("Machine Learning")
        self.assertEqual(doc.title(), "Machine Learning")
        
        # 5. Check stats
        stats = self.engine.get_stats()
        self.assertEqual(stats["urls_added"], 1)
        self.assertTrue(stats["active_query"])
        self.assertEqual(stats["query_keywords"], 2)


if __name__ == "__main__":
    unittest.main()
