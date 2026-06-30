from pathlib import Path

import pytest

from comm import Comm, NotPossibleException as CommNotPossibleException
from doc import Doc, NotPossibleException as DocNotPossibleException
from docCnt import DocCnt
from engine import Engine, NotPossibleException as EngineNotPossibleException
from query import Query
from titleTable import (
    DuplicateException,
    NotPossibleException as TitleTableNotPossibleException,
    TitleTable,
)
from wordTable import WordTable


ROOT = Path(__file__).resolve().parent
DOCS_TECH = ROOT / "docs" / "technology.txt"
DOCS_SCIENCE = ROOT / "docs" / "science.txt"

D1_TITLE = "Introduction to Python"
D2_TITLE = "Machine Learning Fundamentals"
D3_TITLE = "Web Development with JavaScript"
D4_TITLE = "Database Systems and SQL"
D5_TITLE = "Cloud Computing Overview"
SCI_QUANTUM_TITLE = "Quantum Mechanics Basics"


def _split_docs(file_path: Path):
    text = file_path.read_text(encoding="utf-8")
    return [chunk.strip() for chunk in text.split("\n\n\n") if chunk.strip()]


@pytest.fixture()
def sample_doc_texts():
    docs = _split_docs(DOCS_TECH)
    assert len(docs) == 5
    return {
        "D1": docs[0],
        "D2": docs[1],
        "D3": docs[2],
        "D4": docs[3],
        "D5": docs[4],
    }


@pytest.fixture()
def sample_docs_urls():
    return [f"file://{DOCS_TECH}", f"file://{DOCS_SCIENCE}"]


@pytest.fixture()
def engine_with_docs(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    return e


# -----------------------------------------------------------------------------
# 1. Comm — getDocs
# -----------------------------------------------------------------------------


def test_comm_01_valid_file_url_returns_iterator(sample_docs_urls):
    docs = list(Comm.getDocs(sample_docs_urls[0]))
    assert len(docs) == 5
    assert all(isinstance(x, str) and x is not None for x in docs)


@pytest.mark.parametrize("bad_url", [None, "", "   ", "en.wikipedia.org/wiki/Python", "not_a_url_at_all"])
def test_comm_02_to_06_invalid_inputs_raise(bad_url):
    with pytest.raises(CommNotPossibleException):
        list(Comm.getDocs(bad_url))


def test_comm_07_unreachable_or_missing_raises(tmp_path):
    missing = tmp_path / "missing_docs.txt"
    with pytest.raises(CommNotPossibleException):
        list(Comm.getDocs(f"file://{missing}"))


def test_comm_08_valid_url_with_no_docs_returns_empty_iterator(tmp_path):
    empty_docs = tmp_path / "blank.txt"
    empty_docs.write_text("\n\n\n   \n\n\n", encoding="utf-8")
    docs = list(Comm.getDocs(f"file://{empty_docs}"))
    assert docs == []


# -----------------------------------------------------------------------------
# 2. Doc — constructor and accessors
# -----------------------------------------------------------------------------


def test_doc_01_and_02_valid_docs_construct(sample_doc_texts):
    d1 = Doc(sample_doc_texts["D1"])
    d2 = Doc(sample_doc_texts["D2"])
    assert d1.title() == D1_TITLE
    assert d2.title() == D2_TITLE


@pytest.mark.parametrize("bad_input", [None, "", "   \t\n"])
def test_doc_03_to_05_invalid_doc_input_raises(bad_input):
    with pytest.raises(DocNotPossibleException):
        Doc(bad_input)


def test_doc_06_title_with_empty_body_is_valid():
    d = Doc(f"{D1_TITLE}\n")
    assert d.title() == D1_TITLE
    assert d.body() == ""


def test_doc_07_no_parseable_title_expected_failure_against_spec():
    with pytest.raises(DocNotPossibleException):
        Doc("no title marker just body text")


@pytest.mark.parametrize(
    "doc_key, expected_title",
    [
        ("D1", D1_TITLE),
        ("D4", D4_TITLE),
    ],
)
def test_doc_08_to_10_title_checks(sample_doc_texts, doc_key, expected_title):
    d = Doc(sample_doc_texts[doc_key])
    assert d.title() == expected_title
    assert d.title() is not None


@pytest.mark.parametrize(
    "doc_key, must_contain",
    [
        ("D2", "learning"),
        ("D5", "cloud"),
    ],
)
def test_doc_11_to_13_body_checks(sample_doc_texts, doc_key, must_contain):
    d = Doc(sample_doc_texts[doc_key])
    assert must_contain.lower() in d.body().lower()
    assert d.body() is not None


# -----------------------------------------------------------------------------
# 3. DocCnt — compare behavior
# -----------------------------------------------------------------------------


def _mk_doc(title="T", body="word word"):
    return Doc(f"Title: {title}\n{body}")


def test_dcnt_01_null_argument():
    dc = DocCnt(_mk_doc(), 1)
    with pytest.raises(TypeError):
        _ = (dc == None)


def test_dcnt_02_non_doccnt_argument():
    dc = DocCnt(_mk_doc(), 1)
    with pytest.raises(TypeError):
        _ = (dc == "python")


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 7, -1),
        (3, 3, 0),
        (7, 2, 1),
        (0, 0, 0),
    ],
)
def test_dcnt_03_to_06_count_ordering(a, b, expected):
    dc1 = DocCnt(_mk_doc("A"), a)
    dc2 = DocCnt(_mk_doc("B"), b)
    if expected == -1:
        assert dc1 < dc2
    elif expected == 0:
        assert dc1 == dc2
    else:
        assert dc1 > dc2


def test_dcnt_07_self_comparison():
    dc = DocCnt(_mk_doc(), 5)
    assert dc == dc


# -----------------------------------------------------------------------------
# 4. Engine — all methods
# -----------------------------------------------------------------------------


def test_eng_01_constructor_normal_init():
    e = Engine()
    assert e._word_table.isInteresting("the") is False
    assert e._word_table.isInteresting("and") is False
    assert e._word_table.isInteresting("is") is False


def test_eng_02_words_file_missing(monkeypatch):
    monkeypatch.setattr(WordTable, "_UNINTERESTING_FILE", "definitely_missing_words_file.txt")
    with pytest.raises(EngineNotPossibleException):
        Engine()


def test_eng_03_words_file_empty(monkeypatch, tmp_path):
    empty_words = tmp_path / "empty_words.txt"
    empty_words.write_text("", encoding="utf-8")
    monkeypatch.setattr(WordTable, "_UNINTERESTING_FILE", str(empty_words))
    e = Engine()
    assert e._word_table.isInteresting("the") is True


def test_eng_04_queryfirst_valid(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    assert set(q.keys()) == {"data"}


def test_eng_05_queryfirst_matches_multiple_docs(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    assert q.size() >= 2


@pytest.mark.parametrize("bad_word", ["the", "123!!", None, ""])
def test_eng_06_to_09_queryfirst_invalid_inputs(engine_with_docs, bad_word):
    with pytest.raises(EngineNotPossibleException):
        engine_with_docs.queryFirst(bad_word)


def test_eng_10_queryfirst_word_in_no_doc(engine_with_docs):
    q = engine_with_docs.queryFirst("blockchain")
    assert q.size() == 0


def test_eng_11_queryfirst_resets_key(engine_with_docs):
    engine_with_docs.queryFirst("data")
    q2 = engine_with_docs.queryFirst("database")
    assert set(q2.keys()) == {"database"}


def test_eng_12_querymore_narrows_results(engine_with_docs):
    q1 = engine_with_docs.queryFirst("data")
    s1 = q1.size()
    q2 = engine_with_docs.queryMore("sql")
    assert set(q2.keys()) == {"data", "sql"}
    assert q2.size() <= s1


def test_eng_13_querymore_keeps_d1_for_python_and_syntax(engine_with_docs):
    q = engine_with_docs.queryFirst("python")
    q = engine_with_docs.queryMore("syntax")
    titles = [q.fetch(i).title() for i in range(q.size())]
    assert D1_TITLE in titles


def test_eng_14_querymore_duplicate_key_raises(engine_with_docs):
    engine_with_docs.queryFirst("data")
    with pytest.raises(EngineNotPossibleException):
        engine_with_docs.queryMore("data")


def test_eng_15_querymore_without_queryfirst_raises():
    e = Engine()
    with pytest.raises(EngineNotPossibleException):
        e.queryMore("python")


@pytest.mark.parametrize("bad_word", ["and", None])
def test_eng_16_17_querymore_invalid_inputs(engine_with_docs, bad_word):
    engine_with_docs.queryFirst("data")
    with pytest.raises(EngineNotPossibleException):
        engine_with_docs.queryMore(bad_word)


def test_eng_18_19_finddoc_found(engine_with_docs):
    d1 = engine_with_docs.findDoc(D1_TITLE)
    d4 = engine_with_docs.findDoc(D4_TITLE)
    assert d1.title() == D1_TITLE
    assert d4.title() == D4_TITLE


@pytest.mark.parametrize("bad_title", ["Introduction to Cooking", None, ""])
def test_eng_20_to_22_finddoc_invalid(engine_with_docs, bad_title):
    with pytest.raises(EngineNotPossibleException):
        engine_with_docs.findDoc(bad_title)


def test_eng_23_adddocs_no_active_query_returns_empty_query(sample_docs_urls):
    e = Engine()
    q = e.addDocs(sample_docs_urls[0])
    assert isinstance(q, Query)


def test_eng_24_adddocs_with_active_query_returns_matches(sample_docs_urls):
    e = Engine()
    e.queryFirst("quantum")
    q = e.addDocs(sample_docs_urls[1])
    titles = [q.fetch(i).title() for i in range(q.size())]
    assert SCI_QUANTUM_TITLE in titles


def test_eng_25_duplicate_url_raises(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    with pytest.raises(EngineNotPossibleException):
        e.addDocs(sample_docs_urls[0])


@pytest.mark.parametrize("bad_url", [None, "not_a_url"])
def test_eng_26_27_adddocs_invalid_url_raises(bad_url):
    e = Engine()
    with pytest.raises(EngineNotPossibleException):
        e.addDocs(bad_url)


# -----------------------------------------------------------------------------
# 5. Query — all methods
# -----------------------------------------------------------------------------


def test_qry_01_single_keyword(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    assert set(q.keys()) == {"data"}


def test_qry_02_two_keywords(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    q = engine_with_docs.queryMore("sql")
    assert set(q.keys()) == {"data", "sql"}


def test_qry_03_no_match_query_keeps_key(engine_with_docs):
    q = engine_with_docs.queryFirst("blockchain")
    assert set(q.keys()) == {"blockchain"}
    assert q.keys() is not None


def test_qry_04_word_in_multiple_docs(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    assert q.size() == 3


def test_qry_05_word_in_no_docs(engine_with_docs):
    q = engine_with_docs.queryFirst("blockchain")
    assert q.size() == 0


def test_qry_06_refining_narrows_results(engine_with_docs):
    q1 = engine_with_docs.queryFirst("database")
    s1 = q1.size()
    q2 = engine_with_docs.queryMore("sql")
    assert q2.size() <= s1


def test_qry_07_08_fetch_ranking(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    assert q.fetch(0).title() == D2_TITLE
    assert q.fetch(1).title() == D4_TITLE


def test_qry_09_fetch_last_index_valid(engine_with_docs):
    q = engine_with_docs.queryFirst("data")
    d = q.fetch(q.size() - 1)
    assert isinstance(d, Doc)


@pytest.mark.parametrize("index_factory", [lambda q: q.size(), lambda q: -1])
def test_qry_10_11_invalid_fetch_indices(engine_with_docs, index_factory):
    q = engine_with_docs.queryFirst("data")
    with pytest.raises(IndexError):
        q.fetch(index_factory(q))


def test_qry_12_fetch_when_empty_raises(engine_with_docs):
    q = engine_with_docs.queryFirst("blockchain")
    with pytest.raises(IndexError):
        q.fetch(0)


def test_qry_13_adddoc_all_keywords_present_in_h():
    q = Query({"python"})
    before = q.size()
    d = Doc("Title: T\npython sort sort")
    q.addDoc(d, {"python": 1, "sort": 2})
    assert q.size() == before + 1


def test_qry_14_adddoc_missing_keyword_not_added():
    q = Query({"python", "climate"})
    before = q.size()
    d = Doc("Title: T\npython only")
    q.addDoc(d, {"python": 2})
    assert q.size() == before


def test_qry_15_adddoc_empty_hashtable_not_added():
    q = Query({"python"})
    before = q.size()
    d = Doc("Title: T\nno keywords here")
    q.addDoc(d, {})
    assert q.size() == before


# -----------------------------------------------------------------------------
# 6. TitleTable — all methods
# -----------------------------------------------------------------------------


def test_tt_01_constructor_empty_lookup_raises():
    tt = TitleTable()
    with pytest.raises(TitleTableNotPossibleException):
        tt.lookup(D1_TITLE)


def test_tt_02_to_03_add_and_lookup(sample_doc_texts):
    tt = TitleTable()
    docs = [Doc(sample_doc_texts[k]) for k in ["D1", "D2", "D3", "D4", "D5"]]
    for d in docs:
        tt.addDoc(d)
    assert tt.lookup(D1_TITLE).title() == D1_TITLE
    assert tt.lookup(D5_TITLE).title() == D5_TITLE


def test_tt_04_duplicate_title_raises(sample_doc_texts):
    tt = TitleTable()
    d1 = Doc(sample_doc_texts["D1"])
    ddup = Doc(f"Title: {D1_TITLE}\nother body")
    tt.addDoc(d1)
    with pytest.raises(DuplicateException):
        tt.addDoc(ddup)


def test_tt_05_add_same_doc_twice_raises(sample_doc_texts):
    tt = TitleTable()
    d1 = Doc(sample_doc_texts["D1"])
    tt.addDoc(d1)
    with pytest.raises(DuplicateException):
        tt.addDoc(d1)


@pytest.mark.parametrize("title", [D2_TITLE, D5_TITLE])
def test_tt_06_07_exact_lookup(sample_doc_texts, title):
    tt = TitleTable()
    for k in ["D1", "D2", "D3", "D4", "D5"]:
        tt.addDoc(Doc(sample_doc_texts[k]))
    assert tt.lookup(title).title() == title


@pytest.mark.parametrize("bad_title", ["Introduction to Quantum Computing", None, ""])
def test_tt_08_to_10_invalid_lookup(sample_doc_texts, bad_title):
    tt = TitleTable()
    tt.addDoc(Doc(sample_doc_texts["D1"]))
    with pytest.raises(TitleTableNotPossibleException):
        tt.lookup(bad_title)


def test_tt_11_lookup_on_empty_raises():
    tt = TitleTable()
    with pytest.raises(TitleTableNotPossibleException):
        tt.lookup(D1_TITLE)


# -----------------------------------------------------------------------------
# 7. WordTable — all methods
# -----------------------------------------------------------------------------


def test_wt_01_file_present():
    wt = WordTable()
    assert wt.isInteresting("the") is False
    assert wt.isInteresting("python") is True


def test_wt_02_file_missing(monkeypatch):
    monkeypatch.setattr(WordTable, "_UNINTERESTING_FILE", "definitely_missing_words_file.txt")
    with pytest.raises(DocNotPossibleException):
        WordTable()


def test_wt_03_empty_file(monkeypatch, tmp_path):
    p = tmp_path / "empty_words.txt"
    p.write_text("", encoding="utf-8")
    monkeypatch.setattr(WordTable, "_UNINTERESTING_FILE", str(p))
    wt = WordTable()
    assert wt.isInteresting("the") is True


@pytest.mark.parametrize(
    "word, expected",
    [
        ("python", True),
        ("learning", True),
        ("the", False),
        ("and", False),
        (None, False),
        ("", False),
        ("java2!", False),
        ("   ", False),
    ],
)
def test_wt_04_to_11_isinteresting(word, expected):
    wt = WordTable()
    assert wt.isInteresting(word) is expected


def test_wt_12_to_16_adddoc_indexing(sample_doc_texts):
    wt = WordTable()
    d1 = Doc(sample_doc_texts["D1"])
    d2 = Doc(sample_doc_texts["D2"])

    wt.addDoc(d1)
    assert len(wt.lookup("python")) >= 1
    assert wt.lookup("the") == []

    wt.addDoc(d2)
    neural = wt.lookup("neural")
    assert len(neural) >= 1
    assert max(dc.cnt for dc in neural) >= 1

    dud = Doc("Title: Stop Words\nthe and is for of")
    h = wt.addDoc(dud)
    assert h == {}


def test_wt_17_to_21_lookup_counts(sample_doc_texts):
    wt = WordTable()
    d1 = Doc(sample_doc_texts["D1"])
    d2 = Doc(sample_doc_texts["D2"])
    d3 = Doc(sample_doc_texts["D3"])
    d4 = Doc(sample_doc_texts["D4"])
    d5 = Doc(sample_doc_texts["D5"])

    wt.addDoc(d1)
    wt.addDoc(d2)
    wt.addDoc(d3)
    wt.addDoc(d4)
    wt.addDoc(d5)

    data_hits = wt.lookup("data")
    assert len(data_hits) == 3
    assert max(dc.cnt for dc in data_hits) == 2

    database_hits = wt.lookup("database")
    assert len(database_hits) == 1
    assert database_hits[0].doc.title() == D4_TITLE

    cloud_hits = wt.lookup("cloud")
    assert len(cloud_hits) == 1
    assert cloud_hits[0].doc.title() == D5_TITLE

    assert wt.lookup("blockchain") == []

    neural_hits = wt.lookup("neural")
    assert len(neural_hits) == 1
    assert neural_hits[0].cnt == 1


def test_wt_22_to_26_adddoc_returned_hashtable(sample_doc_texts):
    wt = WordTable()
    d1 = Doc(sample_doc_texts["D1"])
    d4 = Doc(sample_doc_texts["D4"])
    d3 = Doc(sample_doc_texts["D3"])
    d2 = Doc(sample_doc_texts["D2"])

    h1 = wt.addDoc(d1)
    assert h1.get("python", 0) > 0
    assert h1.get("syntax", 0) > 0

    h4 = wt.addDoc(d4)
    assert h4.get("sql", 0) > 0

    h3 = wt.addDoc(d3)
    assert "the" not in h3

    h2 = wt.addDoc(d2)
    assert h2.get("learning", 0) == 6

    dud = Doc("Title: Stop Words\nthe and is")
    hd = wt.addDoc(dud)
    assert hd == {}


# -----------------------------------------------------------------------------
# Integration scenarios
# -----------------------------------------------------------------------------


def test_int_01_full_flow_data_top_is_d2(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    q = e.queryFirst("data")
    assert q.fetch(0).title() == D2_TITLE


def test_int_02_refine_to_single_result(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    q = e.queryFirst("database")
    q = e.queryMore("sql")
    assert q.size() == 1
    assert q.fetch(0).title() == D4_TITLE


def test_int_03_finddoc_after_adddocs(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    d = e.findDoc(D3_TITLE)
    assert d.title() == D3_TITLE


def test_int_04_adddocs_updates_active_query(sample_docs_urls):
    e = Engine()
    e.queryFirst("quantum")
    q = e.addDocs(sample_docs_urls[1])
    titles = [q.fetch(i).title() for i in range(q.size())]
    assert SCI_QUANTUM_TITLE in titles


def test_int_05_duplicate_url_rejected(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    with pytest.raises(EngineNotPossibleException):
        e.addDocs(sample_docs_urls[0])


def test_int_06_queryfirst_resets_key(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    e.queryFirst("data")
    e.queryMore("sql")
    q = e.queryFirst("cloud")
    assert set(q.keys()) == {"cloud"}


def test_int_07_documents_ordered_by_match_count(sample_docs_urls):
    e = Engine()
    e.addDocs(sample_docs_urls[0])
    q = e.queryFirst("data")
    assert q.fetch(0).title() == D2_TITLE
