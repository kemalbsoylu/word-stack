import os
import sqlite3

from datetime import datetime
from api import get_word_info
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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


def format_date(iso_string):
    """Convert an ISO timestamp into human-readable date."""
    if not iso_string or iso_string == "N/A":
        return "Never studied"
    try:
        dt = datetime.fromisoformat(iso_string)
        # Format: Mar 09, 2026 at 12:00 PM
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except ValueError:
        return iso_string


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
    console.print()
    console.print(table)
    console.print()
    conn.close()


def show_word(word):
    """Show all details for a specific word."""
    conn = get_connection()
    cursor = conn.cursor()

    # Use WHERE to find the exact word, making it case-insensitive
    cursor.execute("SELECT * FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    row = cursor.fetchone()

    if row:
        # Build a single formatted string with markup tags for the content
        content = (
            f"[bold cyan]Translation :[/bold cyan] {row['translation']}\n"
            f"[bold cyan]Phonetic    :[/bold cyan] {row['phonetic']}\n"
            f"[bold cyan]Definition  :[/bold cyan] {row['definition']}\n"
            f"[bold cyan]Example     :[/bold cyan] {row['example']}\n"
            f"[bold cyan]Last Studied:[/bold cyan] {format_date(row['last_studied'])}"
        )

        # Wrap it in a Panel (expand=False keeps the box wrapped tightly around the text)
        card = Panel(
            content,
            title=f"📖 [bold magenta]{row['word'].upper()}[/bold magenta]",
            border_style="blue",
            expand=False
        )

        console.print()  # Add a blank line for breathing room
        console.print(card)
        console.print()
    else:
        console.print(f"[bold red]⚠️ The word '{word}' was not found in your list.[/bold red]")

    conn.close()


def delete_word(word):
    """Delete a word from the saved list."""
    conn = get_connection()
    cursor = conn.cursor()

    # First, check if the word exists and give good user feedback
    cursor.execute("SELECT id FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    if not cursor.fetchone():
        console.print(f"[bold yellow]⚠️ The word '{word}' was not found in your list.[/bold yellow]")
        conn.close()
        return

    # Then, delete it
    cursor.execute("DELETE FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Successfully deleted '{word}'.[/bold green]")


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
        console.print("[bold yellow]Your word list is empty. Add some words first![/bold yellow]")
        conn.close()
        return

    # Intro screen
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f"\n[bold magenta]🎓 Starting Study Session ({len(study_list)} words)[/bold magenta]")
    console.print("Try to remember the translation and meaning.")
    console.input("\n[dim]Press Enter to begin...[/dim]")

    for i, row in enumerate(study_list):
        # Clear the terminal for a clean flashcard experience
        os.system('cls' if os.name == 'nt' else 'clear')

        # 1. The Question Panel (Front of flashcard)
        front = Panel(
            f"[bold white]Word {i + 1} of {len(study_list)}[/bold white]",
            title=f"🤔 [bold cyan]{row['word'].upper()}[/bold cyan]",
            border_style="cyan",
            expand=False
        )
        console.print(front)

        # Wait for the user to guess
        user_input = console.input("\n[dim]Press Enter to reveal answer (or 'q' to quit)...[/dim] ")
        if user_input.lower() == 'q':
            console.print("\n[bold yellow]Ending study session early. Great job today![/bold yellow]")
            break

        # 2. The Answer Panel (Back of flashcard)
        back_content = (
            f"[bold green]Translation :[/bold green] {row['translation']}\n"
            f"[bold green]Phonetic    :[/bold green] {row['phonetic']}\n"
            f"[bold green]Definition  :[/bold green] {row['definition']}\n"
            f"[bold green]Example     :[/bold green] {row['example']}\n\n"
            f"[dim]Previously Studied: {format_date(row['last_studied'])}[/dim]"
        )

        back = Panel(
            back_content,
            title=f"💡 [bold green]Answer[/bold green]",
            border_style="green",
            expand=False
        )
        console.print(back)

        # Update the timestamp for THIS specific word using its unique ID
        now = datetime.now().isoformat()
        cursor.execute('''
            UPDATE words
            SET last_studied = ?
            WHERE id = ?
        ''', (now, row['id']))

        # Pause before the next word, unless it's the very last one
        if i < len(study_list) - 1:
            next_action = console.input("\n[dim]Press Enter for the next word (or 'q' to quit)...[/dim] ")
            if next_action.lower() == 'q':
                console.print("\n[bold yellow]Ending study session early. Great job today![/bold yellow]")
                break

    # Commit the updates at the very end
    conn.commit()
    conn.close()
    console.print("\n[bold green]✅ Study session complete! Progress saved.[/bold green]")
