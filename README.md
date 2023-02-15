# spanki

Command line tool to lookup Spanish words from multiple dictionaries and easily add them to an anki deck (SPanish + ANKI = SPANKI)

Spanki can use a variety of Spanish-English dictionaries from rapidapi and the user can pick a translation and immediately
create a card in an Anki deck for future recall/study. API calls are threaded for faster response.

## Requirements

1. Python installed.
2. An account with rapidapi.com  https://rapidapi.com/
3. A subscription within rapidapi to one or more Spanish translation API's.
   Currently 3 services are supported, all of which have a free (or "freemium") tier:
  a. MyMemory Translation Memory: https://rapidapi.com/translated/api/mymemory-translation-memory
  b. Long Translator: https://rapidapi.com/cloudlabs-dev/api/long-translator 
  c. Rapid Translate Multi Traduction: https://rapidapi.com/sibaridev/api/rapid-translate-multi-traduction
4. A running instance of Anki
5. A deck in Anki to add new cards to.
6. A card type in Anki that contains the field "Word", "Part of Speech", "Meaning" and "Gender"
7. The AnkiConnect Add-In (https://ankiweb.net/shared/info/2055492159)

## Setup

In the options.py file:
 - Enter your rapidapi key.
 - Enter the name of the deck to add cards to
 - Edit the apis list to include the apis subscribed to
 - If using a note type other than "Basic" change the note_type. Any other note type must include fields 
    "Word", "Part of Speech", "Meaning", and "Gender". Otherwise the Basic card type is front/back.

## Usage

Run spanky.py from the command line. Enter a word or phrase in Spanish. When translation is returned, spanki can create 
a card and add it to the Anki deck. You can enter the part of speech and gender (for nouns)

## Examples

$ ./spanki.py
Enter word/phrase to translate (or q to quit): almendra
1 from mymemory: almond
2 from multi-traduction: almond
3 from long-translator: almond
Add to anki? y
Enter Part of Speech: n
Enter Gender: m
{'result': 1676503147588, 'error': None}
Enter word/phrase to translate (or q to quit): taladro 
1 from mymemory: blue gum borer, common eucalypt longicorn, eucalyptus borer
2 from multi-traduction: drill
3 from long-translator: drill
Enter number choice from above or:
 q to skip adding to anki
 c to concatenate choices : 

(Note that for taladro, you can enter 2 or 3 and add a card for drill, 1 to add a card for blue gum borer, or c to add a card with all the definitions into one card. The mymemory API sometimes has unusual translations for words.)

## License

GNU GENERAL PUBLIC LICENSE

## TODO

- Add more API's
- Look up words in fd-spa-eng dictionary of linux `dict` command
	
## Contribution

Please submit pull requests! Before doing so, test code by adding a word to an anki deck and run pylint until it shows 10/10



