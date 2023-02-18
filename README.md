# spanki

Command line tool to lookup Foreign language words from multiple dictionaries and easily add them to an anki deck

 (Originally developed for Spanish. SPanish + ANKI = SPANKI)

Spanki can use a variety of foreign language dictionaries from rapidapi and the user can pick a translation and immediately
create a card in an Anki deck for future recall/study. API calls are threaded for faster response.

## Requirements

1. Python installed.
2. Either 
    - rest4dict running on the localhost (http://github.com/kentonself/rest4dict)  AND/OR
    - An account with rapidapi.com  https://rapidapi.com/ AND
    - A subscription within rapidapi to one or more translation API
        -  Currently 3 rapidapi services are supported, all of which have a free (or "freemium") tier:
            - MyMemory Translation Memory: https://rapidapi.com/translated/api/mymemory-translation-memory
            - Long Translator: https://rapidapi.com/cloudlabs-dev/api/long-translator
            - Rapid Translate Multi Traduction: https://rapidapi.com/sibaridev/api/rapid-translate-multi-traduction
3. A running instance of Anki with the AnkiConnect Add-In (https://ankiweb.net/shared/info/2055492159)
4. A deck in Anki to add new cards to.

## Environment

Spanki uses the following environment variables:
```
SPANKI_APIS            - Mandatory A comma separated list of APIs to check (see Examples below)
SPANKI_KEY             - Mandatory if using rapidapi. The key from rapidapi ("X-RapidAPI-Key") for your subscriptions
SPANKI_DECK_NAME       - Mandatory. The deck name in Anki to add cards to.
SPANKI_NOTE_TYPE       - Optional. If set Spanki will add fields for gender and part of speech, oherwise wil insert a
                                   basic front/back card
SPANKI_SYNC_ON_ADD     - Optional. If set (unless set to 0 or False), will sync with AnkiWeb after each add.
                                  (Can add time for sync)
SPANKI_LANG            - Optional. Language code to be translated. Ex. "es" for Spanish, "it" for Italian, etc.
                                   (Defaults to Spanish. Only tested in Spanish, so YMMV)
SPANKI_ANKICONNECT_URL - Optional. If set will override the default AnkiConnect address http://localhost:8765
```
Examples:
```
export SPANKI_KEY=0123456789abcdef123456789aabcdef123456789abcdef01
export SPANKI_APIS=mymemory,multi-traduction,long-translator,rest4dict
export SPANKI_DECK_NAME=Kenton\'s\ Spanish\ Words
export SPANKI_NOTE_TYPE=Spanish
export SPANKI_SYNC_ON_ADD=1
export SPANKI_LANG=es
export SPANK_ANKICONNECT_URL=http://remotehost.local:8765
```


## Usage

Run spanky.py from the command line. Enter a word or phrase in Spanish. When translation is returned, spanki can create
a card and add it to the Anki deck. You can enter the part of speech and gender (for nouns)

## Examples

```
$ ./spanki.py
Enter word/phrase to translate (or q to quit): almendra
1 from mymemory: almond
2 from multi-traduction: almond
3 from long-translator: almond
Add to anki? y
Enter Part of Speech: n
Enter Gender: m
{'result': 1676503147588, 'error': None}
Enter word/phrase to translate (or q to quit): lampara
1 from mymemory: light fixture
2 from multi-traduction: lamp
3 from long-translator: lamp
Enter number choice from above or:
 q to skip adding to anki
 c to concatenate choices : 2
Add to anki? y
Enter Part of Speech: n
Enter Gender: f
{'result': 1676553009807, 'error': None}
```

(Note that for lampara, you can enter 2 or 3 and add a card for lamp, 1 to add a card for light fixture, or c to add a card with all the definitions into one card. The mymemory API sometimes has unusual translations for words. 'taladro' ('drill") is an interesting example of this.)

## License

GNU GENERAL PUBLIC LICENSE

## TODO

- Add other target languages besides English
- Add more API's
- Look up words in fd-spa-eng dictionary of linux `dict` command (incorporate with rest4dict)
- Parse the return from API call to AnkiConnect to be cleaner
	
## Contribution

Please submit pull requests! Before doing so, test code by adding a word to an anki deck and run pylint until it shows 10/10



