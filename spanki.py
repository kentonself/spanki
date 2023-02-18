#! /usr/bin/python3
""" Use Rapid API to translate spanish to english and add to anki
     See https://rapidapi.com/translated/api/mymemory-translation-memory
"""
import os
import sys
import re
import threading
import requests

supported_apis = ['mymemory', 'multi-traduction','long-translator', 'rest4dict']
rapidapi_apis = ['mymemory', 'multi-traduction','long-translator']

# pylint: disable=invalid-name

def call_api(endpoint, text):
    """ Threaded function that makes API call """
    if endpoint == 'mymemory':
        mymemory_api(endpoint, text)
    if endpoint == 'multi-traduction':
        multi_traduction_api(endpoint, text)
    if endpoint == 'long-translator':
        long_translator_api(endpoint, text)
    if endpoint == 'rest4dict':
        rest4dict_api(endpoint, text)

def mymemory_api(endpoint, text):
    "Call the rapidapi mymemory call"
    url  = 'https://translated-mymemory---translation-memory.p.rapidapi.com/get'
    headers = {'X-RapidAPI-Key': spanki_key}
    params =  {'langpair': lang + '|en', 'q': text}

    response = requests.get(url=url, timeout = 10, headers = headers, params=params)
    if response.status_code != 200:
        print(f'API {endpoint} returned {response.status_code}')
        xlations[endpoint] =  None
    elif response.json()['responseData']['translatedText'] is None:
        print (f'No translation for {orig}')
        xlations[endpoint] =  None
    else:
        xlations[endpoint] =  response.json()['responseData']['translatedText'].lower()
    if xlations[endpoint] == orig:
        xlations[endpoint]=None

def multi_traduction_api(endpoint, text):
    "Call the rapidapi multi-traduction call"
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

    payload = {
    	"from": lang,
    	"to": "en",
    	"e": "",
    	"q": [text]
    }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": spanki_key,
    	"X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f'API {endpoint} returned {response.status_code}')
        xlations[endpoint] =  None
    else:
        xlations[endpoint]= None if response.json()[0] == orig else response.json()[0]

def long_translator_api(endpoint, text):
    "Call the rapidapi long-translator call"
    url = "https://long-translator.p.rapidapi.com/translate"

    payload = {
            "source_language": lang,
            "target_language": "en",
            "text": text
            }
    headers = {
	        "content-type": "application/x-www-form-urlencoded",
	        "X-RapidAPI-Key": spanki_key,
	        "X-RapidAPI-Host": "long-translator.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f'API {endpoint} returned {response.status_code}')
        xlations[endpoint] =  None
    else:
        xlations[endpoint] = None \
                if response.json()['data']['translatedText'].lower() == orig.lower() \
                else response.json()['data']['translatedText'].lower()

def rest4dict_api(endpoint, text):
    "call rest4dict running locally (http://gitub.com/kentonself/rest4dict)"
    payload={'source': lang, 'target':'en', 'word': text}
    response = requests.post('http://localhost:5000/api/dict', json=payload, timeout=10)
    if response.status_code == 200 and response.json()['found'] == 1:
        xlations[endpoint] = response.json()['xlation'].lower()
    else:
        xlations[endpoint] = None


# check for env before continuing
envset = True
spanki_key =  os.environ.get('SPANKI_KEY')

supported_apis_string = ','.join(supported_apis)
if os.environ.get('SPANKI_APIS') is None:
    envset = False
    print("Environment Variable SPANKI_APIS must be set")
    print(f"SPANKI_APIS is a comma delimited set. Supported apis are {supported_apis_string}")
    print()
else:
    for api in os.environ.get('SPANKI_APIS').split(','):
        if api not in supported_apis:
            envset = False
            print(f'{api} is not a supported api. Supported apis are {supported_apis_string}')
            print()
        if api in rapidapi_apis and spanki_key is None:
            envset = False
            print(f"Environment Variable SPANKI_KEY must be set since {api} is a rapidapi service")
            print()

# allow for overwriting the default anki connect URL to run on remote instances of Anki/AnkiConnect
ankiconnect_url = os.environ.get('SPANKI_ANKICONNECT_URL')
if ankiconnect_url is None:
    ankiconnect_url = 'http://localhost:8765'

print(ankiconnect_url)

# test for existance of Anki/AnkiConnect and get deckNames
try:
    availdecks = requests.post(url = ankiconnect_url,\
                               json={"action": "deckNames", "version": 6 }, \
                               timeout=10)
except requests.ConnectionError:
    envset = False
    print( "Anki may not be running or AnkiConnect may not be installed")
    print()

if availdecks.json()['error']:
    envset = False
    print( "Anki may not be running or AnkiConnect may not be installed")
    print()
deck_name = os.environ.get('SPANKI_DECK_NAME')
if deck_name is None:
    envset = False
    print("Environment Variable SPANKI_DECK_NAME must be set to Anki Deck")
    print("Example: SPANKI_DECK_NAME=Kenton\\'s\\ Spanish\\ Words")
    print()
elif deck_name not in availdecks.json()['result']:
    envset = False
    print(f'{deck_name} is not a deck in Anki')
    print()
lang=os.environ.get('SPANKI_LANG')
if lang is None:
    lang = "es"
else:
    lang = lang.lower()

note_type = os.environ.get('SPANKI_NOTE_TYPE')
if note_type is None:
    note_type = "Basic"
    print("Environment variable SPANKI_NOTE_TYPE is not set. Basic will be used.")

sync_on_add = os.environ.get('SPANKI_SYNC_ON_ADD') \
        if os.environ.get('SPANKI_SYNC_ON_ADD') is not None else "False"

if envset is False:
    sys.exit()

# Environment should be good now, and Anki running with AnkiConnect

try:
    while True:
        #ignore upper-case "requirement" for found and xlate
        #pylint: disable-msg=C0103
        orig = input('Enter word/phrase to translate (or q to quit): ')

        if orig == 'q':
            sys.exit()

        xlations = {}

        # Thread each api call
        threads = []
        for api in  os.environ.get('SPANKI_APIS').split(','):
            x = threading.Thread(target=call_api, args=(api, orig))
            threads.append(x)
            x.start()

        # wait for threads to finish
        for thread in threads:
            thread.join()

        # iterate through results from each API call and fill up choices list
        found = 0
        choices = []
        for api in os.environ.get('SPANKI_APIS').split(','):
            if xlations[api]:
                choices.append(xlations[api])
                found += 1
                print(f'{found} from {api}: {xlations[api]}')

        if found == 0:
            continue

        # if more than 1 unique value, give choice to user before adding to anki
        # (converting the python list to a python set removes dupliates)
        if found > 1 and len(set(choices)) > 1:
            while True:
                concat = ' ,'.join(set(choices))
                concat = re.sub('^ , ', ' ', concat, count=0, flags=0)

                choice = input('Enter number choice from above or:\n' +\
                                ' q to skip adding to anki\n' +\
                                ' c to concatenate choices\n   (' + concat + ') : ')
                if choice.lower() in ['q', 'c']:
                    break
                if not choice.isnumeric():
                    print('Choice must be a number. Try again')
                    continue
                if int(choice) > found or int(choice) < 1:
                    print(f'Choice must be between 1 and {found}. Try again')
                    continue
                break
            if choice.lower() == 'q':
                continue
            if choice.lower() == 'c':
                xlation = ', '.join(set(choices))
            else:
                xlation = choices[int(choice) - 1]
        else:
            #All API's translate the same.
            xlation = choices[0]

        # add card to Anki through AnkiConnect
        add = input('Add to anki? ')
        if add.lower() in ['y', 'yes', 't', 'true']:
            if note_type != "Basic":
                speech = input('Enter Part of Speech: ')
                gender = input('Enter Gender: ') if speech.lower() in ['n', 'noun'] else  ""
                ankiact = {
                    "action": "addNote",
                    "version": 6,
                    "params": {
                        "note": {
                            "deckName": deck_name,
                            "modelName": note_type,
                            "fields": {
                                "Word": orig,
                                "Meaning": xlation,
                                "Part Of Speech": speech,
                                "Gender": gender
                            },
                            "options": {
                                "allowDuplicate": False,
                                "duplicateScope": "deck",
                                "duplicateScopeOptions": {
                                    "deckName": deck_name,
                                    "checkChildren": False,
                                    "checkAllModels": False
                                }
                            }
                        }
                    }
                }
            else :
                #Basic Card type
                ankiact = {
                    "action": "addNote",
                    "version": 6,
                    "params": {
                        "note": {
                            "deckName": deck_name,
                            "modelName": "Basic",
                            "fields": {
                                "Front": orig,
                                "Back": xlation,
                            },
                            "options": {
                                "allowDuplicate": False,
                                "duplicateScope": "deck",
                                "duplicateScopeOptions": {
                                    "deckName": deck_name,
                                    "checkChildren": False,
                                    "checkAllModels": False
                                }
                            }
                        }
                    }
                }

            # Add the card
            ankiresp = requests.post(url = ankiconnect_url, json=ankiact, timeout=10)
            print(ankiresp.json())

            # If sync is turned on, sync with AnkiWeb
            if sync_on_add.lower() not in  ['0', 'false']:
                ankisync = requests.post(url = ankiconnect_url, \
                        json = { "action": "sync", "version": 6}, timeout=30)
                print(ankisync.json())

except KeyboardInterrupt:

    # Cntl-C pressed. End the script.
    print()
    print('Exiting. Goodbye!')
    sys.exit()
