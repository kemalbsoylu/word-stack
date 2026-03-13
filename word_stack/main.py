import argparse
import importlib.metadata

from rich_argparse import RawDescriptionRichHelpFormatter
from word_stack.storage import add_word, list_words, show_word, delete_word, study_words, has_studied_today, \
    add_multiple_words


def get_version():
    """Fetch the package version from pyproject.toml."""
    try:
        return importlib.metadata.version("word-stack")
    except importlib.metadata.PackageNotFoundError:
        return "unknown (not installed as a package)"


def main():
    status_msg = "✅ You have studied today!" if has_studied_today() else "❌ You haven't studied today yet."

    parser = argparse.ArgumentParser(
        description=f"Word-Stack: Your personal vocabulary builder.\n\nDaily Status: {status_msg}",
        formatter_class=RawDescriptionRichHelpFormatter
    )

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {get_version()}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add a new word")
    add_parser.add_argument("word", type=str, help="The English word")
    add_parser.add_argument("translation", type=str, nargs="?", default="N/A", help="Optional translation")

    bulk_parser = subparsers.add_parser("bulk", help="Add multiple words at once (e.g., word-stack bulk apple banana)")
    bulk_parser.add_argument("words", type=str, nargs="+", help="List of English words separated by spaces")

    list_parser = subparsers.add_parser("list", help="List latest saved words")
    list_parser.add_argument("-l", "--limit", type=int, default=10, help="Number of latest words to show (default: 10)")

    show_parser = subparsers.add_parser("show", help="Show details for a specific word")
    show_parser.add_argument("word", type=str, help="The English word to inspect")

    delete_parser = subparsers.add_parser("delete", help="Delete a saved word")
    delete_parser.add_argument("word", type=str, help="The English word to delete")

    study_parser = subparsers.add_parser("study", help="Start a daily study session (10 words)")

    args = parser.parse_args()

    if args.command == "add":
        add_word(args.word, args.translation)
    elif args.command == "bulk":
        add_multiple_words(args.words)
    elif args.command == "list":
        list_words(args.limit)
    elif args.command == "show":
        show_word(args.word)
    elif args.command == "delete":
        delete_word(args.word)
    elif args.command == "study":
        study_words()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
