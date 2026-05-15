"""Demo script showing TitleTable usage with addDoc and lookup."""

from doc import Doc
from titleTable import TitleTable, DuplicateException, NotPossibleException


def main():
    print("=" * 60)
    print("TitleTable Demo - addDoc and lookup functions")
    print("=" * 60)
    
    # Create a new title table
    table = TitleTable()
    print("\n1. Created empty TitleTable")
    print(f"   Table size: {len(table)}")
    
    # Add some documents
    print("\n2. Adding documents...")
    
    doc1 = Doc("Python Programming", "Learn Python basics and advanced concepts")
    table.addDoc(doc1)
    print(f"   ✓ Added: '{doc1.title()}'")
    
    doc2 = Doc("Data Structures", "Arrays, lists, trees, and graphs explained")
    table.addDoc(doc2)
    print(f"   ✓ Added: '{doc2.title()}'")
    
    doc3 = Doc("Search Algorithms", "Binary search, DFS, BFS, and more")
    table.addDoc(doc3)
    print(f"   ✓ Added: '{doc3.title()}'")
    
    print(f"\n   Table now contains {len(table)} documents")
    
    # Try to add a duplicate
    print("\n3. Attempting to add duplicate title...")
    try:
        duplicate = Doc("Python Programming", "A different body text")
        table.addDoc(duplicate)
        print("   ✗ Should have raised DuplicateException!")
    except DuplicateException as e:
        print(f"   ✓ Caught expected exception: {e}")
    
    # Look up existing documents
    print("\n4. Looking up documents...")
    
    found = table.lookup("Data Structures")
    print(f"   ✓ Found: '{found.title()}'")
    print(f"     Body: {found.body()}")
    
    # Try to look up non-existent document
    print("\n5. Attempting to look up non-existent document...")
    try:
        table.lookup("Machine Learning")
    except NotPossibleException as e:
        print(f"   ✓ Caught expected exception: {e}")
    
    # Show all titles in table
    print(f"\n6. All documents in table ({len(table)} total):")
    for title in ["Python Programming", "Data Structures", "Search Algorithms"]:
        if title in table:
            doc = table.lookup(title)
            print(f"   • {title}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
