import time
import ollama
import pyperclip
from dotenv import load_dotenv
import os
import requests

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL")
DECK_NAME = os.getenv("DECK_NAME")
MODEL_NAME_ANKI = os.getenv("MODEL_NAME_ANKI")


def add_anki_note(front: str, back: str):
    """Adds a new note (flashcard) to Anki using AnkiConnect."""
    if not all([ANKI_CONNECT_URL, DECK_NAME, MODEL_NAME_ANKI]):
        print("Error: Anki variables are not set in the .env file.")
        return

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME_ANKI,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": ["translation", "ollama"]
            }
        }
    }
    
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response.raise_for_status()
        print("Flashcard added successfully to Anki.")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
        print("Please ensure Anki is open and AnkiConnect is installed and running.")


def interpret_with_ollama(text: str):

  if not MODEL_NAME:
        print("Error: Ollama MODEL_NAME is not set in the .env file.")
        return
  try:
    response: ollama.ChatResponse = ollama.chat(model=MODEL_NAME, messages=[
      {
        'role': 'user',
        'content': 'Could you translate this to spanish (just response the translation): ?' + text,
      },
    ])
    add_anki_note(front=text, back=response['message']['content'])
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
