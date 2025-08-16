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
- requests (HTTP requests to AnkiConnect)
- Anki with the AnkiConnect add-on

## Prerequisites
- Python 3.8 or newer
- Ollama installed and running (locally or accessible) with at least one model available
- Anki desktop app installed with the AnkiConnect add-on enabled and running

## Installation
1. Clone or download the repository.
    ```powershell
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
Create or modify the `config.json` file in the project root. The configuration is structured as follows:

```json
{
  "mode": "explain",           // Mode can be "explain" or "translate"
  "target_language": "es",     // Target language for translations (e.g., "es" for Spanish)
  "ollama": {
    "model_name": "gemma3:1b"  // Ollama model identifier
  },
  "anki": {
    "connect_url": "http://127.0.0.1:8765",  // AnkiConnect URL
    "deck_name": "English",                   // Anki deck to add notes to
    "model_name": "Basic"                     // Anki note type / model to use
  }
}
```

Adjust these values to match your preferences:
- `mode`: Choose between "translate" for direct translations or "explain" for explanations
- `target_language`: Set your target language code (e.g., "es", "en", "fr")
- `ollama.model_name`: Set the Ollama model you want to use
- `anki`: Configure your Anki connection settings and preferences

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
- Edit `interpret_with_ollama` in `main.py` to customize the prompts
- Update `config.json` to:
  - Switch between translation and explanation modes
  - Change target language
  - Configure different Ollama models
  - Modify Anki settings (deck, note type)

## Troubleshooting
- Configuration errors: Make sure `config.json` exists and contains all required fields with valid values
- Anki note not created: Make sure Anki is running and AnkiConnect is installed and enabled. Test the AnkiConnect endpoint using your browser or curl against the URL specified in `config.json`
- Ollama errors: Ensure Ollama daemon/service is running and the model specified in `config.json` exists and is startable
- Clipboard not detected: Check `pyperclip` compatibility on your platform and that the script has permissions to access the clipboard

## Contributing
Contributions and ideas welcome. Open an issue or submit a PR with improvements.