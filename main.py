import time
import ollama
import pyperclip
import requests
import json
from langdetect import detect
from prompts import SYSTEM_PROMPT

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Access configuration values
MODEL_NAME = CONFIG["ollama"]["model_name"]
ANKI_CONFIG = CONFIG["anki"]

LANG_MAP = {
    "pl": "Polish",
    "es": "Spanish",
    "en": "English",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
}


def add_anki_note(front: str, back: str):
    """Adds a new note (flashcard) to Anki using AnkiConnect."""
    if not all([ANKI_CONFIG["connect_url"], ANKI_CONFIG["deck_name"], ANKI_CONFIG["model_name"]]):
        print("Error: Anki configuration is incomplete in config.json")
        return

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": ANKI_CONFIG["deck_name"],
                "modelName": ANKI_CONFIG["model_name"],
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["translation", "ollama"]
            }
        }
    }
    
    try:
        response = requests.post(ANKI_CONFIG["connect_url"], json=payload)
        response.raise_for_status()
        print("Flashcard added successfully to Anki.")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
        print("Please ensure Anki is open and AnkiConnect is installed and running.")


def interpret_with_ollama(text: str):
    language_code = detect(text)
    language_name = LANG_MAP.get(language_code, "the same language as the input")
    if not MODEL_NAME:
        print("Error: Ollama model_name is not set in config.json")
        return
    try:
        if CONFIG["mode"] == "translate":
            prompt = f"Translate this text to {CONFIG['target_language']} (only translation, no explanations):\n{text}"
        else:
            prompt = (
                f"Explain the following word, expression, or text in simple terms. "
                f"Respond only with the explanation, using the same language as the input "
                f"({language_name}). Do not give translations or alternatives.\n\n"
                f"Text: {text}"
            )
    
            response: ollama.ChatResponse = ollama.chat(model=MODEL_NAME, messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            }
            ,{
                'role': 'user',
                'content': prompt,
            },
            ])
            add_anki_note(front=text, back=response['message']['content'])
            print(f"Language detected: {language_name}")
            print("Response: ", response['message']['content'])
    except Exception as e:
        print(f"Error with Ollama: {e}")


def main():
    print("Akvo is running. Copy some text to translate/explain it...")  
    last_clipboard_content = pyperclip.paste()
    while True:
        try:
            current_clipboard_content = pyperclip.paste()
            
            # Check if the content has changed and is not empty
            if current_clipboard_content != last_clipboard_content and current_clipboard_content.strip():
                interpret_with_ollama(current_clipboard_content)
            
            # Update the last known content
            last_clipboard_content = current_clipboard_content
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nExiting clipboard translator.")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")


if __name__ == "__main__":
  main()