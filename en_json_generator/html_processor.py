f = open('en_json_generator/file.html', 'r')
html = f.read()
result_json = {}
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
    return result

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
    
def main():
    points = get_plain_text_index_range_array(html)
    new_html = ''
    for i in range(1, len(points)):
        new_html += html[points[i - 1]['end_index']:points[i]['start_index']]
        interpolation_text = (html[points[i]['start_index']:points[i]['end_index']])
        new_html += get_interpolation_text(interpolation_text)
    new_html += html[points[len(points) - 1]['end_index']:]
    out = open('en_json_generator/new-html.html', 'w')
    out.write(new_html)

main()
print(result_json)