import os
import json

result_json = {}

def load_json(json_file_path):
    global result_json
    json_content = json.load(open(json_file_path))
    result_json = json_content

def dump_json(json_file_path):
    global result_json
    output_stream = open(json_file_path, 'w')
    output_stream.write(json.dumps(result_json))
    output_stream.close()

def get_camel_case(string: str):
    global result_json
    vector = string.strip().split(' ')
    result = ''
    first_time = True
    for element in vector:
        if(first_time):
            result += element.lower()
            first_time = False
        else:
            result += element.capitalize()
    result_json[result] = string.strip()
    return remove_specified_characters(result, '\'\"`\n')

def remove_specified_characters(string: str, except_str: str):
    new_string = ''
    for char in string:
        if(not char in except_str):
            new_string += char
    return new_string

def get_plain_text_index_range_array(html: str):
    plain_text = ''
    chevron_ongoing = False
    string_ongoing = False
    comment_ongoing = False
    start_index = 0
    end_index = 0
    plain_text_index_range_array = []
    index = 0
    for char in html:
        if(html[index: index + 4] == '<!--' and not string_ongoing):
            comment_ongoing = True
        if(char == '<' and not (string_ongoing or comment_ongoing)):
            chevron_ongoing = True
            end_index = index
            plain_text_index_range_array.append({
                'start_index': start_index,
                'end_index': end_index,
            })
        if(char == '>' and not (string_ongoing or comment_ongoing)):
            chevron_ongoing = False
            start_index = index + 1
        if(char == '\"' and chevron_ongoing):
            string_ongoing = not string_ongoing
        if(not chevron_ongoing):
            plain_text += char
        index += 1
        if(html[index - 2: index + 1] == '-->'):
            comment_ongoing = False
    return plain_text_index_range_array

def get_l_spaces(text: str):
    new_string = ''
    for char in text:
        if(char == ' ' or char == '\n'):
            new_string += char
        else:
            return new_string
    return new_string

def get_r_spaces(text: str):
    new_string = ''
    for char in text[::1]:
        if(char == ' ' or char == '\n'):
            new_string += char
        else:
            return new_string
    return new_string

def get_interpolation_syntax(text: str):
    return ('{{ \'' + get_camel_case(text) + '\' | translate }}' if not text.strip() == '' else text)

def process_plain_text(text: str):
    index = 0
    new_text = ''
    interpolation_ongoing = False
    interpolation_index_range = [{
        'start_index': 0,
        'end_index': 0
    }]
    start_index = 0
    end_index = 0
    result = ''
    for char in text:
        if(text[index: index + 2] == '{{' or char == '&'):
            interpolation_ongoing = True
            start_index = index

        if(not interpolation_ongoing):
            new_text += char

        if(text[index - 1: index + 1] == '}}' or char == ';'):
            interpolation_ongoing = False
            end_index = index
            interpolation_index_range.append({
                'start_index': start_index,
                'end_index': end_index + 1
            })

        index += 1
    for i in range(1, len(interpolation_index_range)):
        indexes = interpolation_index_range
        temp = text[indexes[i - 1]['end_index']: indexes[i]['start_index']]
        result += get_interpolation_syntax(temp)
        result += text[indexes[i]['start_index']:indexes[i]['end_index']]
    result += get_interpolation_syntax(text[interpolation_index_range[len(interpolation_index_range) - 1]['end_index']:])
    return result

def get_interpolation_text(text: str):
    return process_plain_text(text) if not text.strip() == '' else  text
    
def process_untranslated_text(html_file_path):
    html_file = open(html_file_path, 'r')
    html = html_file.read()
    points = get_plain_text_index_range_array(html)
    if(points == []):
        return
    new_html = ''
    for i in range(1, len(points)):
        new_html += html[points[i - 1]['end_index']:points[i]['start_index']]
        interpolation_text = (html[points[i]['start_index']:points[i]['end_index']])
        new_html += get_interpolation_text(interpolation_text)
    new_html += html[points[len(points) - 1]['end_index']:]
    html_file.close()
    rewrite_file = open(html_file_path, 'w')
    rewrite_file.write(new_html)

# Returns path of all html file in a directory recursively
def get_all_html_files(directory):
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if '.html' in file:
                files.append(os.path.join(r, file))
    return files


def main(project_path, en_json_path):
    global result_json
    load_json(en_json_path)
    html_files = get_all_html_files(project_path)
    for html_file in html_files:
        print('Processing file:' + html_file)
        process_untranslated_text(html_file)
        print('Done processing file:' + html_file)
    dump_json(en_json_path)
    print('Done!!!')


def test_execution():
    json_path = 'D:\\windows_project\\hyperluxe\\web\\src\\assets\\lang-file\\en.json'
    project_path = 'D:\\windows_project\\hyperluxe\\web\\src\\app'
    main(project_path, json_path)

def test_user_input_execution():
    json_path = input('Input your json file complete path')
    project_path = input('Input your angular project source path')
    main(project_path, json_path)

def test_single_html_file(html_file_path):
    print('Processing file:' + html_file_path)
    process_untranslated_text(html_file_path)
    print('Done processing file:' + html_file_path)
    
test_execution()

# test_single_html_file('D:\\windows_project\\hyperluxe\\web\\src\\app\\pages\\auth\\auth.component.html')