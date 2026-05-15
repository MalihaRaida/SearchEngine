# TitleTable Implementation Summary

## Overview
Successfully implemented the `TitleTable` class for the Search Engine project according to the specifications in `Specifications SearchEngine.txt`.

## Implementation Details

### Class: `TitleTable`
Located in: `titleTable.py`

**Key Features:**
- Stores documents indexed by their titles for fast lookup
- Enforces unique titles (prevents duplicates)
- Provides efficient O(1) lookup by title
- Case-sensitive title matching

### Methods Implemented

#### `__init__(self)`
- Initializes an empty title table
- Uses a dictionary to store documents keyed by title

#### `addDoc(self, d: Doc) -> None`
**Purpose:** Add a document to the table

**Parameters:**
- `d`: Document to add (must not be None)

**Behavior:**
- Validates that document is not None
- Checks if a document with the same title already exists
- If duplicate found: raises `DuplicateException`
- If unique: adds document to internal dictionary

**Specification Compliance:**
- ✓ Requires d is not null
- ✓ Modifies table state
- ✓ Throws `DuplicateException` if title already exists
- ✓ Adds document with its title as key

#### `lookup(self, t: str) -> Doc`
**Purpose:** Retrieve a document by its title

**Parameters:**
- `t`: Title to search for

**Returns:**
- The `Doc` object with matching title

**Behavior:**
- Validates that title is not None or empty
- Searches internal dictionary for title
- If found: returns the document
- If not found: raises `NotPossibleException`

**Specification Compliance:**
- ✓ Throws `NotPossibleException` if t is null
- ✓ Throws `NotPossibleException` if title not found
- ✓ Returns document if found

### Exception Classes

#### `DuplicateException`
- Inherits from `Exception`
- Raised when attempting to add a document with a duplicate title
- Includes descriptive error message with the duplicate title

#### `NotPossibleException`
- Inherits from `Exception`
- Raised when an operation cannot be completed (e.g., lookup of non-existent title)
- Includes descriptive error message

## Testing

### Unit Tests (`test_titleTable.py`)
Comprehensive test suite with 10 test cases:

1. ✓ `test_init_empty` - Table starts empty
2. ✓ `test_addDoc_single` - Add single document
3. ✓ `test_addDoc_multiple` - Add multiple documents
4. ✓ `test_addDoc_duplicate_raises_exception` - Duplicate detection
5. ✓ `test_addDoc_none_raises_ValueError` - None validation
6. ✓ `test_lookup_existing` - Successful lookup
7. ✓ `test_lookup_nonexistent_raises_exception` - Not found handling
8. ✓ `test_lookup_none_raises_exception` - None validation
9. ✓ `test_lookup_empty_string_raises_exception` - Empty string validation
10. ✓ `test_case_sensitive_titles` - Case sensitivity verification

**All tests passing:** 14/14 (including Doc tests)

### Demo Script (`demo_titleTable.py`)
Interactive demonstration showing:
- Creating a TitleTable
- Adding multiple documents
- Duplicate detection
- Successful lookups
- Error handling for non-existent titles

## Usage Example

```python
from doc import Doc
from titleTable import TitleTable, DuplicateException, NotPossibleException

# Create table
table = TitleTable()

# Add documents
doc1 = Doc("Python Guide", "Learn Python programming")
table.addDoc(doc1)

# Look up document
found = table.lookup("Python Guide")
print(found.body())  # "Learn Python programming"

# Handle duplicates
try:
    table.addDoc(Doc("Python Guide", "Different content"))
except DuplicateException as e:
    print(f"Error: {e}")

# Handle missing documents
try:
    table.lookup("Non-existent Title")
except NotPossibleException as e:
    print(f"Error: {e}")
```

## Integration with Search Engine

The `TitleTable` integrates with the larger search engine system:

1. **Engine class** uses TitleTable to:
   - Store all documents added from URLs
   - Implement the `findDoc(title)` method
   - Prevent duplicate documents (same title = duplicate per spec)

2. **Doc class** provides:
   - `title()` method used by TitleTable as key
   - Document content and metadata

3. **Future integration**:
   - Will work with `WordTable` for keyword indexing
   - Will support `Query` results containing document references

## Specification Compliance Checklist

✓ FR2: Add Documents from URL
  - Documents stored locally
  - Duplicate detection by title

✓ FR3: Search by Title  
  - `lookup()` method retrieves by title
  - Returns document if found
  - Raises exception if not found

✓ ER6: Duplicate Document
  - Same title = duplicate
  - System rejects duplicates with exception

## Files Created/Modified

- `titleTable.py` - Main implementation (80 lines)
- `test_titleTable.py` - Unit tests (104 lines)
- `demo_titleTable.py` - Demo script (68 lines)

## Next Steps

To continue building the search engine, implement:
1. `wordTable.py` - Track interesting/uninteresting words and word counts
2. `query.py` - Manage query keywords and matching documents
3. `engine.py` - Main engine coordinating all components
4. `comm.py` - Fetch documents from URLs
