#!/usr/bin/env python3
"""
Demo script for DocCnt class.

This script demonstrates the usage of the DocCnt class, including:
- Creating DocCnt objects
- Comparing based on count
- Sorting by count
- Error handling
"""

from docCnt import DocCnt
from doc import Doc


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def demo_basic_usage():
    """Demonstrate basic DocCnt creation and properties."""
    print_section("1. Basic Usage")
    
    # Create some documents
    doc1 = Doc.from_string("Python Tutorial\nLearn Python programming basics")
    doc2 = Doc.from_string("Java Guide\nLearn Java programming fundamentals")
    doc3 = Doc.from_string("C++ Basics\nIntroduction to C++ language")
    
    # Create DocCnt objects with different counts
    dc1 = DocCnt(doc1, 5)
    dc2 = DocCnt(doc2, 10)
    dc3 = DocCnt(doc3, 3)
    
    print("Created three DocCnt objects:")
    print(f"  {dc1}")
    print(f"  {dc2}")
    print(f"  {dc3}")
    
    print("\nAccessing properties:")
    print(f"  dc1.doc.title: {dc1.doc._title}")
    print(f"  dc1.cnt: {dc1.cnt}")


def demo_comparison():
    """Demonstrate comparison operations."""
    print_section("2. Comparison Operations")
    
    doc1 = Doc.from_string("Doc A\nContent A")
    doc2 = Doc.from_string("Doc B\nContent B")
    doc3 = Doc.from_string("Doc C\nContent C")
    
    dc1 = DocCnt(doc1, 5)
    dc2 = DocCnt(doc2, 10)
    dc3 = DocCnt(doc3, 5)
    
    print(f"dc1 (count=5): {dc1}")
    print(f"dc2 (count=10): {dc2}")
    print(f"dc3 (count=5): {dc3}")
    
    print("\nComparison results:")
    print(f"  dc1 == dc3: {dc1 == dc3}  (same count)")
    print(f"  dc1 == dc2: {dc1 == dc2}  (different count)")
    print(f"  dc1 < dc2:  {dc1 < dc2}   (5 < 10)")
    print(f"  dc2 > dc1:  {dc2 > dc1}   (10 > 5)")
    print(f"  dc1 <= dc3: {dc1 <= dc3}  (5 <= 5)")
    print(f"  dc1 >= dc3: {dc1 >= dc3}  (5 >= 5)")


def demo_sorting():
    """Demonstrate sorting DocCnt objects."""
    print_section("3. Sorting by Count")
    
    # Create documents with various counts
    docs_data = [
        ("High Ranking Doc", "Important content", 25),
        ("Medium Doc", "Moderate content", 10),
        ("Low Ranking Doc", "Less important", 3),
        ("Another Medium", "More content", 12),
        ("Top Doc", "Most relevant", 30),
    ]
    
    doc_cnts = []
    for title, body, count in docs_data:
        doc = Doc.from_string(f"{title}\n{body}")
        doc_cnts.append(DocCnt(doc, count))
    
    print("Original order:")
    for i, dc in enumerate(doc_cnts, 1):
        print(f"  {i}. {dc}")
    
    # Sort ascending
    sorted_asc = sorted(doc_cnts)
    print("\nSorted ascending (by count):")
    for i, dc in enumerate(sorted_asc, 1):
        print(f"  {i}. {dc}")
    
    # Sort descending
    sorted_desc = sorted(doc_cnts, reverse=True)
    print("\nSorted descending (by count):")
    for i, dc in enumerate(sorted_desc, 1):
        print(f"  {i}. {dc}")
    
    # Find min and max
    print(f"\nMinimum: {min(doc_cnts)}")
    print(f"Maximum: {max(doc_cnts)}")


def demo_search_results_ranking():
    """Demonstrate using DocCnt for search result ranking."""
    print_section("4. Search Results Ranking Use Case")
    
    print("Simulating search results for keyword 'python'...")
    print("Each DocCnt represents (document, keyword_match_count)\n")
    
    # Create search results with match counts
    search_results = [
        ("Python Basics Tutorial", "Introduction to Python...", 15),
        ("Advanced Python Topics", "Deep dive into Python...", 25),
        ("Python vs Java", "Comparison of Python and Java...", 8),
        ("Python Best Practices", "How to write better Python...", 18),
        ("Getting Started with Python", "Your first Python program...", 12),
    ]
    
    result_list = []
    for title, body, match_count in search_results:
        doc = Doc.from_string(f"{title}\n{body}")
        result_list.append(DocCnt(doc, match_count))
    
    print("Search results before ranking:")
    for i, dc in enumerate(result_list, 1):
        print(f"  {i}. {dc.doc._title:40s} (matches: {dc.cnt})")
    
    # Rank by relevance (descending order)
    ranked_results = sorted(result_list, reverse=True)
    
    print("\nRanked search results (by match count):")
    for rank, dc in enumerate(ranked_results, 1):
        print(f"  {rank}. {dc.doc._title:40s} (matches: {dc.cnt})")


def demo_error_handling():
    """Demonstrate error handling."""
    print_section("5. Error Handling")
    
    doc = Doc.from_string("Test Doc\nTest content")
    dc = DocCnt(doc, 5)
    
    # Test various error conditions
    print("Testing error conditions:\n")
    
    # 1. None doc
    print("1. Creating DocCnt with None doc:")
    try:
        DocCnt(None, 5)
    except ValueError as e:
        print(f"   ✓ Caught ValueError: {e}")
    
    # 2. Invalid doc type
    print("\n2. Creating DocCnt with invalid doc type:")
    try:
        DocCnt("not a doc", 5)
    except TypeError as e:
        print(f"   ✓ Caught TypeError: {e}")
    
    # 3. Invalid count type
    print("\n3. Creating DocCnt with invalid count type:")
    try:
        DocCnt(doc, "5")
    except TypeError as e:
        print(f"   ✓ Caught TypeError: {e}")
    
    # 4. Comparing with None
    print("\n4. Comparing DocCnt with None:")
    try:
        result = dc == None
    except TypeError as e:
        print(f"   ✓ Caught TypeError: {e}")
    
    # 5. Comparing with non-DocCnt
    print("\n5. Comparing DocCnt with integer:")
    try:
        result = dc < 10
    except TypeError as e:
        print(f"   ✓ Caught TypeError: {e}")


def demo_edge_cases():
    """Demonstrate edge cases."""
    print_section("6. Edge Cases")
    
    doc1 = Doc.from_string("Doc 1\nContent 1")
    doc2 = Doc.from_string("Doc 2\nContent 2")
    doc3 = Doc.from_string("Doc 3\nContent 3")
    
    # Zero count
    dc_zero = DocCnt(doc1, 0)
    print(f"Zero count: {dc_zero}")
    
    # Negative count
    dc_neg = DocCnt(doc2, -5)
    print(f"Negative count: {dc_neg}")
    
    # Large count
    dc_large = DocCnt(doc3, 1000000)
    print(f"Large count: {dc_large}")
    
    # Comparison with negatives and zero
    print("\nComparisons with edge cases:")
    print(f"  {dc_neg.cnt} < {dc_zero.cnt}: {dc_neg < dc_zero}")
    print(f"  {dc_zero.cnt} < {dc_large.cnt}: {dc_zero < dc_large}")
    
    # Sorting with mixed counts
    mixed = [dc_large, dc_zero, dc_neg]
    sorted_mixed = sorted(mixed)
    print("\nSorted (negative, zero, large):")
    for dc in sorted_mixed:
        print(f"  count={dc.cnt}: {dc.doc._title}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  DocCnt Class Demonstration")
    print("=" * 70)
    
    demo_basic_usage()
    demo_comparison()
    demo_sorting()
    demo_search_results_ranking()
    demo_error_handling()
    demo_edge_cases()
    
    print("\n" + "=" * 70)
    print("  Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
