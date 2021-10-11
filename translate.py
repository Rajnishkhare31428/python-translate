import os
import json
from google.cloud import translate
from google.cloud.translate_v3.types.translation_service import TranslateTextRequest, Translation
from file_handler import *

credential_file = 'credentials.json'
translation_config_file = 'translation-config.json'
credentials = json.load(open(credential_file))
translation_config = json.load(open(translation_config_file))
source_language = translation_config['source_language']
target_languages = translation_config['target_languages']
input_file = translation_config['input_file']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'


for language in target_languages:
    reset_index()
    translate_client = translate.TranslationServiceClient() 
    translateRequest = TranslateTextRequest()
    translateRequest.source_language_code = source_language
    translateRequest.parent = 'projects/' + credentials['project_id']
    translateRequest.mime_type = 'text/html'
    translateRequest.target_language_code = language
    translateRequest.contents = get_all_values(input_json, [])
    response = (translate_client.translate_text(translateRequest)).translations
    translated_array = list(response)
    updated_json = get_translated_json(input_json, translated_array)
    put_output_in_file(updated_json, language + '.json')
    
print('Translation finished!')