import sqlite3

from datetime import datetime
from api import get_word_info
from rich.console import Console
from rich.table import Table

# Initialize the rich console
console = Console()

# Our new database file
DB_FILE = "words.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    # This makes SQLite return rows that act like Python dictionaries
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Define schema (the structure of the data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            translation TEXT,
            phonetic TEXT,
            definition TEXT,
            example TEXT,
            last_studied TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run this automatically when storage.py is imported
init_db()


def add_word(word, translation):
    """Add a new word and its translation to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Check if the word already exists
    # Use parameterized queries (?) to prevent SQL Injection attacks
    cursor.execute("SELECT word FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    if cursor.fetchone():
        console.print(f"[bold yellow]The word '{word}' is already in your list![/bold yellow]")
        conn.close()
        return

    # 2. Fetch API Info
    with console.status(f"[bold cyan]🔍 Fetching info for '{word}' from the internet...[/bold cyan]", spinner="dots"):
        api_info = get_word_info(word)

    # 3. Insert into the database
    cursor.execute('''
        INSERT INTO words (word, translation, phonetic, definition, example, last_studied)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        word,
        translation,
        api_info["phonetic"] if api_info else "N/A",
        api_info["definition"] if api_info else "N/A",
        api_info["example"] if api_info else "N/A",
        None
    ))

    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Successfully added '{word}'.[/bold green]")


def list_words():
    """Display all saved words."""
    conn = get_connection()
    cursor = conn.cursor()

    # Use SELECT to grab only the columns need to display
    cursor.execute("SELECT word, translation, definition FROM words")
    rows = cursor.fetchall()

    if not rows:
        # Use simple markup tags like [yellow] for colors
        console.print("[yellow]Your word list is empty. Add some words first![/yellow]")
        conn.close()
        return

    # Create the Rich Table
    table = Table(title="📚 Your Saved Words", show_header=True, header_style="bold magenta")

    # Define columns
    table.add_column("Word", style="cyan", width=15)
    table.add_column("Translation", style="green", width=15)
    table.add_column("Definition", style="white")

    # Add rows to the table
    for row in rows:
        table.add_row(row['word'], row['translation'], row['definition'])

    # Print the table instead of standard text
    console.print(table)
    conn.close()


def show_word(word):
    """Show all details for a specific word."""
    conn = get_connection()
    cursor = conn.cursor()

    # Use WHERE to find the exact word, making it case-insensitive
    cursor.execute("SELECT * FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    row = cursor.fetchone()

    if row:
        print(f"\n📖 Details for '{row['word']}':")
        print("-" * 30)
        print(f"Translation  : {row['translation']}")
        print(f"Phonetic     : {row['phonetic']}")
        print(f"Definition   : {row['definition']}")
        print(f"Example      : {row['example']}")
        print(f"Last Studied : {row['last_studied']}")
        print("-" * 30)
    else:
        print(f"⚠️ The word '{word}' was not found in your list.")

    conn.close()


def delete_word(word):
    """Delete a word from the saved list."""
    conn = get_connection()
    cursor = conn.cursor()

    # First, check if the word exists and give good user feedback
    cursor.execute("SELECT id FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    if not cursor.fetchone():
        print(f"The word '{word}' was not found in your list.")
        conn.close()
        return

    # Then, delete it
    cursor.execute("DELETE FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    conn.commit()
    conn.close()
    print(f"✅ Successfully deleted '{word}'.")


def study_words():
    """Start an interactive study session with words."""
    conn = get_connection()
    cursor = conn.cursor()

    # THE MAGIC OF SQL:
    # Ask the database to sort by last_studied, put NULLs (never studied) first, and only give 10 results
    cursor.execute('''
        SELECT * FROM words
        ORDER BY last_studied ASC NULLS FIRST 
        LIMIT 10
    ''')
    study_list = cursor.fetchall()

    if not study_list:
        print("Your word list is empty. Add some words first!")
        conn.close()
        return

    print(f"\n🎓 Starting Study Session ({len(study_list)} words)")
    print("Try to remember the translation and meaning. Press ENTER to reveal.")
    print("Type 'q' and press ENTER at any time to quit early.")
    print("=" * 50)

    for i, row in enumerate(study_list):
        print(f"\nWord {i + 1}/{len(study_list)}: -> ** {row['word'].upper()} ** <-")

        user_input = input("\nPress Enter to reveal answer...")
        if user_input.lower() == 'q':
            print("\nEnding study session early. Great job today!")
            break

        print(f"Translation  : {row['translation']}")
        print(f"Phonetic     : {row['phonetic']}")
        print(f"Definition   : {row['definition']}")
        print(f"Example      : {row['example']}")
        print("-" * 50)

        # Update the timestamp for THIS specific word using its unique ID
        now = datetime.now().isoformat()
        cursor.execute('''
            UPDATE words
            SET last_studied = ?
            WHERE id = ?
        ''', (now, row['id']))

    # Commit the updates at the very end
    conn.commit()
    conn.close()
    print("\n✅ Study session complete! Progress saved.")
