import argparse

from rich_argparse import RichHelpFormatter
from storage import add_word, list_words, show_word, delete_word, study_words


def main():
    # 1. Initialize the parser with the Rich formatter
    parser = argparse.ArgumentParser(
        description="Word-Stack-CLI: Your personal vocabulary builder.",
        formatter_class=RichHelpFormatter  # <-- NEW LINE
    )

    # 2. Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command: translation is now optional (nargs="?", default="N/A")
    add_parser = subparsers.add_parser("add", help="Add a new word")
    add_parser.add_argument("word", type=str, help="The English word")
    add_parser.add_argument("translation", type=str, nargs="?", default="N/A",
                            help="Optional translation in your language")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List all saved words")

    # 'show' command
    show_parser = subparsers.add_parser("show", help="Show all details for a specific word")
    show_parser.add_argument("word", type=str, help="The English word to inspect")

    # 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete a saved word")
    delete_parser.add_argument("word", type=str, help="The English word to delete")

    # 'study' command
    study_parser = subparsers.add_parser("study", help="Start a daily study session (10 words)")

    # 3. Parse the arguments that the user typed in the terminal
    args = parser.parse_args()

    # 4. Route the command to the correct function
    if args.command == "add":
        add_word(args.word, args.translation)
    elif args.command == "list":
        list_words()
    elif args.command == "show":
        show_word(args.word)
    elif args.command == "delete":
        delete_word(args.word)
    elif args.command == "study":
        study_words()
    else:
        # If the user just runs `python main.py` with no arguments, show the help menu
        parser.print_help()


if __name__ == "__main__":
    main()
