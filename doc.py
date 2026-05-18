# class Doc {
# // overview: A document contains a title and a text body.
# // methods
# String title ( )
# // effects: Returns the title of this.
# String body ( )
# // effects: Returns the body of this.

# Doc (String d) throws NotPossibleException
# // effects: If d cannot be processed as a document throws
# // NotPossibleException else makes this be the Doc
# // Corresponding to d.
# }

import re
from collections import Counter


class NotPossibleException(ValueError):
    """Raised when a Doc cannot be created from the given string."""
    pass


class Doc:
    """A document contains a title and a text body."""

    def __init__(self, d: str, url: str = None):
        """Parse raw string d into a Doc.

        If d cannot be processed as a document raises NotPossibleException,
        else initialises this to be the Doc corresponding to d.
        url is the source URL stored with the document (spec NFR2).
        """
        if not d or not d.strip():
            raise NotPossibleException("Cannot create Doc from empty string.")

        lines = d.splitlines()
        title = None
        body_lines = []

        # Try 'Title: <title>' prefix (case-insensitive)
        for i, line in enumerate(lines):
            m = re.match(r"^[Tt]itle\s*:\s*(.+)$", line.strip())
            if m:
                title = m.group(1).strip()
                body_lines = lines[i + 1:]
                break

        if title is None:
            # No 'Title:' prefix — first non-blank line is the title
            for i, line in enumerate(lines):
                if line.strip():
                    title = line.strip()
                    body_lines = lines[i + 1:]
                    break

        if not title:
            raise NotPossibleException("Cannot determine title from document string.")

        self._title = title
        self._body = "\n".join(body_lines).strip()
        self._url = url
        # Word entries (spec NFR2): word → occurrence count in body
        self._word_counts = Counter(re.findall(r"[a-z]+", self._body.lower()))

    # ------------------------------------------------------------------
    # Factory (convenience wrapper matching the constructor signature)
    # ------------------------------------------------------------------

    @classmethod
    def from_string(cls, d: str, url: str = None) -> "Doc":
        """Equivalent to Doc(d, url=url)."""
        return cls(d, url=url)

    # ------------------------------------------------------------------
    # Methods specified in design
    # ------------------------------------------------------------------

    def title(self) -> str:
        """Return the title of this document."""
        return self._title

    def body(self) -> str:
        """Return the body text of this document."""
        return self._body

    def url(self) -> str:
        """Return the source URL of this document, or None (spec NFR2)."""
        return self._url

    def word_counts(self) -> dict:
        """Return a dict mapping each word in the body to its frequency.

        Used by WordTable.addDoc to record interesting word occurrences (spec NFR2).
        """
        return dict(self._word_counts)

    def __repr__(self) -> str:
        return f"Doc(title={self._title!r}, url={self._url!r})"