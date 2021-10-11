import json
from typing import List

index = 0

def get_all_values_recursively(dict, result: List):
    for key in dict:
        value_type = type(dict[key])
        if value_type == type(dict):
            get_all_values_recursively(dict[key], result)
        else:
            result.append(dict[key])
    return result

def get_translated_json(dict, translated_array):
    global index
    for key in dict:
        value_type = type(dict[key])
        if value_type != type(dict):
            dict[key] = str(translated_array[index].translated_text)
            index += 1
        else:
            get_translated_json(dict[key], translated_array)
    return dict

def reset_index():
    global index
    index = 0

def put_output_in_file(dict, filename):
    with open('output/' + filename, 'w') as f:
        # json.dumps(dict, f)
        content = json.dumps(dict)
        f.write(content)
        f.close()

