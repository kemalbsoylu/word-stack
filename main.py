import argparse
import json
import os

# Define the file name as a constant at the top
DATA_FILE = "words.json"


def load_words():
    """Load words from the JSON file. Return an empty list if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_words(words):
    """Save the list of words to the JSON file."""
    # Used indent=4 to make the JSON file readable
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(words, file, indent=4)


def add_word(word, translation):
    """Add a new word and its translation to the list."""
    words = load_words()

    # Check if word already exists to avoid duplicates
    for entry in words:
        if entry["word"].lower() == word.lower():
            print(f"The word '{word}' is already in your list!")
            return

    # Create a dictionary for the new word
    new_entry = {
        "word": word,
        "translation": translation
    }
    words.append(new_entry)
    save_words(words)
    print(f"Successfully added '{word}' -> '{translation}'")


def list_words():
    """Display all saved words."""
    words = load_words()
    if not words:
        print("Your word list is empty. Add some words first!")
        return

    print("\n Your Saved Words:")
    print("-" * 20)
    for entry in words:
        print(f"- {entry['word']}: {entry['translation']}")
    print("-" * 20)


def main():
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(description="Word-Stack-CLI: Your personal vocabulary builder.")

    # 2. Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup the 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new word and its translation")
    add_parser.add_argument("word", type=str, help="The English word")
    add_parser.add_argument("translation", type=str, help="The translation in your language")

    # Setup the 'list' command
    list_parser = subparsers.add_parser("list", help="List all saved words")

    # 3. Parse the arguments that the user typed in the terminal
    args = parser.parse_args()

    # 4. Route the command to the correct function
    if args.command == "add":
        add_word(args.word, args.translation)
    elif args.command == "list":
        list_words()
    else:
        # If the user just runs `python main.py` with no arguments, show the help menu
        parser.print_help()


if __name__ == "__main__":
    main()
