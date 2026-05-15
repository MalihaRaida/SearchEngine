"""Demo script showcasing the complete Engine functionality.

This demonstrates all five Engine methods:
1. __init__() - Initialize engine
2. findDoc() - Find document by title
3. queryFirst() - Start new query with keyword
4. queryMore() - Refine query with additional keyword
5. addDocs() - Add documents from URL
"""

from engine import Engine, NotPossibleException
import os


def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)


def print_query_results(query, label="Query Results"):
    """Pretty print query results."""
    print(f"\n{label}:")
    print(f"  Keywords: {', '.join(query.keys())}")
    print(f"  Matches: {query.size()}")
    
    if query.size() > 0:
        print("\n  Top matches (ranked by keyword frequency):")
        for i in range(min(3, query.size())):
            doc = query.fetch(i)
            match_count = doc.match_count(query.keys())
            print(f"    {i+1}. '{doc.title()}' (score: {match_count})")
            print(f"       URL: {doc.url()}")
            print(f"       Preview: {doc.body()[:60]}...")
    else:
        print("  No matching documents found.")


def main():
    print_separator("🔍 SEARCH ENGINE DEMO")
    
    # Create sample documents file
    sample_file = "demo_documents.txt"
    with open(sample_file, 'w') as f:
        f.write("""Title: Introduction to Python
Python programming language tutorial for beginners
Learn Python syntax data structures algorithms


Title: Python Web Development
Build web applications using Python Django Flask
Python backend development REST APIs databases


Title: Data Science with Python
Python data analysis pandas numpy matplotlib
Machine learning scikit-learn tensorflow python


Title: Java Programming Basics
Java programming object oriented design patterns
Java collections algorithms data structures


Title: Machine Learning Fundamentals
Machine learning algorithms neural networks
Deep learning artificial intelligence models""")
    
    try:
        # =====================================================================
        # STEP 1: Initialize Engine
        # =====================================================================
        print_separator("1. Initialize Engine")
        
        engine = Engine()
        print("✓ Engine initialized successfully")
        print(f"✓ Loaded uninteresting words")
        
        stats = engine.get_stats()
        print(f"\nInitial State:")
        print(f"  Documents: {stats['documents']}")
        print(f"  URLs added: {stats['urls_added']}")
        print(f"  Active query: {stats['active_query']}")
        
        # =====================================================================
        # STEP 2: Add Documents from URL
        # =====================================================================
        print_separator("2. Add Documents from URL")
        
        url = f"file://{sample_file}"
        print(f"Adding documents from: {url}")
        
        query = engine.addDocs(url)
        print(f"✓ Documents added successfully")
        
        stats = engine.get_stats()
        print(f"\nUpdated State:")
        print(f"  Documents: {stats['documents']}")
        print(f"  URLs added: {stats['urls_added']}")
        
        # =====================================================================
        # STEP 3: Find Document by Title
        # =====================================================================
        print_separator("3. Find Document by Title")
        
        title_to_find = "Data Science with Python"
        print(f"Searching for: '{title_to_find}'")
        
        doc = engine.findDoc(title_to_find)
        print(f"\n✓ Found document!")
        print(f"  Title: {doc.title()}")
        print(f"  URL: {doc.url()}")
        print(f"  Body: {doc.body()[:100]}...")
        print(f"  Word count: {len(doc.tokens())}")
        
        # Test error case
        print(f"\nTrying to find non-existent document...")
        try:
            engine.findDoc("Nonexistent Title")
        except NotPossibleException as e:
            print(f"✓ Correctly raised exception: {e}")
        
        # =====================================================================
        # STEP 4: Start Query (queryFirst)
        # =====================================================================
        print_separator("4. Start New Query - queryFirst()")
        
        keyword1 = "python"
        print(f"Starting query with keyword: '{keyword1}'")
        
        query = engine.queryFirst(keyword1)
        print_query_results(query, f"Query Results for '{keyword1}'")
        
        # Show document ranking
        if query.size() >= 2:
            print(f"\n  Ranking details:")
            for i in range(min(3, query.size())):
                doc = query.fetch(i)
                count = doc.match_count([keyword1])
                print(f"    '{doc.title()}': contains '{keyword1}' {count} times")
        
        # Test error cases
        print(f"\nTrying query with uninteresting word...")
        try:
            engine.queryFirst("the")
        except NotPossibleException as e:
            print(f"✓ Correctly raised exception: {e}")
        
        # =====================================================================
        # STEP 5: Refine Query (queryMore)
        # =====================================================================
        print_separator("5. Refine Query - queryMore()")
        
        keyword2 = "machine"
        print(f"Refining query by adding keyword: '{keyword2}'")
        print(f"Current keywords: {query.keys()}")
        
        refined_query = engine.queryMore(keyword2)
        print_query_results(refined_query, f"Refined Query Results")
        
        print(f"\n  Filtering effect:")
        print(f"    Original matches: {query.size()}")
        print(f"    After refinement: {refined_query.size()}")
        print(f"    Keywords: {', '.join(refined_query.keys())}")
        
        # Show that all results contain both keywords
        if refined_query.size() > 0:
            print(f"\n  Verification (all docs contain both keywords):")
            for i in range(refined_query.size()):
                doc = refined_query.fetch(i)
                contains_both = doc.contains_all_keywords([keyword1, keyword2])
                print(f"    '{doc.title()}': ✓ {contains_both}")
        
        # Test error cases
        print(f"\nTrying to add duplicate keyword...")
        try:
            engine.queryMore(keyword1)
        except NotPossibleException as e:
            print(f"✓ Correctly raised exception: {e}")
        
        # =====================================================================
        # STEP 6: Add More Documents (updates active query)
        # =====================================================================
        print_separator("6. Add More Documents (Updates Active Query)")
        
        # Create additional documents
        extra_file = "extra_documents.txt"
        with open(extra_file, 'w') as f:
            f.write("""Title: Python Machine Learning Guide
Comprehensive python machine learning tutorial
Neural networks deep learning python libraries


Title: Advanced Python Techniques
Advanced python programming patterns decorators
Metaclasses generators python optimization""")
        
        print(f"Current query state:")
        print(f"  Keywords: {', '.join(refined_query.keys())}")
        print(f"  Matches: {refined_query.size()}")
        
        url2 = f"file://{extra_file}"
        print(f"\nAdding more documents from: {url2}")
        
        updated_query = engine.addDocs(url2)
        print(f"✓ New documents added")
        
        print_query_results(updated_query, "Updated Query Results")
        
        # =====================================================================
        # Final Statistics
        # =====================================================================
        print_separator("📊 Final Statistics")
        
        stats = engine.get_stats()
        print(f"Total documents: {stats['documents']}")
        print(f"URLs added: {stats['urls_added']}")
        print(f"Unique interesting words: {stats['unique_words']}")
        print(f"Active query: {stats['active_query']}")
        print(f"Query keywords: {stats['query_keywords']}")
        print(f"Query matches: {stats['query_matches']}")
        
        # =====================================================================
        # Complete Workflow Example
        # =====================================================================
        print_separator("🎯 Complete Workflow Example")
        
        print("Scenario: Find all documents about Java")
        print("\n1. Query for 'java'")
        query = engine.queryFirst("java")
        print(f"   Found {query.size()} document(s)")
        
        if query.size() > 0:
            print("\n2. Get the top result")
            top_doc = query.fetch(0)
            print(f"   Title: '{top_doc.title()}'")
            
            print("\n3. View the document")
            print(f"   {top_doc.body()[:120]}...")
        
        print_separator("✅ Demo Complete!")
        print("All Engine methods successfully demonstrated:")
        print("  ✓ __init__()    - Engine initialization")
        print("  ✓ addDocs()     - Adding documents from URLs")
        print("  ✓ findDoc()     - Finding documents by title")
        print("  ✓ queryFirst()  - Starting new queries")
        print("  ✓ queryMore()   - Refining queries")
        print("\nThe search engine is fully functional! 🎉")
        print_separator()
        
    finally:
        # Cleanup
        if os.path.exists(sample_file):
            os.remove(sample_file)
        if os.path.exists("extra_documents.txt"):
            os.remove("extra_documents.txt")


if __name__ == "__main__":
    main()
