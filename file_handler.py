import json
from typing import List

json_data = open('en.json')
input_json = json.load(json_data)
# result = []
x = 0

def get_all_values(dict, result: List):
    for key in dict:
        value_type = type(dict[key])
        if value_type == type(dict):
            get_all_values(dict[key], result)
        else:
            result.append(dict[key])
    return result

def put_update_values_back(dict, index: int, translation_vector):
    for key in dict:
        value_type = type(dict[key])
        if value_type != type(dict):
            dict[key] = translation_vector[index] + 'updated' + str(index)
            index += 1
        else:
            put_update_values_back(dict[key], index, translation_vector)
    return dict

value_vector = get_all_values(input_json, [])
output = put_update_values_back(input_json, 0, value_vector)

with open('output.json', 'w') as f:
    json.dump(output, f)