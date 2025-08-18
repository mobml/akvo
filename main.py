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
    target_language_code = CONFIG.get("target_language", "en")
    target_language_name = LANG_MAP.get(target_language_code)
    if not MODEL_NAME:
        print("Error: Ollama model_name is not set in config.json")
        return
    try:
        if CONFIG['mode'] == "translate":
            prompt = (
                f"Task: Translate the following text into {target_language_name}. \n"
                f"Objective: Provide only the translation, without explanations, alternatives, or commentary. \n"
                f"Constraints: The output must be a single, clear translation in {target_language_name}. "
                f"No additional notes or formatting. \n\n"
                f"Text to translate:\n{text}"
            )

        elif CONFIG["mode"] == "explain":
            prompt = (
                f"Task: Explain the following word, phrase, or text in simple terms. \n"
                f"Objective: Help the learner understand the meaning in {language_name}, "
                f"using straightforward vocabulary and clear phrasing. \n"
                f"Constraints: Respond only with the explanation in {language_name}. "
                f"Do not provide translations, alternatives, or switch languages. "
                f"Keep the explanation short, precise, and easy to follow. \n\n"
                f"Text to explain:\n{text}"
            )
        else:
            prompt = (
                f"Task: Rewrite the following text in simpler {language_name}. \n"
                f"Objective: Lower the text difficulty to the specified target level (e.g., C1 → B1) "
                f"while preserving the original meaning. \n"
                f"Constraints: Use the same language as the input. "
                f"Simplify vocabulary and sentence structures, but do not remove essential meaning. "
                f"If no target level is specified, default to B1. "
                f"Keep the output short, clear, and learner-friendly. \n\n"
                f"Text to simplify:\n{text}"
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
        print("Target language: ", CONFIG.get("target_language", "N/A"))
        print("Response: ", response['message']['content'])
    except Exception as e:
        print(f"Error with Ollama: {e}")


def main():
    print("Akvo is running. Copy some text to translate/explain it...")
    print("Model:", MODEL_NAME)
    print("Mode:", CONFIG["mode"])
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