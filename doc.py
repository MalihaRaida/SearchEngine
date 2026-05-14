import re
from collections import Counter


class Doc:
    """A document contains a title, an optional source URL, and a text body."""

    def __init__(self, title: str, body: str, url: str = None):
        self._title = title
        self._body = body
        self._url = url
        self._word_counts = self._compute_word_counts(body)

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_string(cls, d: str, url: str = None) -> "Doc":
        """Parse a raw string into a Doc.

        The string may optionally begin with a 'Title: ...' line.
        If no such prefix is present the first non-blank line is used as
        the title and the remainder is the body.

        Raises ValueError if d cannot be processed as a document.
        """
        if not d or not d.strip():
            raise ValueError("Cannot create Doc from empty string.")

        lines = d.splitlines()

        # Try 'Title: <title>' prefix (case-insensitive)
        title = None
        body_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            match = re.match(r"^[Tt]itle\s*:\s*(.+)$", stripped)
            if match and title is None:
                title = match.group(1).strip()
                body_lines = lines[i + 1 :]
                break
        else:
            # No 'Title:' prefix — first non-blank line is the title
            for i, line in enumerate(lines):
                if line.strip():
                    title = line.strip()
                    body_lines = lines[i + 1 :]
                    break

        if not title:
            raise ValueError("Cannot determine title from document string.")

        body = "\n".join(body_lines).strip()

        return cls(title, body, url=url)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def title(self) -> str:
        """Return the title of this document."""
        return self._title

    def body(self) -> str:
        """Return the body text of this document."""
        return self._body

    def url(self) -> str:
        """Return the source URL of this document, or None."""
        return self._url

    # ------------------------------------------------------------------
    # Word / keyword helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> list:
        """Lowercase and extract alphabetic tokens from text."""
        return re.findall(r"[a-z]+", text.lower())

    @staticmethod
    def _compute_word_counts(text: str) -> Counter:
        return Counter(Doc._tokenize(text))

    def word_counts(self) -> dict:
        """Return a dict mapping each word in the body to its frequency."""
        return dict(self._word_counts)

    def tokens(self) -> set:
        """Return the set of unique words that appear in the body."""
        return set(self._word_counts.keys())

    def contains_all_keywords(self, keywords: list) -> bool:
        """Return True iff every keyword appears at least once in the body."""
        return all(kw.lower() in self._word_counts for kw in keywords)

    def match_count(self, keywords: list) -> int:
        """Return the total number of occurrences of all keywords in the body."""
        return sum(self._word_counts.get(kw.lower(), 0) for kw in keywords)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Doc(title={self._title!r}, url={self._url!r})"