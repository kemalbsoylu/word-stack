import os
import sqlite3

from datetime import datetime
from pathlib import Path
from word_stack.api import get_word_info
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

if os.getenv("WORD_STACK_ENV") == "development":
    APP_DIR = Path.cwd() / ".dev_data"
else:
    APP_DIR = Path.home() / ".word-stack"

APP_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = APP_DIR / "words.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

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


def has_studied_today():
    """Check the database to see if any word was studied today."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(last_studied) FROM words")
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        last_studied_iso = row[0]
        if last_studied_iso != "N/A":
            last_date = last_studied_iso.split("T")[0]
            today_date = datetime.now().date().isoformat()
            return last_date == today_date

    return False


def add_word(word, translation="N/A"):
    """Add a new word and its translation to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    if cursor.fetchone():
        console.print(f"[bold yellow]The word '{word}' is already in your list![/bold yellow]")
        conn.close()
        return

    try:
        with console.status(f"[bold cyan]🔍 Fetching info for '{word}' from the internet...[/bold cyan]",
                            spinner="dots"):
            api_info = get_word_info(word)

    except ValueError:
        console.print(f"[bold yellow]⚠️ '{word}' was not saved. It could not be found in the dictionary.[/bold yellow]")
        conn.close()
        return

    except ConnectionError as e:
        console.print(f"[bold red]❌ '{word}' was not saved. Network error![/bold red]")
        conn.close()
        return

    cursor.execute('''
        INSERT INTO words (word, translation, phonetic, definition, example, last_studied)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        word,
        translation,
        api_info["phonetic"],
        api_info["definition"],
        api_info["example"],
        None
    ))

    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Successfully added '{word}'.[/bold green]")


def add_multiple_words(words):
    """Add multiple words at once with a progress bar and summary."""
    conn = get_connection()
    cursor = conn.cursor()

    added = []
    skipped = []
    not_found = []
    errors = []

    unique_words = list(dict.fromkeys(words))

    console.print()

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing words...", total=len(unique_words))

        for word in unique_words:
            progress.update(task, description=f"[cyan]Fetching '{word}'...")

            cursor.execute("SELECT word FROM words WHERE LOWER(word) = LOWER(?)", (word,))
            if cursor.fetchone():
                skipped.append(word)
                progress.advance(task)
                continue

            try:
                api_info = get_word_info(word)

                cursor.execute('''
                    INSERT INTO words (word, translation, phonetic, definition, example, last_studied)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    word,
                    "N/A",
                    api_info["phonetic"],
                    api_info["definition"],
                    api_info["example"],
                    None
                ))
                conn.commit()
                added.append(word)

            except ValueError:
                not_found.append(word)
            except ConnectionError:
                errors.append(word)

            progress.advance(task)

    conn.close()

    console.print("\n[bold magenta]Summary[/bold magenta]")

    if added:
        console.print(f"[bold green]✅ Added ({len(added)}):[/bold green] {', '.join(added)}")
    if skipped:
        console.print(f"[bold yellow]⏭️  Skipped - already saved ({len(skipped)}):[/bold yellow] {', '.join(skipped)}")
    if not_found:
        console.print(f"[bold red]❌ Not Found ({len(not_found)}):[/bold red] {', '.join(not_found)}")
    if errors:
        console.print(f"[bold red]⚠️  Network Errors ({len(errors)}):[/bold red] {', '.join(errors)}")

    console.print()


def list_words(count=10):
    """Display latest saved words, newest first."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")
    total_words = cursor.fetchone()[0]

    if total_words == 0:
        console.print("[yellow]Your word list is empty. Add some words first![/yellow]")
        conn.close()
        return

    cursor.execute("SELECT word, translation, definition FROM words ORDER BY id DESC LIMIT ?", (count,))
    rows = cursor.fetchall()

    display_count = len(rows)

    table = Table(title=f"📚 Your Latest {display_count} Words (Total: {total_words})", show_header=True, header_style="bold magenta")

    table.add_column("Word", style="cyan", width=15)
    table.add_column("Translation", style="green", width=15)
    table.add_column("Definition", style="white")

    for row in rows:
        table.add_row(row['word'], row['translation'], row['definition'])

    console.print()
    console.print(table)

    remaining_words = total_words - display_count

    if remaining_words == 1:
        console.print(f"[dim]...and {remaining_words} more word hidden.[/dim]")
    elif remaining_words > 1:
        console.print(f"[dim]...and {remaining_words} more words hidden.[/dim]")

    if has_studied_today():
        console.print("\n[bold green]✅ Daily Goal: You have studied today![/bold green]")
    else:
        console.print("\n[bold yellow]⚠️ Daily Goal: You haven't studied today yet. Run 'study'![/bold yellow]")

    console.print()
    conn.close()


def show_word(word):
    """Show all details for a specific word."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    row = cursor.fetchone()

    if row:
        content = (
            f"[bold cyan]Translation :[/bold cyan] {row['translation']}\n"
            f"[bold cyan]Phonetic    :[/bold cyan] {row['phonetic']}\n"
            f"[bold cyan]Definition  :[/bold cyan] {row['definition']}\n"
            f"[bold cyan]Example     :[/bold cyan] {row['example']}\n"
            f"[bold cyan]Last Studied:[/bold cyan] {format_date(row['last_studied'])}"
        )

        card = Panel(
            content,
            title=f"📖 [bold magenta]{row['word'].upper()}[/bold magenta]",
            border_style="blue",
            expand=False
        )

        console.print()
        console.print(card)
        console.print()
        conn.close()
    else:
        conn.close()
        console.print(f"\n[bold yellow]⚠️ The word '{word}' was not found in your list.[/bold yellow]")

        choice = console.input(f"[dim]Would you like to search the dictionary and add '{word}' now? (y/n): [/dim]")
        if choice.lower() == 'y':
            console.print()
            add_word(word, "N/A")


def delete_word(word):
    """Delete a word from the saved list."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    if not cursor.fetchone():
        console.print(f"[bold yellow]⚠️ The word '{word}' was not found in your list.[/bold yellow]")
        conn.close()
        return

    cursor.execute("DELETE FROM words WHERE LOWER(word) = LOWER(?)", (word,))
    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Successfully deleted '{word}'.[/bold green]")


def study_words():
    """Start an interactive study session with words."""
    conn = get_connection()
    cursor = conn.cursor()

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

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f"\n[bold magenta]🎓 Starting Study Session ({len(study_list)} words)[/bold magenta]")

    if has_studied_today():
        console.print("[bold cyan]🌟 You already studied today, but extra practice is always great![/bold cyan]\n")

    console.print("Try to remember the translation and meaning.")
    console.input("\n[dim]Press Enter to begin...[/dim]")

    for i, row in enumerate(study_list):
        os.system('cls' if os.name == 'nt' else 'clear')

        front = Panel(
            f"[bold white]Word {i + 1} of {len(study_list)}[/bold white]",
            title=f"🤔 [bold cyan]{row['word'].upper()}[/bold cyan]",
            border_style="cyan",
            expand=False
        )
        console.print(front)

        user_input = console.input("\n[dim]Press Enter to reveal answer (or 'q' to quit)...[/dim] ")
        if user_input.lower() == 'q':
            console.print("\n[bold yellow]Ending study session early. Great job today![/bold yellow]")
            break

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

        now = datetime.now().isoformat()
        cursor.execute('''
            UPDATE words
            SET last_studied = ?
            WHERE id = ?
        ''', (now, row['id']))

        if i < len(study_list) - 1:
            next_action = console.input("\n[dim]Press Enter for the next word (or 'q' to quit)...[/dim] ")
            if next_action.lower() == 'q':
                console.print("\n[bold yellow]Ending study session early. Great job today![/bold yellow]")
                break

    conn.commit()
    conn.close()
    console.print("\n[bold green]✅ Study session complete! Progress saved.[/bold green]")
