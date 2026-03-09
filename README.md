# Word-Stack-CLI (An Educational Python Journey)

Welcome to `word-stack-cli`! 

This repository isn't just a vocabulary tool; it is a **step-by-step educational guide** for Python beginners. If you know the basics of Python (variables, loops, functions) and want to learn how a "real" project is structured, evolved, and packaged, you are in the right place.

## The Goal
We are building a Command Line Interface (CLI) tool to save English words, fetch their definitions, and study them daily.

Instead of dropping the final, complex code on you, this project is built in **Three Phases**. By looking at the commit history, you can see exactly how a software project grows from a simple script into a professional package.

## Project Phases

### ✅ Phase 1: The Foundation (Completed)
* **Goal:** Make it work locally with the simplest tools possible.
* **Concepts:** `argparse` for CLI commands, reading/writing `json` files for storage, and basic project structure using `uv`.
* **Features:** Add a word, view saved words, delete words.

### ✅ Phase 2: The "Real World" Integration (Completed)
* **Goal:** Connect to the internet and upgrade our data storage.
* **Concepts:** Making HTTP requests to free public APIs, parsing complex JSON responses, and migrating from simple JSON files to a relational `SQLite` database.
* **Features:** Fetch word definitions automatically, track the "last studied" date, and filter 10 words a day to study.

### ✅ Phase 3: Professional Standards (Completed)
* **Goal:** Make the tool robust, pretty, and installable by anyone.
* **Concepts:** Unit testing with `pytest`, adding a beautiful UI (tables, panels, and spinners) with `rich`, and packaging the tool so it runs globally.

---
*Follow the commit history from the beginning to see how this project is built!*

---

## Getting Started (How to Use)

Because we are using modern tooling, you don't need to manually create virtual environments or run `pip install`. 

### Prerequisites
Make sure you have [uv](https://docs.astral.sh/uv/) installed on your system. 

### Installation
Clone this repository to your machine, then install it globally using `uv`:
```bash
git clone https://github.com/kemalbsoylu/word-stack-cli.git
cd word-stack-cli
uv tool install .
```
   
### Commands

Because you installed it globally, you can now run `word-stack` from **anywhere** on your computer! 

*(Note: Your database is safely stored in a hidden folder at `~/.word-stack/words.db`, keeping your file system clean!)*

**1. See all available commands:**
```bash
word-stack --help
```

**2. Add a new word:**
You can add just the English word, or include a translation in your native language. The tool will automatically fetch the definition and pronunciation from the internet!
```bash
word-stack add "unique"
word-stack add "equilibrium" "denge"
```

**3. List all your saved words:**
```bash
word-stack list
```

**4. Show detailed information for a specific word:**
```bash
word-stack show "unique"
```

**5. Start a daily study session:**
This pulls up to 10 of your oldest (or unstudied) words and quizzes you on them.
```bash
word-stack study
```

**6. Delete a word:**
```bash
word-stack delete "equilibrium"
```

### Running Tests
This project includes automated tests to ensure everything works correctly without breaking existing features. To run the test suite (which includes mocked API responses), navigate to the project folder and run:
```bash
uv run pytest
```

---

## 🤝 Community & Future Improvements (Good First Issues)

This project is built for learning, which means it is a great place to make your first open-source contribution! Here are a few fantastic features waiting to be built:

* **1. Automatic Translation:** If a user only types `word-stack add "apple"`, the tool could automatically detect their system language (or accept a configured user choice) and fetch the translation from a free translation API.
* **2. Data Syncing (`sync` command):** If a user added words back in Phase 1 before we had an API, those words are missing definitions. A new command like `word-stack sync "apple"` could re-fetch the data from the internet and `UPDATE` the database row.
* **3. List Pagination:** As the database grows, printing hundreds of words to the terminal becomes messy. Adding a flag to the list command (e.g., `word-stack list --page 2`) using SQL `LIMIT` and `OFFSET` would be a great database scaling challenge.

Feel free to explore the code, fork the repository, and submit a Pull Request!
