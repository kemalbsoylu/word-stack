# Word-Stack

A sleek, fast, terminal-based vocabulary builder. Add words from your command line, automatically fetch their definitions and pronunciations, and build a daily study habit without ever leaving your terminal.

## Features
* **Lightning Fast:** Built with modern Python and `uv`.
* **Zero-Friction Adding:** Just type `word-stack add <word>`. The Dictionary API automatically fetches definitions, examples, and phonetics.
* **Daily Study Mode:** Uses a built-in SQLite database to track your learning and serves you a daily quiz of 10 unstudied words.
* **Beautiful UI:** Terminal output is fully styled with `rich` for gorgeous tables, panels, and loading animations.

## Installation

Word-Stack is easily installable globally using `uv`:

```bash
git clone https://github.com/kemalbsoylu/word-stack.git
cd word-stack
uv tool install .
```

*Note: The application creates a local SQLite database safely tucked away in `~/.word-stack/words.db` to keep your system clean.*

## Usage

Once installed, you can use the `word-stack` (or set up an alias like `ws`) from anywhere on your system.

**Add a word (Auto-fetches definition):**
```bash
word-stack add "persevere"
word-stack add "equilibrium" "denge"
```

**List your saved words:**
```bash
word-stack list
```

**View word details:**
```bash
word-stack show "persevere"
```

**Start your daily study session:**
```bash
word-stack study
```

**Delete a word:**
```bash
word-stack delete "persevere"
```

---

### 🎓 For Python Beginners
Are you learning Python and want to see exactly how this tool was built? 

This repository is the production version of the tool. If you want to see a step-by-step, 3-phase educational history of how to build a CLI app from scratch, please visit the [Word-Stack-CLI Educational Repository](https://github.com/kemalbsoylu/word-stack-cli). It is designed specifically for beginners to explore and submit their first Open Source contributions!
