# Contributing to Word-Stack-CLI

First off, thank you for considering contributing to `word-stack-cli`! This project is designed for learning, so whether you are fixing a typo, adding a new feature, or writing tests, your help is welcome.

## How to Contribute

### 1. Fork and Clone
Fork this repository to your own GitHub account, and then clone it to your local machine:
```bash
git clone https://github.com/kemalbsoylu/word-stack-cli.git
cd word-stack-cli
```

### 2. Set Up the Project
We use `uv` to manage dependencies. You don't need to manually create a virtual environment. Just run:
```bash
uv tool install --force .
```
This will install all dependencies and make the `word-stack` command available locally for testing.

### 3. Make Your Changes
Pick an issue from the README (like adding a `sync` command or pagination), or work on your own idea! 

### 4. Run the Tests
Before submitting your changes, make sure you haven't broken any existing features. Run the test suite:
```bash
uv run pytest
```
*If all the tests pass (show as green), you are good to go!*

### 5. Submit a Pull Request
Push your code to your forked repository and open a Pull Request (PR) against our main branch. Describe what you added and why it helps learners.
