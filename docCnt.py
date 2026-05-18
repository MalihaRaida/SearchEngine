# class DocCnt implements Comparable {
# // overview: DocCnt is a record like type with two fields, a Doc
# // and an integer.
# // methods
# int compareTo (Object x) throws ClassCastException, NullPointerException
# // effects: If x is null throws NullPointerException; if x isn’t a DocCnt
# // object, throws ClassCastException. Otherwise, if this.cnt < x.cnt
# // returns -1; if this.cnt = x.cnt returns 0; else returns 1.
# }


from functools import total_ordering
from doc import Doc


@total_ordering
class DocCnt:
    """
    Overview: DocCnt is a record-like type with two fields: a Doc and an integer count.
    
    The class implements comparison based on the count value, allowing DocCnt objects
    to be sorted and compared.
    """

    def __init__(self, doc: Doc, cnt: int):
        """
        Initialize a DocCnt with a document and count.
        
        Args:
            doc: The Doc object
            cnt: The count (integer)
            
        Raises:
            TypeError: If doc is not a Doc instance or cnt is not an integer
            ValueError: If doc is None
        """
        if doc is None:
            raise ValueError("Doc cannot be None")
        if not isinstance(doc, Doc):
            raise TypeError("doc must be a Doc instance")
        if not isinstance(cnt, int):
            raise TypeError("cnt must be an integer")
            
        self._doc = doc
        self._cnt = cnt

    @property
    def doc(self) -> Doc:
        """Return the Doc object."""
        return self._doc

    @property
    def cnt(self) -> int:
        """Return the count."""
        return self._cnt

    def __eq__(self, other) -> bool:
        """
        Check equality based on count.
        
        Effects: If other is null raises TypeError; if other isn't a DocCnt
                 object, raises TypeError. Otherwise, returns True if 
                 this.cnt == other.cnt, False otherwise.
        """
        if other is None:
            raise TypeError("Cannot compare with None")
        if not isinstance(other, DocCnt):
            raise TypeError("Can only compare DocCnt with DocCnt")
        return self._cnt == other._cnt

    def __lt__(self, other) -> bool:
        """
        Compare based on count for ordering.
        
        Effects: If other is null raises TypeError; if other isn't a DocCnt
                 object, raises TypeError. Otherwise, returns True if 
                 this.cnt < other.cnt, False otherwise.
        """
        if other is None:
            raise TypeError("Cannot compare with None")
        if not isinstance(other, DocCnt):
            raise TypeError("Can only compare DocCnt with DocCnt")
        return self._cnt < other._cnt

    def __repr__(self) -> str:
        """Return string representation of DocCnt."""
        return f"DocCnt(doc={self._doc._title!r}, cnt={self._cnt})"

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return f"DocCnt({self._doc._title}, {self._cnt})"
