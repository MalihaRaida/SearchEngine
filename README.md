# Search Engine

A document search engine written in Python. It indexes text documents loaded from files, supports keyword-based querying with multi-keyword refinement, and ranks results by relevance.

---

## Project Structure

```
SearchEngine/
├── main.py                  # Interactive CLI — entry point for users
├── engine.py                # Engine — central coordinator
├── doc.py                   # Doc — parses raw text into title + body
├── query.py                 # Query — holds keywords and ranked results
├── wordTable.py             # WordTable — inverted word index
├── titleTable.py            # TitleTable — title-to-document index
├── docCnt.py                # DocCnt — (Doc, count) pair used for ranking
├── comm.py                  # Comm — fetches documents from file:// URLs
├── sorting.py               # Sorting — quicksort utility (descending)
├── uninteresting_words.txt  # Stop words that cannot be used as keywords
└── docs/
    ├── technology.txt       # Sample documents: Python, ML, Web, Databases, Cloud
    ├── science.txt          # Sample documents: Evolution, Quantum, Climate, etc.
    └── history.txt          # Sample documents: Rome, WW2, Space Race, etc.
```

---

## Getting Started

### Run the interactive CLI

```bash
python main.py
```

### Load documents and search

```
> add file://docs/technology.txt
> add file://docs/science.txt
> add file://docs/history.txt
> search python
> more machine
> find Introduction to Python
> help
> quit
```

### CLI Commands

| Command | Description |
|---|---|
| `add <url>` | Load documents from a `file://` URL |
| `search <word>` | Start a new query with a single keyword |
| `more <word>` | Narrow the current query with an additional keyword |
| `find <title>` | Look up a document by its exact title |
| `help` | Show command reference |
| `quit` | Exit the program |

---

## Document File Format

Each file can contain multiple documents separated by **three blank lines** (`\n\n\n`).  
Each document must have a title either as `Title: <name>` or simply as the first non-blank line.

```
Title: Introduction to Python
Python is a high-level programming language known for its readable syntax.
It supports multiple programming paradigms.


Title: Machine Learning Fundamentals
Machine learning enables computers to learn from data.
Common techniques include supervised and unsupervised learning.
```

---

## Module Overview

### `engine.py` — Engine

The central coordinator. Holds all application state.

| Method | Description |
|---|---|
| `__init__()` | Loads stop words, initialises empty indexes and query state |
| `addDocs(url)` | Fetches documents from URL, indexes them, updates active query |
| `queryFirst(word)` | Starts a new query; returns ranked matching documents |
| `queryMore(word)` | Adds a keyword to the active query, re-filters and re-ranks |
| `findDoc(title)` | Returns the document with the given exact title |

Raises `NotPossibleException` on invalid input or unavailable resources.

---

### `doc.py` — Doc

Parses a raw string into a structured document.

| Method | Description |
|---|---|
| `title()` | Returns the document title |
| `body()` | Returns the body text |
| `url()` | Returns the source URL |
| `word_counts()` | Returns `{word: frequency}` dict of all body words |
| `match_count(keywords)` | Total occurrences of all keywords in the body (used for ranking) |
| `contains_all_keywords(keywords)` | `True` if every keyword appears at least once (used for filtering) |

---

### `query.py` — Query

Holds the active search state.

| Method | Description |
|---|---|
| `keys()` | Returns the list of current keywords |
| `size()` | Returns the number of matching documents |
| `fetch(i)` | Returns the i-th ranked document (0 = best match) |
| `addDoc(doc, word_counts)` | Adds a doc if it contains all keywords, then re-sorts |
| `set_matches(docs)` | Replaces the match list and re-sorts by `match_count` descending |

---

### `wordTable.py` — WordTable

Inverted index mapping each interesting word to the documents that contain it.

| Method | Description |
|---|---|
| `__init__()` | Reads `uninteresting_words.txt` and builds the stop-word set |
| `isInteresting(word)` | `False` if word is non-alphabetic or a stop word |
| `addDoc(doc)` | Indexes all interesting words in `doc`; returns `{word: count}` dict |
| `lookup(word)` | Returns list of `DocCnt` objects for documents containing the word |

---

### `titleTable.py` — TitleTable

Dictionary-based index from title to document.

| Method | Description |
|---|---|
| `addDoc(doc)` | Inserts doc; raises `DuplicateException` if title already exists |
| `lookup(title)` | Returns doc by exact title; raises `NotPossibleException` if not found |

---

### `docCnt.py` — DocCnt

A simple `(Doc, int)` pair. Stores a document alongside how many times a specific word appears in it. Supports `<` / `>` comparison by count for sorting.

---

### `comm.py` — Comm

Fetches raw document strings from a URL.

| Protocol | Behaviour |
|---|---|
| `file://path` | Opens the local file and splits on `\n\n\n` to yield individual documents |
| `http://` / `https://` | Not implemented — raises `NotPossibleException` |

---

### `sorting.py` — Sorting

Standalone quicksort over any list of comparable objects, in **descending** order.

---

## Architecture Diagram

```
            User
              │
              ▼
          main.py (CLI)
              │
              ▼
            Engine
         ______|_______
        /      |       \
       /       |        \
      ▼        ▼         ▼
TitleTable  WordTable  Query
    │           │         │
    ▼           ▼         ▼
   Doc        DocCnt     Doc (ranked results)

  Comm ──► raw strings ──► Doc
```

---

## Stop Words

Words listed in `uninteresting_words.txt` (one per line) are excluded from indexing and cannot be used as search keywords.  
Common examples: `a`, `an`, `and`, `the`, `is`, `of`, `in`, `to`.

---

## Running the Tests

```bash
python -m unittest discover -v
```

Individual test files: `test_doc.py`, `test_docCnt.py`, `test_engine.py`, `test_titleTable.py`.
