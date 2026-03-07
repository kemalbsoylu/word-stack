import json
import os

from datetime import datetime
from api import get_word_info

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

    # NEW API LOGIC
    print(f"🔍 Fetching info for '{word}'...")
    api_info = get_word_info(word)

    new_entry = {
        "word": word,
        "translation": translation,
        "phonetic": api_info["phonetic"] if api_info else "N/A",
        "definition": api_info["definition"] if api_info else "N/A",
        "example": api_info["example"] if api_info else "N/A",
        "last_studied": None
    }

    words.append(new_entry)
    save_words(words)
    print(f"✅ Successfully added '{word}'.")


def list_words():
    """Display all saved words."""
    words = load_words()
    if not words:
        print("Your word list is empty. Add some words first!")
        return

    print("\n📚 Your Saved Words:")
    print("-" * 40)
    for entry in words:
        # Use .get() here to safely handle words added in Phase 1
        w = entry.get("word", "Unknown")
        t = entry.get("translation", "N/A")
        d = entry.get("definition", "N/A")
        print(f"- {w} ({t}): {d}")
    print("-" * 40)


def show_word(word):
    """Show all details for a specific word."""
    words = load_words()

    for entry in words:
        if entry.get("word", "").lower() == word.lower():
            print(f"\n📖 Details for '{entry.get('word')}':")
            print("-" * 30)
            print(f"Translation  : {entry.get('translation', 'N/A')}")
            print(f"Phonetic     : {entry.get('phonetic', 'N/A')}")
            print(f"Definition   : {entry.get('definition', 'N/A')}")
            print(f"Example      : {entry.get('example', 'N/A')}")
            print(f"Last Studied : {entry.get('last_studied', 'N/A')}")
            print("-" * 30)
            return

    print(f"⚠️ The word '{word}' was not found in your list.")


def delete_word(word):
    """Delete a word from the saved list."""
    words = load_words()

    # Record the initial length to check later
    initial_count = len(words)

    # List comprehension: Keep only the words that DO NOT match the target word
    # Use .lower() to make the deletion case-insensitive
    words = [entry for entry in words if entry["word"].lower() != word.lower()]

    if len(words) == initial_count:
        print(f"The word '{word}' was not found in your list.")
    else:
        save_words(words)
        print(f"✅ Successfully deleted '{word}'.")


def study_words():
    """Start an interactive study session with words."""
    words = load_words()

    if not words:
        print("Your word list is empty. Add some words first!")
        return

    # Helper function to sort words by last_studied date
    def get_sort_key(entry):
        date_str = entry.get("last_studied")
        if not date_str or date_str == "N/A":
            # If it has never been studied, treat it as very old so it appears first
            return "0000-00-00 00:00:00"
        return date_str

    # Sort the list: oldest (or never studied) words come first
    words.sort(key=get_sort_key)

    # Pick the top 10 words
    study_list = words[:10]

    print(f"\n🎓 Starting Study Session ({len(study_list)} words)")
    print("Try to remember the translation and meaning. Press ENTER to reveal.")
    print("Type 'q' and press ENTER at any time to quit early.")
    print("=" * 50)

    for i, entry in enumerate(study_list):
        word = entry.get("word", "Unknown")
        print(f"\nWord {i + 1}/{len(study_list)}: -> ** {word.upper()} ** <-")

        # Pause and wait for user
        user_input = input("\nPress Enter to reveal answer...")
        if user_input.lower() == 'q':
            print("\nEnding study session early. Great job today!")
            break

        print(f"Translation  : {entry.get('translation', 'N/A')}")
        print(f"Phonetic     : {entry.get('phonetic', 'N/A')}")
        print(f"Definition   : {entry.get('definition', 'N/A')}")
        print(f"Example      : {entry.get('example', 'N/A')}")
        print("-" * 50)

        # Update the timestamp using ISO format (e.g., "2026-03-06T12:00:00")
        entry["last_studied"] = datetime.now().isoformat()

    # Save the master list (which now has updated timestamps) back to the JSON file
    save_words(words)
    print("\n✅ Study session complete! Progress saved.")
