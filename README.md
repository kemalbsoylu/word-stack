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

### 🛠️ Phase 2: The "Real World" Integration (Current Phase)
* **Goal:** Connect to the internet and upgrade our data storage.
* **Concepts:** Making HTTP requests to free public APIs, parsing complex JSON responses, and migrating from simple JSON files to a relational `SQLite` database.
* **Features:** Fetch word definitions automatically, track the "last studied" date, and filter 10 words a day to study.

### 🚀 Phase 3: Professional Standards (Coming Soon)
* **Goal:** Make the tool robust, pretty, and installable by anyone.
* **Concepts:** Environment variables (`.env`), unit testing with `pytest`, adding a beautiful UI (loading bars, tables), and packaging the tool so it can be installed globally.

---
*Follow the commit history from the beginning to see how this project is built!*
