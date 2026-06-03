"""Interactive command-line interface for the Search Engine."""

from engine import Engine, NotPossibleException


HELP_TEXT = """
Commands:
  add <url>       - Add documents from a URL (supports file:// and http://)
  search <word>   - Start a new search with a keyword
  more <word>     - Refine the current search with an additional keyword
  find <title>    - Look up a document by its exact title
  help            - Show this help message
  quit            - Exit the program
"""


def print_query_results(query):
    keywords = ", ".join(query.keys())
    count = query.size()
    print(f"\nKeywords : {keywords}")
    print(f"Results  : {count} document(s) found")
    if count == 0:
        print("  (no matches)")
        return
    limit = min(10, count)
    for i in range(limit):
        doc = query.fetch(i)
        title = doc.title()
        body_preview = doc.body()[:80].replace("\n", " ")
        print(f"  [{i + 1}] {title}")
        print(f"       {body_preview}{'...' if len(doc.body()) > 80 else ''}")
    if count > limit:
        print(f"  ... and {count - limit} more result(s)")


def main():
    print("Search Engine")
    print("=============")
    try:
        engine = Engine()
        print("Engine initialized. Type 'help' for available commands.\n")
    except NotPossibleException as e:
        print(f"Error: Failed to initialize engine: {e}")
        return

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd == "add":
            if not arg:
                print("Usage: add <url>")
                continue
            try:
                query = engine.addDocs(arg)
                print(f"Documents added from: {arg}")
                if query.size() > 0:
                    print("Updated query results:")
                    print_query_results(query)
            except NotPossibleException as e:
                print(f"Error: {e}")

        elif cmd == "search":
            if not arg:
                print("Usage: search <word>")
                continue
            try:
                query = engine.queryFirst(arg)
                print_query_results(query)
            except NotPossibleException as e:
                print(f"Error: {e}")

        elif cmd == "more":
            if not arg:
                print("Usage: more <word>")
                continue
            try:
                query = engine.queryMore(arg)
                print_query_results(query)
            except NotPossibleException as e:
                print(f"Error: {e}")

        elif cmd == "find":
            if not arg:
                print("Usage: find <title>")
                continue
            try:
                doc = engine.findDoc(arg)
                print(f"\nTitle : {doc.title()}")
                print(f"Body  :\n{doc.body()}")
            except NotPossibleException as e:
                print(f"Error: {e}")

        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
