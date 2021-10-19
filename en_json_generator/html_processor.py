f = open('en_json_generator/file.html', 'r')
html = f.read()

def get_camel_case(string: str):
    vector = string.split(' ')
    result = ''
    first_time = True
    for element in vector:
        if(first_time):
            result += element.lower()
            first_time = False
        else:
            result += element.capitalize()
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
    chevron_count = 0
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

def process_plain_text(text: str):
    index = 0
    new_text = ''
    interpolation_ongoing = False
    interpolation_index_range = []
    start_index = 0
    end_index = 0
    result = ''
    for char in text:
        if(text[index: index + 2] == '{{'):
            interpolation_ongoing = True
            start_index = index

        if(not interpolation_ongoing):
            new_text += char

        if(text[index - 1: index + 1] == '}}'):
            interpolation_ongoing = False
            end_index = index
            interpolation_index_range.append({
                'start_index': start_index,
                'end_index': end_index
            })

        index += 1
    for i in range(0, len(interpolation_index_range)):
        print(text[interpolation_index_range[i]['start_index']:interpolation_index_range[i]['end_index'] + 1])
    return new_text

def get_interpolation_text(text: str):
    return '{{ \'key\' | translate}}' if not text.strip() == '' else  text
    
def main():
    points = get_plain_text_index_range_array(html)
    new_html = ''
    for i in range(1, len(points)):
        new_html += html[points[i - 1]['end_index']:points[i]['start_index']]
        interpolation_text = (html[points[i]['start_index']:points[i]['end_index']])
        l_spaces = get_l_spaces(interpolation_text)
        r_spaces = get_r_spaces(interpolation_text)
        # if(interpolation_text.strip() == ''):
        #     new_html += (interpolation_text)
        # else:
        #     new_html += l_spaces + '{{ \'' + get_camel_case(interpolation_text).strip() + '\' | translate }}' + r_spaces
        new_html += process_plain_text(interpolation_text)
    new_html += html[points[len(points) - 1]['end_index']:]
    out = open('en_json_generator/new-html.html', 'w')
    out.write(new_html)

plain_text = 'The sum of 1 + 1 is {{1 + 1}}. {{ \'key\' | translate }} out of interpolation {{ xyz }} last part'
print(process_plain_text(plain_text))