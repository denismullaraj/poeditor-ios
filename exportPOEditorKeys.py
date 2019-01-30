import sys, os, io, json
import requests

# Dependencies: requests
# Install dependencies: sudo easy_install -U requests
# Use: python exportPOEditorKeys.py

__PUSH_TO_POEDITOR_URL__ = 'https://api.poeditor.com/v2/projects/upload'

POEDITOR_TOKEN = raw_input("Enter your API Token: ")
POEDITOR_PROJECT_ID = raw_input("Enter the project ID: ")
LANG_TO_UPDATE = raw_input("For which language you want to update terms and translations into POEditor? (en, it, sq): ")

def checkResponseAndRaiseException(response):
    if response['response']['status'] != 'success':
        print response
        raise Exception('Unexpected response!')

if __name__ == "__main__":
    
    print "Pushing " + LANG_TO_UPDATE

    file_to_upload = 'iOSApp/Resources/Localization/%s.lproj/Localizable.strings' % LANG_TO_UPDATE

    files = {
        'file': (file_to_upload, open(file_to_upload, 'rb')),
    }

    payload = {
        'api_token': POEDITOR_TOKEN, 
        'id': POEDITOR_PROJECT_ID, 
        'updating': 'terms_translations',
        'language': LANG_TO_UPDATE,
        'overwrite': 1, 
        'sync_terms': 1
    }

    response = requests.post(__PUSH_TO_POEDITOR_URL__, files=files, data= payload).json()
    checkResponseAndRaiseException(response)