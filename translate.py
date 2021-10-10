import os
import json
from google.cloud import translate
from google.cloud.translate_v3.types.translation_service import TranslateTextRequest
from main import result

credential_file = 'credentials.json'
translation_config_file = 'translation-config.json'
credentials = json.load(open(credential_file))
translation_config = json.load(open(translation_config_file))
source_language = translation_config['source_language']
target_languages = translation_config['target_languages']
input_file = translation_config['input_file']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

translate_client = translate.TranslationServiceClient() 

translateRequest = TranslateTextRequest()
translateRequest.source_language_code = source_language
translateRequest.parent = 'projects/' + credentials['project_id']

for language in target_languages:
    translateRequest.target_language_code = language
    translateRequest.contents = result
    response = (translate_client.translate_text(translateRequest)).translations
    print(len(response))
    for x in response:
        print(x.translated_text)