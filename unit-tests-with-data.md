# Unit Test Document — Search Engine Classes
### Test Data Reference

| Document ID | Title | Key Words (interesting) | Source File |
|-------------|-------|------------------------|-------------|
| D1 | `Python Programming Language Guide` | python, algorithm, function, class, library | `01_python_programming-4.txt` |
| D2 | `Web Development with HTML CSS and JavaScript` | web, javascript, html, css, api, server | `02_web_development-5.txt` |
| D3 | `Machine Learning Fundamentals and Applications` | learning, neural, algorithm, data, model | `03_machine_learning.txt` |
| D4 | `Database Systems Design and SQL` | database, sql, table, query, transaction | `04_database_systems-2.txt` |
| D5 | `Algorithms and Data Structures` | algorithm, tree, graph, sort, hash | `05_algorithms_data_structures-3.txt` |

**URL used in tests:** `https://en.wikipedia.org/wiki/Python_(programming_language)`

**Uninteresting words (NK) examples:** `the`, `is`, `and`, `for`, `of`, `with`, `in`, `a`

---

## 1. Comm — `getDocs(String u)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| COMM-01 | Valid Wikipedia URL returns iterator | `"https://en.wikipedia.org/wiki/Python_(programming_language)"` | Non-null `Iterator`; each element is a non-null String |
| COMM-02 | Null URL | `null` | `NotPossibleException` |
| COMM-03 | Empty string | `""` | `NotPossibleException` |
| COMM-04 | No URL scheme | `"en.wikipedia.org/wiki/Python"` | `NotPossibleException` |
| COMM-05 | Completely malformed | `"not_a_url_at_all"` | `NotPossibleException` |
| COMM-06 | Whitespace string | `"   "` | `NotPossibleException` |
| COMM-07 | Valid URL but unreachable host | `"https://0.0.0.0/page"` | `NotPossibleException` |
| COMM-08 | Valid URL, site returns no documents | `"https://en.wikipedia.org/wiki/Special:BlankPage"` | Iterator with zero elements |
| COMM-09 | Iterator from D1–D5 site yields document strings | URL pointing to site hosting D1–D5 | 5 strings returned, one per document |

---

## 2. Doc — Constructor & Accessors

### `Doc(String d)` Constructor

| Test ID | Description | Input `d` | Expected |
|---------|-------------|-----------|----------|
| DOC-01 | Valid D1 document string | Raw text of `01_python_programming-4.txt` | Doc created; `title()` = `"Python Programming Language Guide"` |
| DOC-02 | Valid D3 document string | Raw text of `03_machine_learning.txt` | Doc created; `title()` = `"Machine Learning Fundamentals and Applications"` |
| DOC-03 | Null input | `null` | `NotPossibleException` |
| DOC-04 | Empty string | `""` | `NotPossibleException` |
| DOC-05 | Whitespace only | `"   \t\n"` | `NotPossibleException` |
| DOC-06 | String with title but empty body | `"Python Programming Language Guide\n"` | Doc created; `body()` returns `""` |
| DOC-07 | String with body but no parseable title | `"no title marker just body text"` | `NotPossibleException` |

### `title()`

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| DOC-08 | D1 title correct | Doc from `01_python_programming-4.txt` | `"Python Programming Language Guide"` |
| DOC-09 | D4 title correct | Doc from `04_database_systems-2.txt` | `"Database Systems Design and SQL"` |
| DOC-10 | Title is never null | Any valid Doc (D1–D5) | Non-null String |

### `body()`

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| DOC-11 | D2 body contains "JavaScript" | Doc from `02_web_development-5.txt` | `body()` contains `"JavaScript"` |
| DOC-12 | D5 body contains "algorithm" | Doc from `05_algorithms_data_structures-3.txt` | `body()` contains `"algorithm"` |
| DOC-13 | Body is never null | Any valid Doc (D1–D5) | Non-null String |

---

## 3. DocCnt — `compareTo(Object x)`

Setup: use D3 (machine learning, high word count) and D1 (python, lower count for a given keyword).

| Test ID | Description | this.cnt | x.cnt | Expected |
|---------|-------------|----------|-------|----------|
| DCNT-01 | Null argument | any | — | `NullPointerException` |
| DCNT-02 | Non-DocCnt argument (`"python"`) | any | — | `ClassCastException` |
| DCNT-03 | `this.cnt < x.cnt` | 2 (D1 occurrences of "algorithm") | 7 (D5 occurrences of "algorithm") | `-1` |
| DCNT-04 | `this.cnt == x.cnt` | 3 | 3 | `0` |
| DCNT-05 | `this.cnt > x.cnt` | 7 | 2 | `1` |
| DCNT-06 | Both counts are 0 | 0 | 0 | `0` |
| DCNT-07 | Self comparison | 5 | 5 (same object) | `0` |

---

## 4. Engine — All Methods

### `Engine()` Constructor

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| ENG-01 | Normal initialization | Uninteresting-words file present | Engine created; `"the"`, `"and"`, `"is"` are in NK |
| ENG-02 | Words file missing | File not found | `NotPossibleException` |
| ENG-03 | Words file empty | Empty file | Engine created; NK is empty |

### `queryFirst(String w)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| ENG-04 | Valid interesting word | `"algorithm"` | `Query` returned; `keys()` = `["algorithm"]` |
| ENG-05 | Matches D3 and D5 | `"algorithm"` (D3 body + D5 body both contain it) | `size()` ≥ 2 |
| ENG-06 | Uninteresting word | `"the"` (in NK) | `NotPossibleException` |
| ENG-07 | Non-word string | `"123!!"` | `NotPossibleException` |
| ENG-08 | Null input | `null` | `NotPossibleException` |
| ENG-09 | Empty string | `""` | `NotPossibleException` |
| ENG-10 | Word present in no document | `"blockchain"` (not in D1–D5) | `Query` with `size()` = 0 |
| ENG-11 | Resets Key on second call | Call `queryFirst("algorithm")` then `queryFirst("database")` | Second call sets Key = `{"database"}` only |

### `queryMore(String w)`

| Test ID | Description | State + Input | Expected |
|---------|-------------|--------------|----------|
| ENG-12 | Narrows results | After `queryFirst("algorithm")`, call `queryMore("python")` | `keys()` = `["algorithm","python"]`; `size()` ≤ previous |
| ENG-13 | D1 is in result | After `queryFirst("python")`, call `queryMore("function")` | D1 (`Python Programming Language Guide`) in matches |
| ENG-14 | Word already in Key | Key = `{"algorithm"}`, add `"algorithm"` again | `NotPossibleException` |
| ENG-15 | No prior `queryFirst` | Key = `{}`, call `queryMore("python")` | `NotPossibleException` |
| ENG-16 | Uninteresting word | `"and"` (in NK) | `NotPossibleException` |
| ENG-17 | Null input | `null` | `NotPossibleException` |

### `findDoc(String t)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| ENG-18 | D1 found by exact title | `"Python Programming Language Guide"` | Returns D1 Doc |
| ENG-19 | D4 found by exact title | `"Database Systems Design and SQL"` | Returns D4 Doc |
| ENG-20 | Unknown title throws | `"Introduction to Cooking"` | `NotPossibleException` |
| ENG-21 | Null title throws | `null` | `NotPossibleException` |
| ENG-22 | Empty string throws | `""` | `NotPossibleException` |

### `addDocs(String u)`

| Test ID | Description | State + Input | Expected |
|---------|-------------|--------------|----------|
| ENG-23 | Add Wikipedia URL; no active query | `"https://en.wikipedia.org/wiki/Python_(programming_language)"`, Key = `{}` | Documents added; empty Query returned |
| ENG-24 | Add URL with active query; matching docs | `queryFirst("neural")` active; URL site contains D3 (has "neural") | Returned Query includes D3 |
| ENG-25 | Duplicate URL | Add same Wikipedia URL twice | `NotPossibleException` on second call |
| ENG-26 | Null URL | `null` | `NotPossibleException` |
| ENG-27 | Malformed URL | `"not_a_url"` | `NotPossibleException` |

---

## 5. Query — All Methods

Setup: Index D1–D5; `queryFirst("algorithm")` → D3 and D5 match; `queryMore("python")` → only D1 and D3 remain (both contain both words).

### `keys()`

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| QRY-01 | Single keyword | `queryFirst("algorithm")` | `keys()` = `["algorithm"]` |
| QRY-02 | Two keywords | After `queryMore("python")` | `keys()` contains `"algorithm"` and `"python"` |
| QRY-03 | No-match query | `queryFirst("blockchain")` | `keys()` = `["blockchain"]`; non-null |

### `size()`

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| QRY-04 | Word in multiple docs | `queryFirst("algorithm")` (appears in D3 and D5) | `size()` = 2 |
| QRY-05 | Word in no docs | `queryFirst("blockchain")` | `size()` = 0 |
| QRY-06 | Refining narrows results | `queryFirst("sql")` → `queryMore("transaction")` | `size()` ≤ result of `queryFirst("sql")` alone |

### `fetch(int i)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| QRY-07 | `fetch(0)` is highest-ranked | `queryFirst("algorithm")` with D3 (7 hits) and D5 (9 hits) | `fetch(0)` is D5 (more occurrences) |
| QRY-08 | `fetch(1)` is second-ranked | Same setup | `fetch(1)` is D3 |
| QRY-09 | Valid last index | `fetch(size()-1)` | Returns a Doc without exception |
| QRY-10 | Index = `size()` throws | `fetch(size())` | `IndexOutOfBoundsException` |
| QRY-11 | Negative index throws | `fetch(-1)` | `IndexOutOfBoundsException` |
| QRY-12 | `fetch(0)` when `size()` = 0 | `queryFirst("blockchain")` | `IndexOutOfBoundsException` |

### `addDoc(Doc d, Hashtable h)`

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| QRY-13 | All keywords in `h` → doc added | Query keys = `["algorithm"]`; h = `{"algorithm":7, "sort":3}` | `size()` increases by 1 |
| QRY-14 | Missing keyword → doc not added | Query keys = `["algorithm","python"]`; h = `{"algorithm":2}` (no "python") | `size()` unchanged |
| QRY-15 | Empty hashtable | Query keys = `["algorithm"]`; h = `{}` | Doc not added |

---

## 6. TitleTable — All Methods

### `TitleTable()` Constructor

| Test ID | Description | Expected |
|---------|-------------|----------|
| TT-01 | Creates empty table | `lookup("Python Programming Language Guide")` → `NotPossibleException` |

### `addDoc(Doc d)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| TT-02 | Add D1 | D1 Doc | No exception; `lookup("Python Programming Language Guide")` returns D1 |
| TT-03 | Add all 5 docs | D1–D5 | All 5 retrievable by exact title |
| TT-04 | Duplicate title | Add D1, then add another Doc with title `"Python Programming Language Guide"` | `DuplicateException` |
| TT-05 | Add same Doc object twice | D1 twice | `DuplicateException` on second call |

### `lookup(String t)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| TT-06 | Exact title match D2 | `"Web Development with HTML CSS and JavaScript"` | Returns D2 Doc |
| TT-07 | Exact title match D5 | `"Algorithms and Data Structures"` | Returns D5 Doc |
| TT-08 | Non-existent title | `"Introduction to Quantum Computing"` | `NotPossibleException` |
| TT-09 | Null title | `null` | `NotPossibleException` |
| TT-10 | Empty string | `""` | `NotPossibleException` |
| TT-11 | Lookup on empty table | `"Python Programming Language Guide"` (before any `addDoc`) | `NotPossibleException` |

---

## 7. WordTable — All Methods

### `WordTable()` Constructor

| Test ID | Description | Expected |
|---------|-------------|----------|
| WT-01 | File present | Created; `isInteresting("the")` = `false`; `isInteresting("algorithm")` = `true` |
| WT-02 | File missing | `NotPossibleException` |
| WT-03 | Empty file | Created; NK empty; all words considered interesting |

### `isInteresting(String w)`

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| WT-04 | Interesting word from D1 | `"python"` | `true` |
| WT-05 | Interesting word from D5 | `"algorithm"` | `true` |
| WT-06 | Uninteresting word | `"the"` | `false` |
| WT-07 | Uninteresting word | `"and"` | `false` |
| WT-08 | Null | `null` | `false` |
| WT-09 | Empty string | `""` | `false` |
| WT-10 | Non-word with digits/symbols | `"java2!"` | `false` |
| WT-11 | Whitespace only | `"   "` | `false` |

### `addDoc(Doc d)` — void (internal indexing)

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| WT-12 | D1 indexed; interesting words recorded | D1 (`python`, `function`, `class` appear multiple times) | `lookup("python")` returns non-empty Vector containing D1 |
| WT-13 | Uninteresting words skipped | D1 added; check `"the"` | `lookup("the")` returns empty Vector |
| WT-14 | D3 indexed; "learning" recorded | D3 (contains `"learning"` ~8 times) | `lookup("learning")` returns D3 with cnt ≥ 8 |
| WT-15 | Two docs share keyword "algorithm" | D3 and D5 both added | `lookup("algorithm")` Vector size = 2 |
| WT-16 | Doc with only uninteresting words | Doc body = `"the and is for of"` | No new entries added |

### `lookup(String k)` — returns Vector

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| WT-17 | "algorithm" in D3 and D5 | `"algorithm"` | Vector of 2 DocCnts; D5 entry has higher cnt |
| WT-18 | "database" only in D4 | `"database"` | Vector of 1 DocCnt for D4 |
| WT-19 | "sql" only in D4 | `"sql"` | Vector of 1 DocCnt for D4 |
| WT-20 | Word in no documents | `"blockchain"` | Empty Vector |
| WT-21 | Each DocCnt cnt is accurate | `"neural"` in D3 (appears 5 times) | DocCnt for D3 has cnt = 5 |

### `addDoc(Doc d)` — Hashtable-returning version

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| WT-22 | D1 returns correct Hashtable | D1 Doc | Hashtable contains `{"python": N, "function": M, "class": K, ...}` where N,M,K > 0 |
| WT-23 | D4 Hashtable contains "sql" | D4 Doc | `h.get("sql")` > 0 |
| WT-24 | D2 Hashtable does not contain "the" | D2 Doc | `h.containsKey("the")` = `false` |
| WT-25 | Hashtable counts match body occurrences | D3 Doc; count "learning" | `h.get("learning")` = actual count in D3 body |
| WT-26 | All-uninteresting-word doc returns empty Hashtable | Doc body = `"the and is"` | Empty Hashtable returned |

---

## Integration Scenarios

| Test ID | Scenario | Steps | Expected |
|---------|----------|-------|----------|
| INT-01 | Full flow: index D1–D5 via Wikipedia URL, query "algorithm" | 1. `Engine()` 2. `addDocs("https://en.wikipedia.org/wiki/Python_(programming_language)")` 3. `queryFirst("algorithm")` 4. `fetch(0)` | D5 (`Algorithms and Data Structures`) returned as top result |
| INT-02 | Refine query to single result | 1. Index D1–D5 2. `queryFirst("sql")` 3. `queryMore("transaction")` 4. `fetch(0)` | D4 (`Database Systems Design and SQL`) is the only match |
| INT-03 | `findDoc` after `addDocs` | 1. `addDocs(url)` loads D1–D5 2. `findDoc("Machine Learning Fundamentals and Applications")` | Returns D3 Doc |
| INT-04 | `addDocs` with active query updates matches | 1. `queryFirst("neural")` 2. `addDocs(url)` adding D3 (contains "neural") | Returned Query includes D3 |
| INT-05 | Duplicate URL rejected | 1. `addDocs(url)` 2. `addDocs(url)` again | `NotPossibleException` on second call |
| INT-06 | `queryFirst` resets Key | 1. `queryFirst("algorithm")` 2. `queryMore("sort")` 3. `queryFirst("database")` | `keys()` = `["database"]` only |
| INT-07 | Documents ordered by match count | `queryFirst("algorithm")` with D3 and D5 indexed | `fetch(0).title()` = D5 (more "algorithm" hits than D3) |
