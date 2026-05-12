class Doc {
      // OVERVIEW: A document contains a title and a text body.
  
"""Doc model for the search engine.

This module provides a concrete Python implementation of a document
used by the search engine. It focuses on storing a title, a body, an
optional source URL and providing tokenization and frequency/count
helpers that the engine and query components can use.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List, Optional


_WORD_RE = re.compile(r"[A-Za-z0-9]+")


class Doc:
                """Represents a document with a title, body and optional source URL.

                Primary responsibilities used by the rest of the search engine:
                - Provide access to title and body text
                - Provide normalized tokens and token frequency counts
                - Fast membership and match-count helpers for query filtering/sorting
                """

                def __init__(self, title: str, body: str, url: Optional[str] = None) -> None:
                                if title is None:
                                                raise ValueError("title must not be None")
                                if body is None:
                                                raise ValueError("body must not be None")

                                self._title = str(title)
                                self._body = str(body)
                                self.url = url

"""Doc model for the search engine.
                            """Return the total number of keyword occurrences for the given set.

                            Useful for ranking documents by how many keyword matches they contain.
                            """
                            total = 0
                            if keywords is None:
                                    return 0
                            for k in keywords:
                                    if not k:
                                            continue
                                    total += self._counts.get(k.lower(), 0)
                            return total

                    def __eq__(self, other: object) -> bool:  # equality by title
                            if not isinstance(other, Doc):
                                    return NotImplemented
                            return self._title == other._title

                    def __repr__(self) -> str:
                            return f"Doc(title={self._title!r}, url={self.url!r})"

