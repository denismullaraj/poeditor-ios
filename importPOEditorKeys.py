import sys, os, io, json
import requests

# Dependencies: requests
# Install dependencies: sudo easy_install -U requests
# Use: python importPOEditorKeys.py

__PULL_FROM_POEDITOR_URL__ = 'https://api.poeditor.com/v2/projects/export'
__LANGUAGES__ = ["en", "it", "sq"]

POEDITOR_TOKEN = raw_input("Enter your API Token: ")
POEDITOR_PROJECT_ID = raw_input("Enter the project ID: ")

def checkResponseAndRaiseException(response):
    if response['response']['status'] != 'success':
        print response
        raise Exception('Unexpected response!')

def createFolderIfNotExist(resourceDir):
    if not os.path.exists(resourceDir):
        os.makedirs(resourceDir)

if __name__ == "__main__":
        
    for lang in __LANGUAGES__:
    
        print "Pulling " + lang
        
        payload = {
            'api_token': POEDITOR_TOKEN, 
            'id': POEDITOR_PROJECT_ID, 
            'type': 'apple_strings', 
            'language': lang
        }
        response = requests.post(__PULL_FROM_POEDITOR_URL__, data=payload).json()
        checkResponseAndRaiseException(response)
        
        poDownloadUrl = response['result']['url']
        
        poLocalizedText = requests.get(poDownloadUrl).text
        checkResponseAndRaiseException(response)
        
        localizedLatestFilePath = 'iOSApp/Resources/Localization/%s.lproj' % lang
        createFolderIfNotExist(localizedLatestFilePath)
        
        with io.open(localizedLatestFilePath + '/Localizable.strings', 'w', encoding='utf8') as output_file:
            output_file.write(poLocalizedText)