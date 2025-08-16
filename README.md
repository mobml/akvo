# Akvo

Akvo is a small Python utility that automates sentence mining for language learners. It watches your clipboard for copied sentences, sends them to an Ollama model for translation (or other processing), and automatically adds the original sentence + the model response as a flashcard into Anki via AnkiConnect.

## Features
- Clipboard watcher: automatically detects new clipboard text
- Uses Ollama models for translation/explanation
- Adds flashcards to Anki using AnkiConnect

## Technologies
- Python 3.8+
- ollama Python client (local Ollama runtime or service)
- pyperclip (clipboard interaction)
- python-dotenv (load configuration from `.env`)
- requests (HTTP requests to AnkiConnect)
- Anki with the AnkiConnect add-on

## Prerequisites
- Python 3.8 or newer
- Ollama installed and running (locally or accessible) with at least one model available
- Anki desktop app installed with the AnkiConnect add-on enabled and running

## Installation
1. Clone or download the repository.
    ````powershell
        git clone https://github.com/mobml/akvo
    ```

2. Create and activate a virtual environment (recommended):

   On Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   pip install requests
   ```

   Note: `requests` is used by `main.py` but may not be listed in `requirements.txt` — install it if needed.

## Configuration
Create a `.env` file in the project root (the repo contains an example). Set the following variables:

```env
MODEL_NAME="gpt-oss:20b"        # Ollama model identifier
ANKI_CONNECT_URL="http://127.0.0.1:8765"  # AnkiConnect URL
DECK_NAME="English"           # Anki deck to add notes to
MODEL_NAME_ANKI="Basic"      # Anki note type / model to use
```

Adjust values to match your Ollama model names, Anki setup and preferred deck/note type.

## Usage
Run the main script. The program will monitor your clipboard and process any new non-empty text you copy.

```powershell
python main.py
```

Typical behavior:
- You copy a sentence (e.g. "How are you?")
- Akvo sends the sentence to the configured Ollama model asking for a Spanish translation
- The returned translation is saved as the "Back" of an Anki note, while the original sentence becomes the "Front"
- The note is added to the configured Anki deck using AnkiConnect

## Examples
1. Copy to clipboard: "How are you?"
   - Ollama responds: "¿Cómo estás?"
   - Anki note created:
     - Front: How are you?
     - Back: ¿Cómo estás?

2. Copy a longer sentence to get a translation or explanation (depending on how you change the prompt in `main.py`).

## Customization
- Edit `interpret_with_ollama` in `main.py` to change prompts or request explanations instead of translations.
- Update `.env` to change model, deck name or Anki model.

## Troubleshooting
- Anki note not created: make sure Anki is running and AnkiConnect is installed and enabled. Test the AnkiConnect endpoint using your browser or curl against `ANKI_CONNECT_URL`.
- Ollama errors: ensure Ollama daemon/service is running and the `MODEL_NAME` exists and is startable.
- Clipboard not detected: check `pyperclip` compatibility on your platform and that the script has permissions to access the clipboard.

## Contributing
Contributions and ideas welcome. Open an issue or submit a PR with improvements.