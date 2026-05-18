#    class WordTable {
#       // OVERVIEW: Keeps track of both interesting and uninteresting words.
#       //   The uninteresting words are obtained from a private file. Records
#       //   the number of times each interesting word occurs in each document.

#       // constructors
#       WordTable ( ) throws NotPossibleException
#          // EFFECTS: If the file cannot be read throws NotPossibleException
#          //   else initializes the table to contain all the words in the file
#          //   as uninteresting words.

#       // methods
#       boolean isInteresting (String w)
#          // EFFECTS: If w is null or a nonword or an uninteresting word
#          //    returns false else returns true.


#    void addDoc (Doc d)
 
#       // REQUIRES: d is not null 
#       // MODIFIES: this
#       // EFFECTS: Adds all interesting words of d to this with a count
#       // of their number of occurrences.
# Vector lookup (String k)
# // requires: k is not null.
# // effects: Returns a vector of DocCnts where the Doc contains k cnt times.
# Hashtable addDoc (Doc d)
# // requires: d is not null
# // modifies: this
# // effects: Adds information about d’s interesting words and their
# // number of occurrences to this; also returns a table mapping each
# // interesting word in d to its number of occurrences.
#    }


import re
from doc import Doc, NotPossibleException
from docCnt import DocCnt


class WordTable:
    """Keeps track of both interesting and uninteresting words.

    The uninteresting words are obtained from a private file.
    Records the number of times each interesting word occurs in each document.
    """

    _UNINTERESTING_FILE = "uninteresting_words.txt"

    def __init__(self):
        """Initialize the table with uninteresting words from the private file.

        Raises NotPossibleException if the file cannot be read.
        """
        self._uninteresting = set()
        self._word_docs = {}  # word -> [DocCnt, ...]

        try:
            with open(self._UNINTERESTING_FILE, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self._uninteresting.add(word)
        except OSError:
            raise NotPossibleException(
                f"Cannot read uninteresting words file: {self._UNINTERESTING_FILE}"
            )

    def isInteresting(self, w: str) -> bool:
        """Return False if w is None, a nonword, or an uninteresting word; True otherwise."""
        if w is None:
            return False
        if not re.match(r'^[a-z]+$', w.lower()):
            return False
        return w.lower() not in self._uninteresting

    def addDoc(self, d: Doc) -> dict:
        """Add all interesting words of d to this with their occurrence counts.

        Requires: d is not None.
        Modifies: this.
        Returns a dict (Hashtable) mapping each interesting word in d to its count.
        """
        interesting = {}
        for word, count in d.word_counts().items():
            if self.isInteresting(word):
                interesting[word] = count
                if word not in self._word_docs:
                    self._word_docs[word] = []
                self._word_docs[word].append(DocCnt(d, count))
        return interesting

    def lookup(self, k: str) -> list:
        """Return a list of DocCnts where the Doc contains k cnt times.

        Requires: k is not None.
        Returns an empty list if k is not found.
        """
        return list(self._word_docs.get(k.lower(), []))
