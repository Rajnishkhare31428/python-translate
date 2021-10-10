import json
from typing import List

json_data = open('en.json')
input_json = json.load(json_data)
index = 0

def get_all_values(dict, result: List):
    for key in dict:
        value_type = type(dict[key])
        if value_type == type(dict):
            get_all_values(dict[key], result)
        else:
            result.append(dict[key])
    return result

def get_translated_json(dict,translation_vector):
    global index
    for key in dict:
        value_type = type(dict[key])
        if value_type != type(dict):
            dict[key] = translation_vector[index].translated_text
            index += 1
        else:
            get_translated_json(dict[key], translation_vector)
    return dict

def reset_index():
    global index
    index = 0

def put_output_in_file(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f)

