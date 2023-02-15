#! /usr/bin/python3
""" Use Rapid API to translate spanish to english and add to anki
     See https://rapidapi.com/translated/api/mymemory-translation-memory
"""
import sys
import threading
import requests
import options

apis = ['mymemory', 'multi-traduction','long-translator']
#apis = ['mymemory']

def call_api(endpoint, text):
    """ Threaded function that makes API call """
    if endpoint == 'mymemory':
        url  = 'https://translated-mymemory---translation-memory.p.rapidapi.com/get'
        headers = {'X-RapidAPI-Key': options.rapidapi}
        params =  {'langpair': 'es|en', 'q': text}

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
    if endpoint == 'multi-traduction':
        url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

        payload = {
        	"from": "es",
        	"to": "en",
        	"e": "",
        	"q": [text]
        }
        headers = {
        	"content-type": "application/json",
        	"X-RapidAPI-Key": options.rapidapi,
        	"X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f'API {endpoint} returned {response.status_code}')
            xlations[endpoint] =  None
        else:
            xlations[endpoint]= None if response.json()[0] == orig else response.json()[0]

    if endpoint == 'long-translator':
        url = "https://long-translator.p.rapidapi.com/translate"

        payload = {
                "source_language": "es",
                "target_language": "en",
                "text": text
                }
        headers = {
	        "content-type": "application/x-www-form-urlencoded",
	        "X-RapidAPI-Key": options.rapidapi,
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
        for api in  apis:
            x = threading.Thread(target=call_api, args=(api, orig))
            threads.append(x)
            x.start()

        # wait for threads to finish
        for thread in threads:
            thread.join()

        # iterate through results from each API call and fill up choices list
        found = 0
        choices = []
        for api in apis:
            if xlations[api]:
                choices.append(xlations[api])
                found += 1
                print(f'{found} from {api}: {xlations[api]}')

        if found == 0:
            continue

        # if more than 1 unique value, give choice to user before adding to anki
        if found > 1 and len(set(choices)) > 1:
            while True:
                choice = input('Enter number choice from above or:\n' +\
                                ' q to skip adding to anki\n' +\
                                ' c to concatenate choices : ')
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
            xlation = choices[0]

        # add user choice to AnkiConnect instance (must be running)
        add = input('Add to anki? ')
        if add.lower() in ['y', 'yes', 't', 'true']:
            speech = input('Enter Part of Speech: ')
            gender = input('Enter Gender: ') if speech.lower() in ['n', 'noun'] else  ""
            ankiact = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": options.deckname,
                        "modelName": "Spanish",
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
                                "deckName": options.deckname,
                                "checkChildren": False,
                                "checkAllModels": False
                            }
                        }
                    }
                }
            }
            ankiresp = requests.post(url = 'http://localhost:8765', json=ankiact, timeout=10)
            print(ankiresp.json())
except KeyboardInterrupt:
    print()
    print('Exiting. Goodbye!')
    sys.exit()
