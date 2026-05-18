#    class TitleTable {
#       //OVERVIEW: Keeps track of documents with their titles.
     

#       // constructors
#       TitleTable ( )
#          // EFFECTS: Initializes this to be an empty table.


#       // methods
#       void addDoc (Doc d) throws DuplicateException
#          // REQUIRES: d is not null 
#          // MODIFIES:  this 
#          // EFFECTS: If a document with d ’s title is already in this throws
#          //   DuplicateException else adds d with its title to this.
 
#       Doc lookup (String t) throws NotPossibleException
#          // EFFECTS: If t is null or there is no document with title t in this 
#          //        throws NotPossibleException else returns the document with title t.

#    }

"""TitleTable keeps track of documents indexed by their titles.

Provides fast lookup by title and duplicate detection.
"""

from typing import Dict
from doc import Doc


class DuplicateException(Exception):
    """Raised when attempting to add a document with a duplicate title."""
    pass


class NotPossibleException(Exception):
    """Raised when an operation cannot be completed."""
    pass


class TitleTable:
    """Keeps track of documents with their titles.
    
    Documents are stored in a dictionary indexed by title (case-sensitive).
    """

    def __init__(self):
        """Initialize an empty title table."""
        self._docs: Dict[str, Doc] = {}

    def addDoc(self, d: Doc) -> None:
        """Add a document to the table.
        
        Args:
            d: The document to add (must not be None)
            
        Raises:
            DuplicateException: If a document with the same title already exists
            ValueError: If d is None
        """
        if d is None:
            raise ValueError("Document cannot be None")
        
        title = d.title()
        if title in self._docs:
            raise DuplicateException(f"Document with title '{title}' already exists")
        
        self._docs[title] = d

    def lookup(self, t: str) -> Doc:
        """Look up a document by title.
        
        Args:
            t: The title to search for
            
        Returns:
            The document with the given title
            
        Raises:
            NotPossibleException: If t is None or no document with that title exists
        """
        if t is None or not t:
            raise NotPossibleException("Title cannot be None or empty")
        
        if t not in self._docs:
            raise NotPossibleException(f"No document found with title '{t}'")
        
        return self._docs[t]

    def __len__(self) -> int:
        """Return the number of documents in the table."""
        return len(self._docs)

    def __contains__(self, title: str) -> bool:
        """Check if a document with the given title exists."""
        return title in self._docs
