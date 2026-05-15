"""Query provides information about keywords and matching documents.

Documents are ranked by the total number of keyword occurrences.
"""

from typing import List, Set
from doc import Doc


class Query:
    """Provides information about the keywords of a query and matching documents.
    
    Documents are ordered by the number of keyword matches they contain,
    with document 0 containing the most matches.
    """
    
    def __init__(self, keywords: Set[str] = None):
        """Initialize a query with optional keywords.
        
        Args:
            keywords: Set of keyword strings (or None for empty query)
        """
        self._keywords: Set[str] = set(keywords) if keywords else set()
        self._matches: List[Doc] = []  # Sorted by match count (descending)
    
    def keys(self) -> List[str]:
        """Return the keywords of this query as a list."""
        return list(self._keywords)
    
    def size(self) -> int:
        """Return the count of documents that match the query."""
        return len(self._matches)
    
    def fetch(self, i: int) -> Doc:
        """Get the ith matching document.
        
        Args:
            i: Index of the document (0-based)
            
        Returns:
            The ith matching document
            
        Raises:
            IndexOutOfBoundsException: If i < 0 or i >= size()
        """
        if i < 0 or i >= len(self._matches):
            raise IndexError(f"Index {i} out of bounds for query with {len(self._matches)} matches")
        
        return self._matches[i]
    
    def addDoc(self, d: Doc, word_counts: dict = None) -> None:
        """Add a document to matches if it contains all keywords.
        
        Args:
            d: The document to potentially add
            word_counts: Optional dict mapping words in d to their counts
                        (if None, will be computed from d)
        
        Modifies:
            Adds d to matches if it contains all keywords, maintaining sort order
        """
        if d is None:
            raise ValueError("Document cannot be None")
        
        # Check if document contains all keywords
        if not d.contains_all_keywords(self._keywords):
            return
        
        # Add to matches
        self._matches.append(d)
        
        # Re-sort by match count (descending)
        self._sort_matches()
    
    def _sort_matches(self) -> None:
        """Sort matches by total keyword occurrence count (descending)."""
        keywords_list = list(self._keywords)
        self._matches.sort(
            key=lambda doc: doc.match_count(keywords_list),
            reverse=True
        )
    
    def set_matches(self, docs: List[Doc]) -> None:
        """Set the matches directly and sort them.
        
        Args:
            docs: List of documents that match all keywords
        """
        self._matches = list(docs)
        self._sort_matches()
    
    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the query.
        
        Args:
            keyword: The keyword to add
        """
        if keyword:
            self._keywords.add(keyword.lower())
    
    def has_keyword(self, keyword: str) -> bool:
        """Check if a keyword is already in the query.
        
        Args:
            keyword: The keyword to check
            
        Returns:
            True if keyword is in the query, False otherwise
        """
        return keyword.lower() in self._keywords if keyword else False
    
    def is_empty(self) -> bool:
        """Return True if the query has no keywords."""
        return len(self._keywords) == 0
    
    def __repr__(self) -> str:
        return f"Query(keywords={self._keywords}, matches={len(self._matches)})"
