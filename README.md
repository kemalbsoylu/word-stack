# Word-Stack

A powerful, terminal-based vocabulary builder and daily study tool. Add words from your command line, automatically fetch their definitions and pronunciations, and build a daily study habit without ever leaving your terminal.

## Features
* **Lightning Fast:** Built with modern Python and `uv`.
* **Zero-Friction Adding:** Just type `word-stack add <word>`. The Dictionary API automatically fetches definitions, examples, and phonetics.
* **Bulk Import:** Quickly add multiple words at once with beautiful progress tracking.
* **Smart Typo Recovery:** Automatically suggests the correct command if you make a typing mistake.
* **Daily Study Mode:** Uses a built-in SQLite database to track your learning and serves you a daily quiz of unstudied words.
* **Beautiful UI:** Terminal output is fully styled with `rich` for gorgeous tables, panels, and loading animations.

## Prerequisites
Before installing, make sure you have the [uv package manager](https://docs.astral.sh/uv/) installed on your system.

## Installation

Word-Stack is officially published on PyPI. You can install it globally in seconds:

```bash
uv tool install word-stack
```
*(Note: You can also use `pip install word-stack`, but `uv` is recommended for isolated installations).*

### Setting up your Alias
To make the tool lightning fast to use, set up a permanent alias in your shell configuration (like `~/.zshrc` or `~/.bashrc`):
```bash
alias ws="word-stack"
```

### Updating your Installation
When a new version is released, simply run:
```bash
uv tool upgrade word-stack
```

## Usage

**Check your installed version:**
```bash
ws --version
```

**Add a word (Auto-fetches definition):**
```bash
ws add "persevere"
ws add "equilibrium" "denge"
```

**Add multiple words at once:**
```bash
ws bulk "apple" "banana" "ephemeral"
```

**List your latest saved words:**
```bash
ws list
ws list --limit 20
```

**View word details:**
```bash
ws show "persevere"
```

**Start your daily study session:**
```bash
ws study
```

**Delete a word:**
```bash
ws delete "persevere"
```

## Development Setup

Word-Stack uses `uv` for lightning-fast development. You **do not** need to manually create virtual environments or run `pip install`. `uv` handles everything for you automatically.

If you want to contribute or test features without altering your personal vocabulary database, set up an isolated development environment:

**1. Clone the repository and set up your environment variables:**
```bash
git clone https://github.com/kemalbsoylu/word-stack.git
cd word-stack
cp .env.example .env
```

**2. Set up a temporary development alias in your terminal:**
```bash
alias dev="uv run --env-file .env -m word_stack.main"
```

Now you can run commands like `dev list` or `dev bulk test`. The application will detect the development environment and safely route all data to a local `.dev_data/words.db` file instead of your global database!

### Running Tests
To run the test suite, simply use:
```bash
uv run pytest
```

---

### 🎓 For Python Beginners
Are you learning Python and want to see exactly how this tool was built? 

This repository is the production version of the tool. If you want to see a step-by-step, 3-phase educational history of how to build a CLI app from scratch, please visit the [Word-Stack-CLI Educational Repository](https://github.com/kemalbsoylu/word-stack-cli). It is designed specifically for beginners to explore and submit their first Open Source contributions!
