import requests
from rich.console import Console

console = Console()


def get_word_info(word):
    """Fetch word details from the Free Dictionary API."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        response = requests.get(url)

        if response.status_code == 404:
            console.print(f"[bold yellow]⚠️ Could not find extra info for '{word}' on the API.[/bold yellow]")
            return None

        response.raise_for_status()  # Check for other errors (e.g., 500)
        data = response.json()[0]  # The API returns a list, take the first entry

        # Using .get() is safer than square brackets [] to avoid KeyErrors
        phonetic = data.get("phonetic", "N/A")

        # Grab the first meaning
        definition = "No definition found"
        example = "No example found"

        if data.get("meanings"):
            first_meaning = data["meanings"][0]
            if first_meaning.get("definitions"):
                definition = first_meaning["definitions"][0].get("definition", definition)
                example = first_meaning["definitions"][0].get("example", example)

        return {
            "phonetic": phonetic,
            "definition": definition,
            "example": example
        }

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]⚠️ Connection error: Could not reach the Dictionary API. ({e})[/bold red]")
        return None
