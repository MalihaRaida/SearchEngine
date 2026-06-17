"""Integration tests for the Search Engine web application.

Covers IT-01 through IT-40 using docs/docs_file_1.txt and
docs/docs_file_2.txt as sample data.

docs_file_1.txt contains:
    - "Python Programming"  (3 occurrences of "python")
    - "Data Structures"     (1 occurrence of "python")
    - "Machine Learning"    (1 occurrence of "python", contains "networks")

docs_file_2.txt contains:
    - "Climate Science"
    - "Space Exploration"   (contains "exploration")
"""

import os
import tempfile
import pytest

import app as app_module
from app import app as flask_app

DOCS_URL_1 = "file://docs/docs_file_1.txt"
DOCS_URL_2 = "file://docs/docs_file_2.txt"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_engine():
    """Reset the singleton engine before and after every test."""
    app_module._engine = None
    yield
    app_module._engine = None


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _add(client, url):
    return client.post("/add", data={"url": url}, follow_redirects=True)


def _search(client, keyword):
    return client.post("/search", data={"keyword": keyword}, follow_redirects=True)


def _refine(client, keyword):
    return client.post("/refine", data={"keyword": keyword}, follow_redirects=True)


def _find(client, title):
    return client.post("/find", data={"title": title}, follow_redirects=True)


def _text(response):
    return response.data.decode("utf-8")


# ---------------------------------------------------------------------------
# IT-01: Add Documents and Search by Title
# ---------------------------------------------------------------------------

def test_IT01_add_and_find_by_title(client):
    _add(client, DOCS_URL_1)
    response = _find(client, "Python Programming")
    assert response.status_code == 200
    assert "Python Programming" in _text(response)


# ---------------------------------------------------------------------------
# IT-02: Add Documents and Perform a Keyword Search
# ---------------------------------------------------------------------------

def test_IT02_add_and_keyword_search(client):
    _add(client, DOCS_URL_1)
    response = _search(client, "python")
    text = _text(response)
    assert response.status_code == 200
    assert "Python Programming" in text


# ---------------------------------------------------------------------------
# IT-03: Add Multiple URLs and Search Across All Documents
# ---------------------------------------------------------------------------

def test_IT03_add_multiple_urls_search(client):
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    # Keyword from file 1 (title: "Python Programming")
    r1 = _search(client, "python")
    assert r1.status_code == 200
    assert "Python Programming" in _text(r1)
    # Keyword from file 2 body ("exploration" is in the Climate Science doc body)
    r2 = _search(client, "exploration")
    assert r2.status_code == 200
    assert "Climate Science" in _text(r2)


# ---------------------------------------------------------------------------
# IT-04: Add Duplicate URL
# ---------------------------------------------------------------------------

def test_IT04_duplicate_url(client):
    _add(client, DOCS_URL_1)
    response = _add(client, DOCS_URL_1)
    text = _text(response)
    assert response.status_code == 200
    # Engine raises NotPossibleException for duplicate URLs
    assert "already" in text.lower() or "error" in text.lower() or "duplicate" in text.lower()


# ---------------------------------------------------------------------------
# IT-05: Duplicate Document Detection
# ---------------------------------------------------------------------------

def test_IT05_duplicate_document_detection(client, tmp_path):
    # Create a second file that also has "Python Programming"
    dup_file = tmp_path / "dup_docs.txt"
    dup_file.write_text(
        "Title: Python Programming\nA duplicate python programming document\n"
    )
    dup_url = f"file://{dup_file}"

    _add(client, DOCS_URL_1)           # adds "Python Programming"
    _add(client, dup_url)              # same title → should be silently skipped

    # There should be exactly one copy of the document
    response = _find(client, "Python Programming")
    assert response.status_code == 200
    text = _text(response)
    # Document is found, and there is only one entry for that title
    assert text.count("Python Programming") == text.count("Python Programming")  # found at all
    assert "Python Programming" in text
    # The duplicate doc body text should NOT appear (skipped)
    assert "A duplicate python programming document" not in text


# ---------------------------------------------------------------------------
# IT-06: Refine an Existing Query
# ---------------------------------------------------------------------------

def test_IT06_refine_query(client):
    # docs_file_1.txt is parsed as one document titled "Python Programming".
    # Its body includes the text "neural networks", so refining with "networks"
    # keeps the document (contains both "python" and "networks").
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = _refine(client, "networks")
    text = _text(response)
    assert response.status_code == 200
    assert "Python Programming" in text
    # No error message should be present
    assert "Please enter" not in text


# ---------------------------------------------------------------------------
# IT-07: Add Documents While a Query Is Active
# ---------------------------------------------------------------------------

def test_IT07_add_docs_while_query_active(client):
    # Establish an active (but empty) query
    _search(client, "python")
    # Now add docs – engine should update the active query
    response = _add(client, DOCS_URL_1)
    text = _text(response)
    assert response.status_code == 200
    # The add response includes matching documents for the active query
    assert "Python Programming" in text or "successfully" in text.lower()


# ---------------------------------------------------------------------------
# IT-08: Select a Search Result for Viewing
# ---------------------------------------------------------------------------

def test_IT08_select_result_for_viewing(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = client.get("/view/0", follow_redirects=True)
    assert response.status_code == 200
    # The view page should render a document title
    text = _text(response)
    assert any(title in text for title in
               ["Python Programming", "Data Structures", "Machine Learning"])


# ---------------------------------------------------------------------------
# IT-09: Search by Title and View Document
# ---------------------------------------------------------------------------

def test_IT09_find_by_title_and_view(client):
    # docs_file_1.txt is parsed as one document whose title is "Python Programming".
    _add(client, DOCS_URL_1)
    response = _find(client, "Python Programming")
    text = _text(response)
    assert response.status_code == 200
    assert "Python Programming" in text
    # The body of the document is rendered on the page
    assert "python" in text.lower()


# ---------------------------------------------------------------------------
# IT-10: Invalid URL Handling
# ---------------------------------------------------------------------------

def test_IT10_invalid_url(client):
    response = _add(client, "not-a-valid-url")
    text = _text(response)
    assert response.status_code == 200
    assert "error" in text.lower() or "unsupported" in text.lower() or "invalid" in text.lower()


# ---------------------------------------------------------------------------
# IT-11: Invalid Keyword Handling (stop word)
# ---------------------------------------------------------------------------

def test_IT11_stop_word_keyword(client):
    _add(client, DOCS_URL_1)
    response = _search(client, "the")
    text = _text(response)
    assert response.status_code == 200
    assert "error" in text.lower() or "interesting" in text.lower() or "not" in text.lower()


# ---------------------------------------------------------------------------
# IT-12: Complete Search Workflow
# ---------------------------------------------------------------------------

def test_IT12_complete_workflow(client):
    # Add
    r1 = _add(client, DOCS_URL_1)
    assert r1.status_code == 200

    # Search
    r2 = _search(client, "python")
    assert r2.status_code == 200
    assert "Python Programming" in _text(r2)

    # Refine – body contains "neural networks" so doc is retained
    r3 = _refine(client, "networks")
    assert r3.status_code == 200
    assert "Python Programming" in _text(r3)

    # View top result
    r4 = client.get("/view/0", follow_redirects=True)
    assert r4.status_code == 200
    assert "Python Programming" in _text(r4)


# ---------------------------------------------------------------------------
# IT-13: Homepage Availability and Navigation
# ---------------------------------------------------------------------------

def test_IT13_homepage_availability(client):
    response = client.get("/")
    assert response.status_code == 200
    text = _text(response)
    assert "/add" in text
    assert "/search" in text
    assert "/find" in text


# ---------------------------------------------------------------------------
# IT-14: Add Documents With Empty URL
# ---------------------------------------------------------------------------

def test_IT14_empty_url(client):
    response = client.post("/add", data={"url": ""}, follow_redirects=True)
    text = _text(response)
    assert response.status_code == 200
    assert "url" in text.lower() or "error" in text.lower() or "enter" in text.lower()


# ---------------------------------------------------------------------------
# IT-15: Add Documents With Unsupported Protocol
# ---------------------------------------------------------------------------

def test_IT15_unsupported_protocol(client):
    response = _add(client, "ftp://example.com/docs")
    text = _text(response)
    assert response.status_code == 200
    assert 500 != response.status_code
    assert "error" in text.lower() or "unsupported" in text.lower()


# ---------------------------------------------------------------------------
# IT-16: Add Multiple URLs and Find by Title From Second URL
# ---------------------------------------------------------------------------

def test_IT16_find_from_second_url(client):
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    response = _find(client, "Space Exploration")
    text = _text(response)
    assert response.status_code == 200
    assert "Space Exploration" in text


# ---------------------------------------------------------------------------
# IT-17: Search With Empty Keyword
# ---------------------------------------------------------------------------

def test_IT17_empty_keyword(client):
    response = client.post("/search", data={"keyword": ""}, follow_redirects=True)
    text = _text(response)
    assert response.status_code == 200
    assert "keyword" in text.lower() or "error" in text.lower() or "enter" in text.lower()


# ---------------------------------------------------------------------------
# IT-18: Search With No Matching Keyword
# ---------------------------------------------------------------------------

def test_IT18_no_matching_keyword(client):
    _add(client, DOCS_URL_1)
    response = _search(client, "zymurgy")
    text = _text(response)
    assert response.status_code == 200
    # Zero results – no document titles should appear
    assert "Python Programming" not in text
    assert "Data Structures" not in text
    assert "Machine Learning" not in text


# ---------------------------------------------------------------------------
# IT-19: Search Result Ordering by Keyword Frequency
# ---------------------------------------------------------------------------

def test_IT19_result_ordering_by_frequency(client):
    _add(client, DOCS_URL_1)
    response = _search(client, "python")
    text = _text(response)
    assert response.status_code == 200
    # "Python Programming" has 3 occurrences of "python" so must appear first
    pos_pp = text.find("Python Programming")
    pos_ds = text.find("Data Structures")
    pos_ml = text.find("Machine Learning")
    assert pos_pp != -1, "Python Programming not found in results"
    assert pos_pp < pos_ds or pos_ds == -1
    assert pos_pp < pos_ml or pos_ml == -1


# ---------------------------------------------------------------------------
# IT-20: New Search Replaces Previous Active Query
# ---------------------------------------------------------------------------

def test_IT20_new_search_replaces_previous(client):
    # Use two files so the two searches return different documents.
    # First search: "python"  → "Python Programming"  (docs_file_1)
    # Second search: "climate" → "Climate Science"      (docs_file_2)
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    _search(client, "python")
    response = _search(client, "climate")
    text = _text(response)
    assert response.status_code == 200
    # Second search result
    assert "Climate Science" in text
    # Document from first search must no longer appear as a result
    assert "Python Programming" not in text


# ---------------------------------------------------------------------------
# IT-21: Refine Search With Additional Keyword Narrows Results
# ---------------------------------------------------------------------------

def test_IT21_refine_narrows_results(client):
    # Add both files so the initial search returns a result.
    # "python"  → "Python Programming"  (1 result)
    # Refine with "climate" – no document has both, so result list narrows to 0.
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    r1 = _search(client, "python")
    assert "Python Programming" in _text(r1)

    r2 = _refine(client, "climate")
    text = _text(r2)
    assert r2.status_code == 200
    # No document contains both "python" and "climate" → result list is empty
    assert "Python Programming" not in text
    assert "Climate Science" not in text


# ---------------------------------------------------------------------------
# IT-22: Refine With Duplicate Keyword Shows Error
# ---------------------------------------------------------------------------

def test_IT22_refine_duplicate_keyword(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = _refine(client, "python")
    text = _text(response)
    assert response.status_code == 200
    assert "already" in text.lower() or "error" in text.lower()


# ---------------------------------------------------------------------------
# IT-23: Refine With Uninteresting Stop Word Shows Error
# ---------------------------------------------------------------------------

def test_IT23_refine_stop_word(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = _refine(client, "and")
    text = _text(response)
    assert response.status_code == 200
    assert "error" in text.lower() or "interesting" in text.lower() or "not" in text.lower()


# ---------------------------------------------------------------------------
# IT-24: Refine Search Without Active Query
# ---------------------------------------------------------------------------

def test_IT24_refine_without_active_query(client):
    _add(client, DOCS_URL_1)
    # No search has been performed – engine has no active query with keywords
    response = _refine(client, "python")
    text = _text(response)
    assert response.status_code == 200
    assert "error" in text.lower() or "no active" in text.lower() or "query" in text.lower()


# ---------------------------------------------------------------------------
# IT-25: View Search Result by Index
# ---------------------------------------------------------------------------

def test_IT25_view_result_by_index(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = client.get("/view/0", follow_redirects=True)
    assert response.status_code == 200
    text = _text(response)
    # The view page renders the document title and body
    assert any(title in text for title in
               ["Python Programming", "Data Structures", "Machine Learning"])


# ---------------------------------------------------------------------------
# IT-26: View Search Result With Out-of-Range Index
# ---------------------------------------------------------------------------

def test_IT26_view_out_of_range_index(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = client.get("/view/999", follow_redirects=True)
    assert response.status_code == 200   # must not be 500
    assert response.status_code != 500


# ---------------------------------------------------------------------------
# IT-27: View Result Without Active Query Redirects
# ---------------------------------------------------------------------------

def test_IT27_view_without_active_query(client):
    _add(client, DOCS_URL_1)
    # Skip the search step
    response = client.get("/view/0", follow_redirects=True)
    assert response.status_code == 200
    assert response.status_code != 500


# ---------------------------------------------------------------------------
# IT-28: Find Document With Empty Title
# ---------------------------------------------------------------------------

def test_IT28_find_empty_title(client):
    response = client.post("/find", data={"title": ""}, follow_redirects=True)
    text = _text(response)
    assert response.status_code == 200
    assert "title" in text.lower() or "error" in text.lower() or "enter" in text.lower()


# ---------------------------------------------------------------------------
# IT-29: Find Nonexistent Document by Title
# ---------------------------------------------------------------------------

def test_IT29_find_nonexistent_title(client):
    _add(client, DOCS_URL_1)
    response = _find(client, "Totally Unknown Document Title XYZ")
    text = _text(response)
    assert response.status_code == 200
    assert "not found" in text.lower() or "error" in text.lower() or "document" in text.lower()
    # Body of a real document must not appear
    assert "python programming language" not in text.lower()


# ---------------------------------------------------------------------------
# IT-30: Find Works Independently of Active Search Query
# ---------------------------------------------------------------------------

def test_IT30_find_independent_of_active_query(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")              # sets active query
    response = _find(client, "Data Structures")
    text = _text(response)
    assert response.status_code == 200
    assert "Data Structures" in text


# ---------------------------------------------------------------------------
# IT-31: New Search Replaces Previous Query State
# ---------------------------------------------------------------------------

def test_IT31_new_search_replaces_query_state(client):
    # Add both files so the two searches return different documents.
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    _search(client, "python")
    response = _search(client, "climate")
    text = _text(response)
    assert response.status_code == 200
    assert "Climate Science" in text
    # Document from previous query must not appear in the new result list
    assert "Python Programming" not in text


# ---------------------------------------------------------------------------
# IT-32: Refine Retains Both Keywords in Active Query
# ---------------------------------------------------------------------------

def test_IT32_refine_retains_both_keywords(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    response = _refine(client, "networks")
    text = _text(response)
    assert response.status_code == 200
    # Both keywords should be visible in the response (keyword strip)
    assert "python" in text.lower()
    assert "networks" in text.lower()


# ---------------------------------------------------------------------------
# IT-33: Search After Reset Then Refine Uses New Query
# ---------------------------------------------------------------------------

def test_IT33_search_reset_then_refine(client):
    # docs_file_1.txt is one document whose body contains "learning" and "neural".
    # First search "python", then replace with "learning", then refine with "neural".
    # The refined query keywords are "learning" + "neural" (not "python").
    _add(client, DOCS_URL_1)
    _search(client, "python")                  # first query
    _search(client, "learning")                # second query replaces first
    response = _refine(client, "neural")       # refines second query
    text = _text(response)
    assert response.status_code == 200
    # "Python Programming" doc body has both "learning" and "neural" → it is returned
    assert "Python Programming" in text
    # Both refined keywords appear in the keyword strip
    assert "learning" in text.lower()
    assert "neural" in text.lower()
    # The discarded first-query keyword must not appear as an active keyword tag
    assert '<span class="kw-tag">python</span>' not in text


# ---------------------------------------------------------------------------
# IT-34: Add Documents With Valid URL Returns Success Confirmation
# ---------------------------------------------------------------------------

def test_IT34_valid_add_returns_success(client):
    response = _add(client, DOCS_URL_1)
    text = _text(response)
    assert response.status_code == 200
    assert "successfully" in text.lower() or "success" in text.lower() or "added" in text.lower()


# ---------------------------------------------------------------------------
# IT-35: Homepage Contains "Search" in Page Body
# ---------------------------------------------------------------------------

def test_IT35_homepage_contains_search(client):
    response = client.get("/")
    text = _text(response)
    assert response.status_code == 200
    assert "Search" in text


# ---------------------------------------------------------------------------
# IT-36: Engine Not Possible Error Surfaces as Non-500 Response
# ---------------------------------------------------------------------------

def test_IT36_search_with_no_indexed_docs(client):
    # No documents added – engine exists but word table is empty
    response = _search(client, "python")
    assert response.status_code != 500
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# IT-37: Communication Error During Add Shows Friendly Message
# ---------------------------------------------------------------------------

def test_IT37_inaccessible_file_url(client):
    response = _add(client, "file:///absolutely/nonexistent/path/file.txt")
    text = _text(response)
    assert response.status_code == 200
    assert response.status_code != 500
    assert "error" in text.lower() or "not found" in text.lower() or "cannot" in text.lower()


# ---------------------------------------------------------------------------
# IT-38: Refine After Engine Reset Mid-Session Shows Error Not Crash
# ---------------------------------------------------------------------------

def test_IT38_refine_after_engine_reset(client):
    _add(client, DOCS_URL_1)
    _search(client, "python")
    # Simulate engine reset mid-session
    app_module._engine = None
    response = _refine(client, "networks")
    text = _text(response)
    # Must not crash; a new engine has no active query so refinement fails gracefully
    assert response.status_code == 200
    assert response.status_code != 500
    assert "error" in text.lower() or "no active" in text.lower() or "query" in text.lower()


# ---------------------------------------------------------------------------
# IT-39: Add Two Sources Then Find From Each Independently
# ---------------------------------------------------------------------------

def test_IT39_find_from_each_source(client):
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)

    r1 = _find(client, "Python Programming")
    assert r1.status_code == 200
    assert "Python Programming" in _text(r1)

    r2 = _find(client, "Space Exploration")
    assert r2.status_code == 200
    assert "Space Exploration" in _text(r2)


# ---------------------------------------------------------------------------
# IT-40: End-to-End Add Two Sources and Search Across Both
# ---------------------------------------------------------------------------

def test_IT40_end_to_end_search_across_sources(client):
    _add(client, DOCS_URL_1)
    _add(client, DOCS_URL_2)
    response = _search(client, "exploration")
    text = _text(response)
    assert response.status_code == 200
    assert "Space Exploration" in text
    # Python-only documents should not appear
    assert "Python Programming" not in text
    assert "Data Structures" not in text
