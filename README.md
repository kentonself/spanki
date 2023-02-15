# spanki

Command line tool to enter Spanish words and add them to an anki deck (SPanish + ANKI = SPANKI)

## Requirements

1. An account with rapidapi.com  https://rapidapi.com/
2. A subscription within rapidapi to one or more Spanish translation API's.
   Currently 3 services are supported, all of which have a free (or "freemium") tier:
  a. MyMemory Translation Memory: https://rapidapi.com/translated/api/mymemory-translation-memory
  b. Long Translator: https://rapidapi.com/cloudlabs-dev/api/long-translator 
  c. Rapid Translate Multi Traduction: https://rapidapi.com/sibaridev/api/rapid-translate-multi-traduction
3. A running instance of Anki
4. A deck in Anki to add new cards to.
5. A card type in Anki that contains the field "Word", "Part of Speech", "Meaning" and "Gender"
6. The AnkiConnect Add-In (https://ankiweb.net/shared/info/2055492159)

## Setup

In the options.py file:
 - Enter your rapidapi key.
 - Enter the name of the deck to add cards to

## Usage

Run spanky.py from the command line. Enter a word or phrase in Spanish. When translation is returned, spanki can create 
a card and add it to the Anki deck. You can enter the part of speech and gender (for nouns)



