"""Flask web application for the Search Engine (FR7)."""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

from engine import Engine, NotPossibleException

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global engine instance (single-user application)
_engine: Engine = None


def get_engine() -> Engine:
    """Return the singleton Engine, initialising it on first call."""
    global _engine
    if _engine is None:
        _engine = Engine()
    return _engine


def _query_to_list(query) -> list:
    """Convert a Query into a list of dicts for template rendering."""
    results = []
    for i in range(query.size()):
        doc = query.fetch(i)
        results.append({
            "idx": i,
            "title": doc.title(),
            "preview": doc.body()[:150].replace("\n", " "),
            "url": doc.url() or "",
        })
    return results


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    message = None
    error = None
    results = []
    query_keys = []

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            error = "Please enter a URL."
        else:
            try:
                engine = get_engine()
                query = engine.addDocs(url)
                results = _query_to_list(query)
                query_keys = query.keys()
                message = f"Documents added successfully from: {url}"
            except NotPossibleException as e:
                error = str(e)

    return render_template("add.html", message=message, error=error,
                           results=results, query_keys=query_keys)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = None
    query_keys = []
    error = None

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if not keyword:
            error = "Please enter a keyword."
        else:
            try:
                engine = get_engine()
                query = engine.queryFirst(keyword)
                results = _query_to_list(query)
                query_keys = query.keys()
            except NotPossibleException as e:
                error = str(e)

    return render_template("search.html", results=results,
                           query_keys=query_keys, error=error)


@app.route("/refine", methods=["POST"])
def refine():
    error = None
    results = None
    query_keys = []

    keyword = request.form.get("keyword", "").strip()
    if not keyword:
        error = "Please enter a keyword to add."
    else:
        try:
            engine = get_engine()
            query = engine.queryMore(keyword)
            results = _query_to_list(query)
            query_keys = query.keys()
        except NotPossibleException as e:
            error = str(e)
            # Preserve previous results on error
            engine = get_engine()
            if engine._current_query is not None:
                results = _query_to_list(engine._current_query)
                query_keys = engine._current_query.keys()

    return render_template("search.html", results=results,
                           query_keys=query_keys, error=error)


@app.route("/find", methods=["GET", "POST"])
def find():
    doc = None
    error = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            error = "Please enter a title."
        else:
            try:
                engine = get_engine()
                doc = engine.findDoc(title)
            except NotPossibleException as e:
                error = str(e)

    return render_template("find.html", doc=doc, error=error)


@app.route("/view/<int:idx>")
def view(idx):
    try:
        engine = get_engine()
        if engine._current_query is None:
            flash("No active search. Start a keyword search first.", "warning")
            return redirect(url_for("search"))
        doc = engine._current_query.fetch(idx)
        return render_template("view.html", doc=doc, idx=idx,
                                back_url=url_for("search"))
    except IndexError:
        flash("Document not found in current results.", "error")
        return redirect(url_for("search"))


if __name__ == "__main__":
    app.run(debug=True)
