#  class Engine {
#      // OVERVIEW: An engine has a state as described in the search engine
#      //   data model. The methods throw the NotPossibleException
#      //   when there is a problem; the exception contains a string explaining
#      //   the problem. All instance methods modify the state of this.

#      // constructors
#      Engine( ) throws NotPossibleException
#         // EFFECTS: If the uninteresting words cannot be retrieved from the
#         //  persistent state throws NotPossibleException else creates NK and
#         //  initializes the application state appropriately.

#      // methods
#      Query queryFirst (String w) throws NotPossibleException
#         // EFFECTS: If ¬WORD(w) or w in NK throws NotPossibleException else
#         //  sets Key = { w }, performs the new query, and returns the result.

#      Query queryMore (String w) throws NotPossibleException
#         // EFFECTS: If ¬WORD(w) or w in NK or Key = { } or w in Key throws
#         //  NotPossibleException else adds w to Key and returns the query result.

#      Doc findDoc (String t) throws NotPossibleException
#         // EFFECTS: If t not in Title throws NotPossibleException
#         //   else returns the document with title t.
 
#      Query addDocs (String u) throws NotPossibleException
#         // EFFECTS: If u is not a URL for a site containing documents or u in URL
#         //  throws NotPossibleException else adds the new documents to Doc.
#         //  If no query was in progress returns the empty query result else
#         //  returns the query result that includes any matching new documents.
#  }

"""Engine is the main class coordinating the search engine functionality.

It manages documents, queries, and URL tracking according to the specification.
"""

from typing import Set
from doc import Doc
from titleTable import TitleTable, DuplicateException
from wordTable import WordTable
from query import Query
from comm import Comm


class NotPossibleException(Exception):
    """Raised when an operation cannot be completed."""
    pass


class Engine:
    """Main search engine class.
    
    Manages the state of the search engine including:
    - Documents (stored in TitleTable)
    - Word indexes (in WordTable)
    - Current query state
    - URLs that have been added
    """
    
    def __init__(self, uninteresting_file: str = None):
        """Initialize the search engine.
        
        Args:
            uninteresting_file: Path to file with uninteresting words
                               (if None, uses default)
        
        Raises:
            NotPossibleException: If uninteresting words cannot be loaded
        """
        try:
            # Initialize WordTable (loads uninteresting words)
            self._word_table = WordTable()
            
            # Initialize TitleTable (empty)
            self._title_table = TitleTable()
            
            # Initialize URL tracking set
            self._urls: Set[str] = set()
            
            # Initialize current query state
            self._current_query: Query = None
            
        except Exception as e:
            raise NotPossibleException(f"Failed to initialize engine: {str(e)}")
    
    def findDoc(self, t: str) -> Doc:
        """Find a document by its title.
        
        Args:
            t: The title to search for
            
        Returns:
            The document with the given title
            
        Raises:
            NotPossibleException: If t is None or no document with that title exists
        """
        if t is None:
            raise NotPossibleException("Title cannot be None")
        
        try:
            return self._title_table.lookup(t)
        except Exception as e:
            raise NotPossibleException(f"Document not found: {t}")
    
    def queryFirst(self, w: str) -> Query:
        """Start a new query with a single keyword.
        
        Args:
            w: The keyword to search for
            
        Returns:
            A Query object containing matching documents
            
        Raises:
            NotPossibleException: If w is not a valid word or is uninteresting
        """
        # Validate w is not None
        if w is None or not w.strip():
            raise NotPossibleException("Keyword cannot be None or empty")
        
        # Validate w is a valid word (only letters)
        normalized = w.lower()
        
        # Check if w is interesting (not in NK)
        if not self._word_table.isInteresting(normalized):
            raise NotPossibleException(f"'{w}' is not an interesting keyword")
        
        # Create new query with this keyword
        self._current_query = Query(keywords={normalized})
        
        # Find all documents containing this keyword
        doc_count_pairs = self._word_table.lookup(normalized)
        
        # Add matching documents to query
        matching_docs = [dc.doc for dc in doc_count_pairs]
        self._current_query.set_matches(matching_docs)
        
        return self._current_query
    
    def queryMore(self, w: str) -> Query:
        """Refine the current query by adding another keyword.
        
        Args:
            w: The additional keyword
            
        Returns:
            Updated Query object with filtered and re-ranked results
            
        Raises:
            NotPossibleException: If no query is active, w is invalid,
                                 w is uninteresting, or w is already in the query
        """
        # Check if there's an active query
        if self._current_query is None or self._current_query.is_empty():
            raise NotPossibleException("No active query to refine")
        
        # Validate w is not None
        if w is None or not w.strip():
            raise NotPossibleException("Keyword cannot be None or empty")
        
        normalized = w.lower()
        
        # Check if w is interesting
        if not self._word_table.isInteresting(normalized):
            raise NotPossibleException(f"'{w}' is not an interesting keyword")
        
        # Check if w is already in the query
        if self._current_query.has_keyword(normalized):
            raise NotPossibleException(f"'{w}' is already in the current query")
        
        # Add keyword to current query
        self._current_query.add_keyword(normalized)
        
        # Re-filter documents: only keep those containing ALL keywords
        current_keywords = self._current_query.keys()
        
        # Get all documents and filter to those containing all keywords
        filtered_docs = []
        for i in range(self._current_query.size()):
            doc = self._current_query.fetch(i)
            if doc.contains_all_keywords(current_keywords):
                filtered_docs.append(doc)
        
        # Update query with filtered and re-ranked results
        self._current_query.set_matches(filtered_docs)
        
        return self._current_query
    
    def addDocs(self, u: str) -> Query:
        """Add documents from a URL.
        
        Args:
            u: The URL to fetch documents from
            
        Returns:
            The current query (updated if active) or an empty query
            
        Raises:
            NotPossibleException: If URL is invalid, already added,
                                 or cannot be accessed
        """
        # Validate URL
        if u is None or not u.strip():
            raise NotPossibleException("URL cannot be None or empty")
        
        # Check if URL already added
        if u in self._urls:
            raise NotPossibleException(f"URL already added: {u}")
        
        # Fetch documents from URL (consume generator eagerly so exceptions
        # raised inside the generator are caught here, not during iteration)
        try:
            doc_strings = list(Comm.getDocs(u))
        except Exception as e:
            raise NotPossibleException(f"Cannot fetch documents from URL: {str(e)}")
        
        # Process each document
        docs_added = 0
        for doc_string in doc_strings:
            try:
                # Parse document
                doc = Doc.from_string(doc_string, url=u)
                
                # Try to add to title table (skip duplicates)
                try:
                    self._title_table.addDoc(doc)
                    
                    # Add to word table
                    word_counts = self._word_table.addDoc(doc)
                    
                    # If there's an active query, update it
                    if self._current_query is not None and not self._current_query.is_empty():
                        self._current_query.addDoc(doc, word_counts)
                    
                    docs_added += 1
                    
                except DuplicateException:
                    # Skip duplicate documents (same title)
                    continue
                    
            except ValueError as e:
                # Skip invalid documents
                continue
        
        # Add URL to tracking set
        self._urls.add(u)
        
        # Return current query or empty query
        if self._current_query is None:
            self._current_query = Query()
        
        return self._current_query
    
    def get_stats(self) -> dict:
        """Get statistics about the engine state (for debugging/testing).
        
        Returns:
            Dict with counts of documents, URLs, and query info
        """
        return {
            "documents": len(self._title_table),
            "urls_added": len(self._urls),
            "unique_words": len(self._word_table),
            "active_query": self._current_query is not None and not self._current_query.is_empty(),
            "query_keywords": len(self._current_query.keys()) if self._current_query else 0,
            "query_matches": self._current_query.size() if self._current_query else 0
        }
