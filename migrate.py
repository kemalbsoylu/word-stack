import json
import os
import sqlite3


JSON_FILE = "words.json"
DB_FILE = "words.db"


def migrate_data():
    print("🚀 Starting Data Migration: JSON to SQLite...")

    # 1. Check if the JSON file actually exists
    if not os.path.exists(JSON_FILE):
        print(f"⚠️ No '{JSON_FILE}' found. Nothing to migrate.")
        return

    # 2. Load the old data
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        try:
            words_to_migrate = json.load(file)
        except json.JSONDecodeError:
            print("⚠️ Error reading JSON file. It might be empty or corrupted.")
            return

    if not words_to_migrate:
        print("The JSON file is empty. Nothing to migrate.")
        return

    # 3. Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure the table exists just in case running this before running main.py
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

    migrated_count = 0
    skipped_count = 0

    print(f"📦 Found {len(words_to_migrate)} words in JSON. Checking against database...")

    # 4. Process each word
    for entry in words_to_migrate:
        word = entry.get("word")
        if not word:
            continue  # Skip invalid entries

        # Check if it already exists in the new DB
        cursor.execute("SELECT id FROM words WHERE LOWER(word) = LOWER(?)", (word,))
        if cursor.fetchone():
            print(f"   ⏭️  Skipping '{word}' (Already in database)")
            skipped_count += 1
            continue

        # Insert into database. Use .get() here to safely handle Phase 1 data
        cursor.execute('''
            INSERT INTO words (word, translation, phonetic, definition, example, last_studied)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            word,
            entry.get("translation", "N/A"),
            entry.get("phonetic", "N/A"),
            entry.get("definition", "N/A"),
            entry.get("example", "N/A"),
            entry.get("last_studied", None)
        ))
        migrated_count += 1
        print(f"   ✅ Migrated '{word}'")

    # 5. Save changes and close
    conn.commit()
    conn.close()

    # 6. Show Summary
    print("\n" + "="*40)
    print("📊 MIGRATION SUMMARY")
    print("="*40)
    print(f"Total processed      : {len(words_to_migrate)}")
    print(f"Successfully migrated: {migrated_count}")
    print(f"Skipped (duplicates) : {skipped_count}")
    print("="*40)
    print("\nTip: Once you verify your data with 'uv run main.py list', you can safely delete 'words.json'.")


if __name__ == "__main__":
    migrate_data()
