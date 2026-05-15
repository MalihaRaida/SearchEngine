"""WordTable tracks interesting and uninteresting words, and word occurrences in documents.

Uninteresting words are loaded from a file and cannot be used as keywords.
For each interesting word, we track which documents contain it and how many times.
"""

import re
from typing import Set, Dict, List
from doc import Doc


class NotPossibleException(Exception):
    """Raised when an operation cannot be completed."""
    pass


class WordTable:
    """Keeps track of both interesting and uninteresting words.
    
    The uninteresting words are obtained from a private file.
    Records the number of times each interesting word occurs in each document.
    """
    
    # Default file containing uninteresting words
    DEFAULT_UNINTERESTING_FILE = "uninteresting_words.txt"
    
    def __init__(self, filename: str = None):
        """Initialize WordTable by loading uninteresting words from file.
        
        Args:
            filename: Path to file containing uninteresting words (one per line)
                     If None, uses DEFAULT_UNINTERESTING_FILE
        
        Raises:
            NotPossibleException: If the file cannot be read
        """
        if filename is None:
            filename = self.DEFAULT_UNINTERESTING_FILE
            
        self._uninteresting: Set[str] = set()
        self._word_docs: Dict[str, List[tuple]] = {}  # word -> [(doc, count), ...]
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self._uninteresting.add(word)
        except FileNotFoundError:
            raise NotPossibleException(f"Cannot read uninteresting words file: {filename}")
        except Exception as e:
            raise NotPossibleException(f"Error loading uninteresting words: {str(e)}")
    
    def isInteresting(self, w: str) -> bool:
        """Check if a word is interesting (can be used as a keyword).
        
        Args:
            w: The word to check
            
        Returns:
            False if w is None, not a word, or an uninteresting word
            True otherwise
        """
        if w is None or not w:
            return False
        
        # Normalize to lowercase
        normalized = w.lower()
        
        # Check if it's a valid word (letters only)
        if not re.match(r'^[a-z]+$', normalized):
            return False
        
        # Check if it's in the uninteresting set
        if normalized in self._uninteresting:
            return False
        
        return True
    
    def addDoc(self, d: Doc) -> Dict[str, int]:
        """Add all interesting words of a document to the table.
        
        Args:
            d: The document to process (must not be None)
            
        Returns:
            A dict mapping each interesting word in d to its occurrence count
            
        Modifies:
            Updates internal word-document index
        """
        if d is None:
            raise ValueError("Document cannot be None")
        
        # Get word counts from the document
        word_counts = d.word_counts()
        interesting_counts = {}
        
        # Filter to only interesting words and update index
        for word, count in word_counts.items():
            if self.isInteresting(word):
                interesting_counts[word] = count
                
                # Update the word-document index
                if word not in self._word_docs:
                    self._word_docs[word] = []
                
                self._word_docs[word].append((d, count))
        
        return interesting_counts
    
    def lookup(self, k: str) -> List[tuple]:
        """Get all documents containing a specific keyword with their counts.
        
        Args:
            k: The keyword to look up (must not be None)
            
        Returns:
            A list of (Doc, count) tuples where Doc contains keyword k, count times
            Returns empty list if keyword not found
        """
        if k is None:
            raise ValueError("Keyword cannot be None")
        
        normalized = k.lower()
        return self._word_docs.get(normalized, [])
    
    def get_uninteresting_words(self) -> Set[str]:
        """Return the set of uninteresting words."""
        return self._uninteresting.copy()
    
    def __len__(self) -> int:
        """Return the number of unique interesting words tracked."""
        return len(self._word_docs)
